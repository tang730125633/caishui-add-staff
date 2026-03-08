#!/usr/bin/env python3
"""
完全通用版 - 使用正确API获取部门映射
通过 POST /api/member/department/queryCompany 获取部门数据
"""

import requests
import pandas as pd
import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://cst.uf-tree.com"

def get_token_from_browser():
    """从浏览器 localStorage 实时获取 Token"""
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
    """通过 API 获取部门映射和公司ID（任何账号通用）"""
    resp = requests.post(
        "https://cst.uf-tree.com/api/member/department/queryCompany",
        headers={"x-token": token, "Content-Type": "application/json"},
        json={},  # 空 body 即可
        timeout=10
    )
    result = resp.json()
    
    if not result.get("success") and result.get("code") != 200:
        raise Exception(f"获取部门失败: {result.get('message')}")
    
    dept_map = {}
    result_data = result.get("result", {})
    departments = result_data.get("departments", [])
    
    # 获取公司ID（从第一个部门中获取，或默认）
    company_id = 7792  # 默认值
    if departments and len(departments) > 0:
        company_id = departments[0].get("companyId", 7792)
    
    for dept in departments:
        dept_id = dept.get("id")
        title = dept.get("title")
        if dept_id and title:
            dept_map[title] = dept_id
        
        # 处理子部门
        children = dept.get("children") or []
        for child in children:
            child_id = child.get("id")
            child_title = child.get("title")
            if child_id and child_title:
                dept_map[child_title] = child_id
    
    return dept_map, company_id

def add_employee_api(name, phone, dept_id, token, company_id=7792):
    """调用API添加员工"""
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
        else:
            return False, result.get("message", "未知错误")
    except Exception as e:
        return False, str(e)

def main():
    print("="*60)
    print("🤖 完全通用版 - 使用正确API获取部门")
    print("="*60)
    
    # 1. 获取Token
    print("\n🔑 从浏览器获取Token...")
    token = get_token_from_browser()
    if not token:
        print("❌ 未找到Token")
        return
    print(f"✅ Token: {token[:20]}...")
    
    # 2. 通过API获取部门映射和公司ID
    print("\n🔍 通过API获取部门映射...")
    try:
        dept_map, company_id = get_department_map_and_company(token)
    except Exception as e:
        print(f"❌ {e}")
        return
    
    print(f"✅ 找到 {len(dept_map)} 个部门 (公司ID: {company_id}):")
    for name, dept_id in sorted(dept_map.items()):
        print(f"   - {name}: {dept_id}")
    
    # 3. 读取Excel
    import os
    excel_files = [f for f in os.listdir('/Users/tang/Desktop') 
                   if f.endswith('.xlsx') and '员工' in f and not f.startswith('.')]
    
    if not excel_files:
        print("❌ 未找到Excel文件")
        return
    
    excel_file = f"/Users/tang/Desktop/{excel_files[0]}"
    print(f"\n📊 读取: {excel_files[0]}")
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    
    # 4. 获取可用部门（优先找"门店"，否则找"测试"，否则取前10个）
    stores = [(name, dept_id) for name, dept_id in dept_map.items() 
              if '门店' in name]
    
    if not stores:
        # 没有"门店"，找包含"测试"的
        stores = [(name, dept_id) for name, dept_id in dept_map.items() 
                  if '测试' in name]
    
    if not stores:
        # 还没有，取所有部门的前10个
        stores = list(dept_map.items())[:10]
    
    if not stores:
        print("❌ 未找到可用部门")
        return
    
    print(f"\n📋 可用部门: {len(stores)}个")
    for i, (name, dept_id) in enumerate(stores[:10], 1):  # 只显示前10个
        print(f"   {i}. {name} (ID:{dept_id})")
    if len(stores) > 10:
        print(f"   ... 还有 {len(stores)-10} 个部门")
    
    # 5. 轮询分配
    print(f"\n🎯 将员工分配到 {len(stores)} 个部门")
    assignments = []
    for idx, row in df.iterrows():
        store_name, store_id = stores[idx % len(stores)]
        assignments.append({
            'name': row['姓名'],
            'phone': str(row['手机号']),
            'dept_name': store_name,
            'dept_id': store_id
        })
    
    print("\n📋 分配预览:")
    for i, a in enumerate(assignments[:10], 1):  # 只显示前10个
        print(f"   {i}. {a['name']} → {a['dept_name']}")
    if len(assignments) > 10:
        print(f"   ... 还有 {len(assignments)-10} 人")
    
    # 6. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    for i, a in enumerate(assignments, 1):
        print(f"\n[{i}/{len(assignments)}] {a['name']} ({a['dept_name']})...", end=" ")
        
        ok, msg = add_employee_api(a['name'], a['phone'], a['dept_id'], token, company_id)
        
        if ok:
            print(f"✅ {msg}")
            success += 1
        else:
            print(f"❌ {msg}")
            fail += 1
        
        time.sleep(0.5)
    
    print("\n" + "="*60)
    print(f"📊 完成: 成功 {success}/{len(df)}")
    print("="*60)

if __name__ == "__main__":
    main()
