#!/usr/bin/env python3
"""
通用批量添加员工 - 自动适应新账号
自动获取Token和部门映射，智能分配员工
"""

import requests
import pandas as pd
import json
import os
from playwright.sync_api import sync_playwright

BASE_URL = "https://cst.uf-tree.com"

def get_token_from_browser():
    """从浏览器获取Token（实时）"""
    js = """
    () => {
        const raw = localStorage.getItem('vuex');
        if (!raw) return null;
        const store = JSON.parse(raw);
        return store.user && store.user.token ? store.user.token : null;
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

def get_department_map():
    """从浏览器获取部门映射"""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "cst.uf-tree.com" in pg.url and "login" not in pg.url:
                    pg.bring_to_front()
                    pg.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
                    pg.wait_for_timeout(2000)
                    pg.click('button:has-text("添加员工")')
                    pg.click('text=直接添加')
                    pg.wait_for_timeout(2000)
                    pg.click('.vue-treeselect__input')
                    pg.wait_for_timeout(2000)
                    
                    depts = pg.evaluate('''() => {
                        const el = document.querySelector('.vue-treeselect');
                        return el && el.__vue__ ? el.__vue__.options : null;
                    }''')
                    
                    browser.close()
                    
                    if depts:
                        dept_map = {}
                        for d in depts:
                            if d.get('id') and d.get('label'):
                                dept_map[d['label']] = d['id']
                        return dept_map
        browser.close()
    return {}

def add_employee_api(name, phone, dept_id, token):
    """调用API添加员工"""
    url = f"{BASE_URL}/api/member/userInfo/add"
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
    print("🤖 通用批量添加员工（自动适应新账号）")
    print("="*60)
    
    # 1. 获取Token
    print("\n🔑 从浏览器获取Token...")
    TOKEN = get_token_from_browser()
    if not TOKEN:
        print("❌ 未找到Token，请确保：")
        print("   1. Chrome已启动调试模式")
        print("   2. 已登录财税通系统")
        print("   3. 浏览器窗口保持打开")
        return
    print(f"✅ Token: {TOKEN[:20]}...")
    
    # 2. 获取部门映射
    print("\n🔍 获取部门映射...")
    dept_map = get_department_map()
    if not dept_map:
        print("❌ 无法获取部门映射")
        return
    
    print(f"✅ 找到 {len(dept_map)} 个部门:")
    for name, dept_id in sorted(dept_map.items()):
        print(f"   - {name}: {dept_id}")
    
    # 3. 获取可用门店（排除集团）
    stores = [(name, dept_id) for name, dept_id in dept_map.items() 
              if '门店' in name or '部门' in name]
    stores.sort()
    
    if not stores:
        print("❌ 未找到可用门店")
        return
    
    print(f"\n📋 可用门店（{len(stores)}个）:")
    for i, (name, dept_id) in enumerate(stores, 1):
        print(f"   {i}. {name} (ID:{dept_id})")
    
    # 4. 读取Excel
    excel_file = "/Users/tang/Desktop/~员工信息_第二批.xlsx"
    print(f"\n📊 读取: 员工信息_第二批.xlsx")
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    
    # 5. 智能分配策略
    print("\n🎯 智能分配策略:")
    print("   员工将自动分配到可用门店")
    print("   采用轮询方式均匀分配")
    
    # 轮询分配
    store_index = 0
    assignments = []
    
    for idx, row in df.iterrows():
        # 轮询选择门店
        store_name, store_id = stores[store_index % len(stores)]
        assignments.append({
            'name': row['姓名'],
            'phone': str(row['手机号']),
            'dept_name': store_name,
            'dept_id': store_id
        })
        store_index += 1
    
    print("\n📋 分配预览:")
    for i, assign in enumerate(assignments, 1):
        print(f"   {i}. {assign['name']} → {assign['dept_name']}")
    
    # 6. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    
    for i, assign in enumerate(assignments, 1):
        print(f"\n[{i}/{len(assignments)}] {assign['name']} ({assign['dept_name']})...", end=" ")
        
        ok, msg = add_employee_api(assign['name'], assign['phone'], assign['dept_id'], TOKEN)
        
        if ok:
            print(f"✅ {msg}")
            success += 1
        else:
            print(f"❌ {msg}")
            fail += 1
    
    print("\n" + "="*60)
    print(f"📊 完成: 成功 {success}/{len(df)}")
    print("="*60)
    
    # 统计各部门人数
    print("\n📈 各部门分布:")
    from collections import Counter
    dept_counts = Counter([a['dept_name'] for a in assignments])
    for dept, count in dept_counts.most_common():
        print(f"   {dept}: {count}人")

if __name__ == "__main__":
    main()
