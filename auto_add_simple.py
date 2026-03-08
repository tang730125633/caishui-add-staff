#!/usr/bin/env python3
"""
通用批量添加员工 - 简化版（避免点击拦截）
"""

import requests
import pandas as pd
import json
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://cst.uf-tree.com"

def get_token_and_depts():
    """从浏览器获取Token和部门数据"""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "cst.uf-tree.com" in pg.url and "login" not in pg.url:
                    pg.bring_to_front()
                    
                    # 获取Token
                    token_js = """
                    () => {
                        const raw = localStorage.getItem('vuex');
                        if (!raw) return null;
                        const store = JSON.parse(raw);
                        return store.user && store.user.token ? store.user.token : null;
                    }
                    """
                    token = pg.evaluate(token_js)
                    
                    # 导航到员工页面（触发数据加载）
                    pg.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
                    time.sleep(3)
                    
                    # 直接从localStorage尝试获取部门数据
                    dept_js = """
                    () => {
                        // 尝试多种方式获取部门数据
                        
                        // 方式1: 从localStorage的vuex中找
                        const raw = localStorage.getItem('vuex');
                        if (raw) {
                            const store = JSON.parse(raw);
                            // 尝试找部门相关数据
                            if (store.department) return {source: 'vuex.department', data: store.department};
                            if (store.departments) return {source: 'vuex.departments', data: store.departments};
                        }
                        
                        // 方式2: 找全局变量
                        if (window.departments) return {source: 'window.departments', data: window.departments};
                        if (window.deptList) return {source: 'window.deptList', data: window.deptList};
                        
                        // 方式3: 扫描Vue组件
                        const treeselect = document.querySelector('.vue-treeselect');
                        if (treeselect && treeselect.__vue__) {
                            return {source: 'vue-component', data: treeselect.__vue__.options};
                        }
                        
                        return null;
                    }
                    """
                    
                    result = pg.evaluate(dept_js)
                    browser.close()
                    
                    if result and result.get('data'):
                        # 解析部门数据
                        dept_map = {}
                        data = result['data']
                        
                        if isinstance(data, list):
                            for d in data:
                                if isinstance(d, dict):
                                    dept_id = d.get('id')
                                    name = d.get('label') or d.get('name')
                                    if dept_id and name:
                                        dept_map[name] = dept_id
                        
                        return token, dept_map, result.get('source', 'unknown')
        
        browser.close()
    return None, {}, 'none'

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
    print("🤖 通用批量添加员工 - 自动适应新账号")
    print("="*60)
    
    # 1. 获取Token和部门数据
    print("\n🔑 从浏览器获取Token和部门数据...")
    TOKEN, dept_map, source = get_token_and_depts()
    
    if not TOKEN:
        print("❌ 未找到Token")
        return
    print(f"✅ Token: {TOKEN[:20]}...")
    
    if not dept_map:
        print("❌ 无法获取部门数据")
        # 使用默认映射作为备选
        print("⚠️ 使用默认部门映射...")
        dept_map = {
            "测试门店1": 9151,
            "测试门店2": 9152,
            "测试门店3": 9153
        }
    
    print(f"✅ 部门数据来源: {source}")
    print(f"找到 {len(dept_map)} 个部门:")
    for name, dept_id in sorted(dept_map.items()):
        print(f"   - {name}: {dept_id}")
    
    # 2. 获取可用门店
    stores = [(name, dept_id) for name, dept_id in dept_map.items() 
              if '门店' in name or '部门' in name]
    
    if not stores:
        print("❌ 未找到可用门店")
        return
    
    print(f"\n📋 可用门店: {len(stores)}个")
    for i, (name, dept_id) in enumerate(stores, 1):
        print(f"   {i}. {name}")
    
    # 3. 读取Excel
    excel_files = [f for f in os.listdir('/Users/tang/Desktop') 
                   if f.endswith('.xlsx') and '员工' in f and not f.startswith('.')]
    
    if not excel_files:
        print("❌ 未找到员工信息Excel文件")
        return
    
    excel_file = f"/Users/tang/Desktop/{excel_files[0]}"
    print(f"\n📊 读取: {excel_files[0]}")
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    
    # 4. 智能分配（轮询）
    print("\n🎯 智能分配:")
    assignments = []
    for idx, row in df.iterrows():
        # 轮询选择
        store_name, store_id = stores[idx % len(stores)]
        assignments.append({
            'name': row['姓名'],
            'phone': str(row['手机号']),
            'dept_name': store_name,
            'dept_id': store_id
        })
    
    print("\n📋 分配预览:")
    for i, a in enumerate(assignments, 1):
        print(f"   {i}. {a['name']} → {a['dept_name']}")
    
    # 5. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    for i, a in enumerate(assignments, 1):
        print(f"\n[{i}/{len(assignments)}] {a['name']} ({a['dept_name']})...", end=" ")
        
        ok, msg = add_employee_api(a['name'], a['phone'], a['dept_id'], TOKEN)
        
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
    import os
    main()
