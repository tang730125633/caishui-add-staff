#!/usr/bin/env python3
"""
通用批量添加 - 手动指定部门（适用于新账号）
"""

import requests
import pandas as pd
import json
from playwright.sync_api import sync_playwright
import time

BASE_URL = "https://cst.uf-tree.com"

def get_token():
    """从浏览器获取Token"""
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
    print("🤖 通用批量添加员工 - 新账号版")
    print("="*60)
    
    # 1. 获取Token
    print("\n🔑 从浏览器获取Token...")
    TOKEN = get_token()
    if not TOKEN:
        print("❌ 未找到Token")
        return
    print(f"✅ Token: {TOKEN[:20]}...")
    
    # 2. 手动输入部门ID（因为新账号可能结构不同）
    print("\n" + "="*60)
    print("⚠️  请手动指定要添加到的部门ID")
    print("="*60)
    print("\n请在浏览器中查看部门ID：")
    print("1. 打开财税通员工管理页面")
    print("2. 点击'添加员工' -> '直接添加'")
    print("3. 点击部门选择框，在开发者工具(F12)中查看")
    print("\n或尝试常用ID：9151(门店1), 9152(门店2), 9153(门店3)")
    
    # 尝试自动检测（从已知信息）
    test_ids = [9151, 9152, 9153, 1, 2, 3, 100, 101, 102]
    
    print("\n🧪 自动检测可用部门ID...")
    valid_depts = []
    for dept_id in test_ids[:3]:  # 只测试前3个
        # 测试添加一个虚拟员工来验证ID是否有效
        test_phone = f"1380000{dept_id:04d}"
        ok, msg = add_employee_api("测试员工", test_phone, dept_id, TOKEN)
        
        if ok or "已存在" in msg or "已在本企业" in msg:
            print(f"   ID {dept_id}: ✅ 有效")
            valid_depts.append(dept_id)
        elif "无操作权限" in msg or "department" in msg.lower():
            print(f"   ID {dept_id}: ❌ 无效")
        else:
            print(f"   ID {dept_id}: ⚠️ {msg}")
    
    if not valid_depts:
        # 手动输入
        dept_id_str = input("\n请输入部门ID (如9151): ").strip()
        try:
            dept_id = int(dept_id_str)
        except:
            print("❌ 无效的ID")
            return
    else:
        dept_id = valid_depts[0]
        print(f"\n✅ 使用部门ID: {dept_id}")
    
    # 3. 读取Excel
    excel_file = "/Users/tang/Desktop/~员工信息_第二批.xlsx"
    print(f"\n📊 读取: 员工信息_第二批.xlsx")
    df = pd.read_excel(excel_file)
    print(f"共 {len(df)} 个员工")
    print(f"将全部分配到部门ID: {dept_id}")
    
    # 4. 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    for idx, row in df.iterrows():
        print(f"\n[{idx+1}/{len(df)}] {row['姓名']}...", end=" ")
        
        ok, msg = add_employee_api(row['姓名'], str(row['手机号']), dept_id, TOKEN)
        
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
