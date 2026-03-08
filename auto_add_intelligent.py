#!/usr/bin/env python3
"""
智能批量添加员工 - 自动获取部门映射
"""

import requests
import pandas as pd
import json
import os
from playwright.sync_api import sync_playwright

# 配置
TOKEN_FILE = "x_token.json"
BASE_URL = "https://cst.uf-tree.com"

def get_token():
    """获取 Token"""
    # 尝试从文件读取
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            data = json.load(f)
            return data.get('token', '')
    
    # 从浏览器获取
    print("🔑 从浏览器获取 Token...")
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        for ctx in browser.contexts:
            for page in ctx.pages:
                if "uf-tree.com" in page.url:
                    vuex = page.evaluate('() => JSON.parse(localStorage.getItem("vuex") || "{}")')
                    token = vuex.get('user', {}).get('token', '')
                    browser.close()
                    
                    # 保存
                    with open(TOKEN_FILE, 'w') as f:
                        json.dump({'token': token}, f)
                    
                    return token
        
        browser.close()
    
    return ''

def get_department_map():
    """获取部门映射"""
    # 检查是否已有映射文件
    if os.path.exists('department_map_simple.json'):
        with open('department_map_simple.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 自动获取
    print("\n🔍 自动获取部门映射...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        for ctx in browser.contexts:
            for page in ctx.pages:
                if "uf-tree.com" in page.url and "login" not in page.url:
                    page.bring_to_front()
                    
                    # 导航到添加页面
                    page.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
                    page.click('button:has-text("添加员工")')
                    page.click('text=直接添加')
                    time.sleep(2)
                    page.click('.vue-treeselect__input')
                    time.sleep(2)
                    
                    # 获取 Vue 数据
                    depts = page.evaluate('''() => {
                        const el = document.querySelector('.vue-treeselect');
                        return el && el.__vue__ ? el.__vue__.options : null;
                    }''')
                    
                    browser.close()
                    
                    if depts:
                        # 解析
                        dept_map = {}
                        for d in depts:
                            if d.get('id') and d.get('label'):
                                dept_map[d['label']] = d['id']
                        
                        # 保存
                        with open('department_map_simple.json', 'w', encoding='utf-8') as f:
                            json.dump(dept_map, f, indent=2, ensure_ascii=False)
                        
                        return dept_map
        
        browser.close()
    
    return {}

def add_employee_api(name, phone, dept_id, token):
    """调用 API 添加员工"""
    headers = {
        "x-token": token,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "nickName": name,
        "mobile": phone,
        "departmentIds": [dept_id],
        "companyId": 7792
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/member/userInfo/add",
            headers=headers,
            json=payload,
            timeout=10
        )
        result = response.json()
        
        if result.get("code") == 200 or result.get("success"):
            return True, "添加成功"
        else:
            return False, result.get("message", "未知错误")
    except Exception as e:
        return False, str(e)

def main():
    import time
    
    print("="*60)
    print("🤖 智能批量添加员工（自动获取部门映射）")
    print("="*60)
    
    # 1. 获取 Token
    token = get_token()
    if not token:
        print("❌ 无法获取 Token")
        return
    print(f"✅ Token: {token[:20]}...")
    
    # 2. 获取部门映射
    dept_map = get_department_map()
    if not dept_map:
        print("❌ 无法获取部门映射")
        return
    
    print(f"\n✅ 部门映射:")
    for name, dept_id in sorted(dept_map.items()):
        print(f"   - {name}: {dept_id}")
    
    # 3. 读取 Excel
    excel_files = [f for f in os.listdir('/Users/tang/Desktop') 
                   if f.endswith('.xlsx') and '员工' in f and not f.startswith('.') and not f.startswith('~')]
    
    if not excel_files:
        print("❌ 未找到员工信息 Excel 文件")
        # 尝试直接使用已知文件
        excel_file = "/Users/tang/Desktop/~员工信息_提取版.xlsx"
        if not os.path.exists(excel_file):
            print("❌ 文件不存在")
            return
    else:
        excel_file = f"/Users/tang/Desktop/{excel_files[0]}"
    
    print(f"\n📊 读取: {os.path.basename(excel_file)}")
    
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    
    # 4. 准备部门映射（直接使用名称匹配）
    print(f"\n📋 部门映射:")
    for name, dept_id in sorted(dept_map.items()):
        print(f"   {name} → ID:{dept_id}")
    
    # 5. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    
    for idx, row in df.iterrows():
        name = row['姓名']
        phone = str(row['手机号'])
        dept_name = str(row['门店'])
        
        dept_id = dept_map.get(dept_name)
        if not dept_id:
            # 尝试模糊匹配
            for k, v in dept_map.items():
                if dept_name in k or k in dept_name:
                    dept_id = v
                    dept_name = k
                    break
        
        if not dept_id:
            print(f"\n[{idx+1}/{len(df)}] {name}... ❌ 未知门店: {dept_name}")
            fail += 1
            continue
        
        print(f"\n[{idx+1}/{len(df)}] {name} ({dept_name})...", end=" ")
        
        ok, msg = add_employee_api(name, phone, dept_id, token)
        
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
