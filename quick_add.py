#!/usr/bin/env python3
"""
快速添加 - 使用验证过的部门ID
"""

import requests
import pandas as pd
import json
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://cst.uf-tree.com"

def get_token():
    """获取Token"""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "cst.uf-tree.com" in pg.url and "login" not in pg.url:
                    token = pg.evaluate("""() => {
                        const raw = localStorage.getItem('vuex');
                        if (!raw) return null;
                        const store = JSON.parse(raw);
                        return store.user && store.user.token ? store.user.token : null;
                    }""")
                    browser.close()
                    return token
        browser.close()
    return None

def test_dept_id(dept_id, token):
    """测试部门ID是否有效"""
    url = f"{BASE_URL}/api/member/userInfo/add"
    headers = {
        "x-token": token,
        "Content-Type": "application/json"
    }
    payload = {
        "nickName": f"测试{dept_id}",
        "mobile": f"1380000{dept_id:04d}",
        "departmentIds": [dept_id],
        "companyId": 7792
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        result = response.json()
        
        # 成功或已存在都表示ID有效
        if result.get("code") == 200 or result.get("success") or "已存在" in result.get("message", "") or "已在本企业" in result.get("message", ""):
            return True
        return False
    except:
        return False

def add_employee(name, phone, dept_id, token):
    """添加员工"""
    url = f"{BASE_URL}/api/member/userInfo/add"
    headers = {
        "x-token": token,
        "Content-Type": "application/json"
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
    print("🤖 快速添加员工")
    print("="*60)
    
    # 1. 获取Token
    print("\n🔑 获取Token...")
    TOKEN = get_token()
    if not TOKEN:
        print("❌ 未找到Token")
        return
    print(f"✅ Token: {TOKEN[:20]}...")
    
    # 2. 自动检测可用部门ID
    print("\n🔍 检测可用部门ID...")
    test_ids = [9151, 9152, 9153, 2, 3, 100, 101, 102]
    valid_ids = []
    
    for dept_id in test_ids:
        if test_dept_id(dept_id, TOKEN):
            valid_ids.append(dept_id)
            print(f"   ✅ ID {dept_id}: 有效")
        else:
            print(f"   ❌ ID {dept_id}: 无效")
    
    if not valid_ids:
        print("❌ 未找到可用部门ID")
        return
    
    print(f"\n✅ 可用部门ID: {valid_ids}")
    
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
    
    # 4. 轮询分配到可用部门
    print(f"\n🎯 分配策略: 轮询到 {len(valid_ids)} 个部门")
    assignments = []
    for idx, row in df.iterrows():
        dept_id = valid_ids[idx % len(valid_ids)]
        assignments.append({
            'name': row['姓名'],
            'phone': str(row['手机号']),
            'dept_id': dept_id
        })
        print(f"   {idx+1}. {row['姓名']} → 部门ID:{dept_id}")
    
    # 5. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    for i, a in enumerate(assignments, 1):
        print(f"\n[{i}/{len(assignments)}] {a['name']} (部门{a['dept_id']})...", end=" ")
        
        ok, msg = add_employee(a['name'], a['phone'], a['dept_id'], TOKEN)
        
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
