#!/usr/bin/env python3
"""
使用示例：财税通员工批量添加
"""

import sys
sys.path.insert(0, '../scripts')

from add_staff import CaishuiStaffManager

def example_basic():
    """基础使用示例"""
    print("="*60)
    print("示例1: 基础使用")
    print("="*60)
    
    # 初始化管理器
    manager = CaishuiStaffManager()
    
    # 初始化（获取Token和部门映射）
    if manager.init():
        print("✅ 初始化成功")
        print(f"   Token: {manager.token[:20]}...")
        print(f"   部门数: {len(manager.dept_map)}")
    else:
        print("❌ 初始化失败")
        return
    
    # 添加单个员工
    success, msg = manager.add_employee(
        name="测试员工",
        phone="13800138000",
        dept_name="测试门店1"
    )
    
    if success:
        print(f"✅ 添加成功: {msg}")
    else:
        print(f"❌ 添加失败: {msg}")

def example_batch():
    """批量添加示例"""
    print("\n" + "="*60)
    print("示例2: 批量添加")
    print("="*60)
    
    manager = CaishuiStaffManager()
    
    if not manager.init():
        print("❌ 初始化失败")
        return
    
    # 从Excel批量添加
    results = manager.add_from_excel("employees.xlsx")
    
    print(f"\n📊 批量添加结果:")
    print(f"   成功: {results['success']}")
    print(f"   失败: {results['failed']}")
    
    if results['errors']:
        print(f"\n❌ 错误详情:")
        for error in results['errors'][:5]:
            print(f"   - {error}")

def example_api_direct():
    """直接调用API示例"""
    print("\n" + "="*60)
    print("示例3: 直接调用API")
    print("="*60)
    
    import requests
    
    # 配置
    TOKEN = "your_token_here"
    BASE_URL = "https://cst.uf-tree.com"
    
    headers = {
        "x-token": TOKEN,
        "Content-Type": "application/json"
    }
    
    payload = {
        "nickName": "API测试员工",
        "mobile": "13800138000",
        "departmentIds": [9151],
        "companyId": 7792
    }
    
    # 调用API
    response = requests.post(
        f"{BASE_URL}/api/member/userInfo/add",
        headers=headers,
        json=payload
    )
    
    result = response.json()
    print(f"📦 响应: {result}")

if __name__ == "__main__":
    # 运行示例
    # example_basic()
    # example_batch()
    # example_api_direct()
    
    print("请取消注释相应的函数调用来运行示例")
