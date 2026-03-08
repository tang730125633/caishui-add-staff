#!/usr/bin/env python3
"""
使用 API 批量添加员工
"""

import requests
import pandas as pd
import json

# 配置
TOKEN = "v7wGHG-F0CRC45UaHseDE0U4AfQ"
BASE_URL = "https://cst.uf-tree.com"

headers = {
    "x-token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 部门映射（从页面获取的）
DEPT_MAP = {
    "1": 9151,  # 测试门店1
    "2": 9152,  # 测试门店2
    "3": 9153,  # 测试门店3
}

def add_employee_api(name, phone, dept_id):
    """调用 API 添加员工"""
    url = f"{BASE_URL}/api/member/userInfo/add"
    
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
    
    # 读取 Excel
    df = pd.read_excel("/Users/tang/Desktop/~员工信息_提取版.xlsx")
    print(f"\n📊 共 {len(df)} 个员工")
    
    # 显示预览
    print("\n📋 数据预览:")
    for idx, row in df.iterrows():
        dept_name = f"测试门店{row['部门']}"
        dept_id = DEPT_MAP.get(str(row['部门']), 9151)
        print(f"   {row['姓名']} | {row['手机号']} | {dept_name} (ID: {dept_id})")
    
    # 自动确认（无需交互）
    print("\n✅ 自动确认，开始添加...")
    
    # 批量添加
    print("\n" + "="*60)
    print("🚀 开始批量添加")
    print("="*60)
    
    success = fail = 0
    
    for idx, row in df.iterrows():
        name = row['姓名']
        phone = str(row['手机号'])
        dept_num = str(row['部门'])
        dept_id = DEPT_MAP.get(dept_num, 9151)
        
        print(f"\n[{idx+1}/{len(df)}] {name}...", end=" ")
        
        ok, msg = add_employee_api(name, phone, dept_id)
        
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
