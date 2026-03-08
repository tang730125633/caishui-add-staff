#!/usr/bin/env python3
"""
自动监听网络请求获取部门ID映射
使用 Playwright 拦截 API 响应
"""

from playwright.sync_api import sync_playwright
import json
import time

def get_department_map_auto():
    """
    自动获取部门ID映射
    原理：监听页面网络请求，拦截部门列表API的响应
    """
    departments = {}
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.new_page()
        
        # 设置请求拦截器
        def handle_response(response):
            """处理响应"""
            url = response.url
            
            # 只关注部门列表API
            if '/api/member/department/list' in url or '/api/department/list' in url:
                print(f"\n📡 拦截到部门列表请求: {url}")
                
                try:
                    # 获取响应体
                    body = response.json()
                    print(f"📦 响应数据: {json.dumps(body, indent=2, ensure_ascii=False)[:1000]}")
                    
                    # 解析部门数据
                    if body.get('code') == 200 and body.get('data'):
                        data = body['data']
                        print(f"\n✅ 成功获取部门数据！")
                        
                        # 递归解析部门树
                        def parse_dept_tree(dept_list, parent_name=""):
                            for dept in dept_list:
                                dept_id = dept.get('id')
                                name = dept.get('name') or dept.get('label') or dept.get('departmentName')
                                
                                if dept_id and name:
                                    # 如果有父部门，拼接名称
                                    full_name = f"{parent_name}/{name}" if parent_name else name
                                    departments[full_name] = dept_id
                                    print(f"   📁 {full_name}: {dept_id}")
                                
                                # 处理子部门
                                children = dept.get('children') or dept.get('childList') or []
                                if children:
                                    parse_dept_tree(children, name)
                        
                        parse_dept_tree(data)
                        
                except Exception as e:
                    print(f"⚠️ 解析响应失败: {e}")
        
        # 监听响应
        page.on("response", handle_response)
        
        # 导航到员工页面（触发部门列表请求）
        print("🌐 导航到员工管理页面...")
        page.goto("https://cst.uf-tree.com/company/staff")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # 如果没有拦截到，尝试点击部门选择框触发请求
        if not departments:
            print("\n🔍 尝试点击部门选择框触发请求...")
            try:
                # 点击添加员工
                page.click('button:has-text("添加员工")', timeout=5000)
                page.click('text=直接添加', timeout=5000)
                time.sleep(2)
                
                # 点击部门选择框
                page.click('.vue-treeselect__input', timeout=5000)
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ 点击失败: {e}")
        
        # 等待一段时间确保所有请求完成
        time.sleep(3)
        
        browser.close()
    
    return departments

def main():
    print("="*60)
    print("🔍 自动获取部门ID映射（网络监听方式）")
    print("="*60)
    print("\n原理：监听页面网络请求，自动拦截部门列表API响应")
    print("="*60)
    
    depts = get_department_map_auto()
    
    if depts:
        print(f"\n✅ 共获取 {len(depts)} 个部门:")
        print("\n📋 部门映射表:")
        print("-"*60)
        for name, dept_id in sorted(depts.items()):
            print(f"   {name:30s} → {dept_id}")
        print("-"*60)
        
        # 保存到文件
        with open('department_map.json', 'w', encoding='utf-8') as f:
            json.dump(depts, f, indent=2, ensure_ascii=False)
        
        # 同时生成简化的映射（去掉父部门前缀）
        simple_map = {}
        for name, dept_id in depts.items():
            # 只保留最后一部分名称
            simple_name = name.split('/')[-1]
            simple_map[simple_name] = dept_id
        
        with open('department_map_simple.json', 'w', encoding='utf-8') as f:
            json.dump(simple_map, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 已保存:")
        print(f"   - department_map.json (完整路径)")
        print(f"   - department_map_simple.json (简化名称)")
        
        # 生成 Excel 可用的映射
        print(f"\n📊 Excel 部门编号映射建议:")
        print("-"*60)
        for i, (name, dept_id) in enumerate(sorted(simple_map.items()), 1):
            if '门店' in name or '部门' in name:
                print(f"   Excel列'部门'填 {i} → {name} (ID: {dept_id})")
        
    else:
        print("\n❌ 未获取到部门数据")
        print("💡 请确保:")
        print("   1. 浏览器已启动调试模式")
        print("   2. 已登录财税通系统")
        print("   3. 已进入企业")
    
    print("\n✅ 完成！")

if __name__ == "__main__":
    main()
