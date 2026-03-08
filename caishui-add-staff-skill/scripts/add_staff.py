#!/usr/bin/env python3
"""
财税通员工批量添加 Skill - 最终通用版
作者: AI Assistant
日期: 2026-03-08

功能: 自动获取Token和部门映射，批量添加员工到财税通系统
适用: 任何账号、任何部门结构
"""

import requests
import pandas as pd
import json
import os
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://cst.uf-tree.com"

def get_token_from_browser():
    """
    从浏览器 localStorage 实时获取 Token
    注意: key是'vuex'，不是'ls_vuex'
    """
    js = """
    () => {
        const v = JSON.parse(localStorage.getItem('vuex'));
        return v.user.token;
    }
    """
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "cst.uf-tree.com" in pg.url and "login" not in pg.url:
                    token = pg.evaluate(js)
                    browser.close()
                    return token
        browser.close()
    return None

def get_department_map_and_company(token):
    """
    通过 API 获取部门映射和公司ID
    接口: POST /api/member/department/queryCompany
    特点: 空body即可，任何账号通用
    """
    resp = requests.post(
        f"{BASE_URL}/api/member/department/queryCompany",
        headers={"x-token": token, "Content-Type": "application/json"},
        json={},  # 空body即可
        timeout=10
    )
    
    result = resp.json()
    if not result.get("success") and result.get("code") != 200:
        raise Exception(f"获取部门失败: {result.get('message')}")
    
    dept_map = {}
    result_data = result.get("result", {})
    departments = result_data.get("departments", [])
    company_id = 7792
    
    if departments and len(departments) > 0:
        company_id = departments[0].get("companyId", 7792)
    
    for dept in departments:
        if isinstance(dept, dict):
            dept_map[dept.get("title", "")] = dept.get("id")
            for child in dept.get("children", []) or []:
                if isinstance(child, dict):
                    dept_map[child.get("title", "")] = child.get("id")
    
    # 过滤掉空key
    dept_map = {k: v for k, v in dept_map.items() if k and v}
    
    return dept_map, company_id

def add_employee(name, phone, dept_id, token, company_id):
    """调用API添加单个员工"""
    url = f"{BASE_URL}/api/member/userInfo/add"
    headers = {
        "x-token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "nickName": name,
        "mobile": phone,
        "departmentIds": [dept_id],
        "companyId": company_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()
        
        if result.get("code") == 200 or result.get("success"):
            return True, "添加成功"
        elif "已存在" in result.get("message", "") or "已在本企业" in result.get("message", ""):
            return True, "已存在"
        else:
            return False, result.get("message", "未知错误")
    except Exception as e:
        return False, str(e)

def main():
    """主函数: 完整流程"""
    print("="*60)
    print("🤖 财税通员工批量添加 - 通用版")
    print("="*60)
    
    # 1. 获取Token
    print("\n🔑 获取Token...")
    token = get_token_from_browser()
    if not token:
        print("❌ 未找到Token，请确保已登录浏览器")
        return
    print(f"✅ Token获取成功")
    
    # 2. 获取部门映射
    print("\n🔍 获取部门映射...")
    try:
        dept_map, company_id = get_department_map_and_company(token)
    except Exception as e:
        print(f"❌ {e}")
        return
    
    print(f"✅ 找到 {len(dept_map)} 个部门 (公司ID: {company_id})")
    
    # 3. 查找Excel文件
    excel_files = [f for f in os.listdir('/Users/tang/Desktop') 
                   if f.endswith('.xlsx') and '员工' in f and not f.startswith('.')]
    
    if not excel_files:
        print("❌ 未找到员工Excel文件")
        return
    
    excel_path = f"/Users/tang/Desktop/{excel_files[0]}"
    print(f"\n📊 读取: {excel_files[0]}")
    
    # 4. 读取员工数据
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"❌ 读取Excel失败: {e}")
        return
    
    print(f"✅ 共 {len(df)} 个员工")
    
    # 5. 准备可用部门
    stores = [(name, dept_id) for name, dept_id in dept_map.items() 
              if '门店' in name or '测试' in name]
    if not stores:
        stores = list(dept_map.items())[:10]
    
    print(f"\n📋 可用部门: {len(stores)}个")
    
    # 6. 分配并添加
    print("\n🚀 开始批量添加...")
    success = fail = 0
    
    for idx, row in df.iterrows():
        store_name, store_id = stores[idx % len(stores)]
        name = row['姓名']
        phone = str(row['手机号'])
        
        print(f"\n[{idx+1}/{len(df)}] {name} ({store_name})...", end=" ")
        
        ok, msg = add_employee(name, phone, store_id, token, company_id)
        
        if ok:
            print(f"✅ {msg}")
            success += 1
        else:
            print(f"❌ {msg}")
            fail += 1
        
        time.sleep(0.3)
    
    # 7. 输出结果
    print("\n" + "="*60)
    print(f"📊 完成: 成功 {success}/{len(df)}, 失败 {fail}")
    print("="*60)

if __name__ == "__main__":
    main()
