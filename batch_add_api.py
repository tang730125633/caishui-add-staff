#!/usr/bin/env python3
"""
使用 API 批量添加员工 - 自动获取 Token 版本
"""

import requests
import pandas as pd
import json
import os
from playwright.sync_api import sync_playwright

# 配置
BASE_URL = "https://cst.uf-tree.com"

def get_token_from_browser():
    """
    从已登录的浏览器实时获取 Token
    从 localStorage 的 vuex 中读取（注意：是 'vuex' 不是 'ls_vuex'）
    """
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
                    
                    # 导航到添加页面触发数据加载
                    pg.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
                    pg.click('button:has-text("添加员工")')
                    pg.click('text=直接添加')
                    pg.wait_for_timeout(2000)
                    pg.click('.vue-treeselect__input')
                    pg.wait_for_timeout(2000)
                    
                    # 从 Vue 组件读取部门数据
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
    """调用 API 添加员工"""
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
    print("🤖 使用 API 批量添加员工")
    print("="*60)
    
    # 1. 获取 Token（实时从浏览器读取）
    print("\n🔑 从浏览器获取 Token...")
    TOKEN = get_token_from_browser()
    
    if not TOKEN:
        print("❌ 未找到 Token，请确保：")
        print("   1. Chrome 已启动调试模式 (--remote-debugging-port=9222)")
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
    
    # 3. 读取 Excel
    excel_files = [f for f in os.listdir('/Users/tang/Desktop') 
                   if f.endswith('.xlsx') and '员工' in f and not f.startswith('.') and not f.startswith('~')]
    
    if not excel_files:
        print("❌ 未找到员工信息 Excel 文件")
        return
    
    excel_file = f"/Users/tang/Desktop/{excel_files[0]}"
    print(f"\n📊 读取: {excel_files[0]}")
    
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    
    # 4. 智能匹配部门
    # 获取门店列表（排除集团）
    store_list = [n for n in dept_map.keys() if '门店' in n or '部门' in n]
    store_list.sort()
    
    # 创建编号映射（1,2,3...）
    store_by_index = {str(i+1): dept_map[name] for i, name in enumerate(store_list)}
    
    print(f"\n📋 Excel 部门编号映射:")
    for num, dept_id in sorted(store_by_index.items()):
        name = [k for k, v in dept_map.items() if v == dept_id][0]
        print(f"   部门 {num} → {name} (ID:{dept_id})")
    
    # 5. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    
    for idx, row in df.iterrows():
        name = row['姓名']
        phone = str(row['手机号'])
        dept_num = str(row['部门'])
        
        dept_id = store_by_index.get(dept_num)
        if not dept_id:
            print(f"\n[{idx+1}/{len(df)}] {name}... ❌ 未知部门编号: {dept_num}")
            fail += 1
            continue
        
        dept_name = [k for k, v in dept_map.items() if v == dept_id][0]
        
        print(f"\n[{idx+1}/{len(df)}] {name} ({dept_name})...", end=" ")
        
        ok, msg = add_employee_api(name, phone, dept_id, TOKEN)
        
        if ok:
            print(f"✅ {msg}")
            success += 1
        else:
            print(f"❌ {msg}")
            fail += 1
    
    print("\n" + "="*60)
    print(f"📊 完成: 成功 {success}/{len(df)}")
    print("="*60)

if __name__ == "__main__":
    main()
