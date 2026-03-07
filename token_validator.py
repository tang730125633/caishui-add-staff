#!/usr/bin/env python3
"""
Token有效性验证工具
用于检测Token是否过期，并提供友好的提示
"""

import requests
import json

def validate_token(config_file="config.json"):
    """验证Token是否有效"""
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        
        token = config.get("token")
        company_id = config.get("company_id")
        
        if not token or not company_id:
            return False, "配置不完整，缺少token或company_id"
        
        # 测试API调用
        headers = {
            "x-token": token,
            "Content-Type": "application/json"
        }
        
        test_data = {
            "nickName": "Token测试",
            "mobile": "13800000000",
            "departmentIds": [9151],
            "companyId": company_id
        }
        
        response = requests.post(
            "https://cst.uf-tree.com/api/member/userInfo/add",
            headers=headers,
            json=test_data,
            timeout=5
        )
        
        result = response.json()
        
        if result.get("success"):
            return True, "Token有效"
        else:
            msg = result.get("message", "")
            if "登陆失效" in msg or "失效" in msg:
                return False, "Token已过期，需要重新获取"
            elif "已存在" in msg or "已在本企业" in msg:
                return True, "Token有效（员工已存在）"
            else:
                return False, f"API错误: {msg}"
                
    except FileNotFoundError:
        return False, "配置文件不存在"
    except Exception as e:
        return False, f"验证失败: {e}"

if __name__ == "__main__":
    print("🔍 验证Token有效性...")
    is_valid, message = validate_token()
    
    if is_valid:
        print(f"✅ {message}")
        print("\n可以正常使用API批量添加员工！")
    else:
        print(f"❌ {message}")
        print("\n请运行以下命令重新获取Token:")
        print("  1. 确保浏览器已启动调试模式: chrome --remote-debugging-port=9222")
        print("  2. 登录财税通系统")
        print("  3. 运行: python auto_config_helper.py")
