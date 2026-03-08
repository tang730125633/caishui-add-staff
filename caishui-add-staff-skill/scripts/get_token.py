#!/usr/bin/env python3
"""
从浏览器抓取部门ID映射
"""

from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    
    # 找到已登录的页面
    page = None
    for ctx in browser.contexts:
        for pg in ctx.pages:
            if "uf-tree.com" in pg.url and "login" not in pg.url:
                page = pg
                print(f"✅ 找到页面: {pg.url}")
                break
    
    if not page:
        print("❌ 未找到已登录的页面")
        browser.close()
        exit(1)
    
    page.bring_to_front()
    
    # 方法1: 通过页面 API 获取部门列表
    print("\n🔍 方法1: 通过页面 fetch API 获取部门...")
    
    result = page.evaluate("""async () => {
        try {
            const res = await fetch('/api/member/department/list');
            return await res.json();
        } catch (e) {
            return { error: e.message };
        }
    }""")
    
    print(f"\n📦 API 响应:")
    print(json.dumps(result, indent=2, ensure_ascii=False)[:1500])
    
    # 解析部门数据
    departments = {}
    if result.get('code') == 200 and result.get('data'):
        for dept in result['data']:
            dept_id = dept.get('id')
            dept_name = dept.get('name')
            if dept_id and dept_name:
                departments[dept_name] = dept_id
                
            # 处理子部门
            children = dept.get('children', [])
            for child in children:
                child_id = child.get('id')
                child_name = child.get('name')
                if child_id and child_name:
                    departments[child_name] = child_id
    
    if departments:
        print(f"\n✅ 找到 {len(departments)} 个部门:")
        for name, dept_id in departments.items():
            print(f"   - {name}: {dept_id}")
        
        # 保存到文件
        with open('/Users/tang/Desktop/自动添加员工项目/department_map.json', 'w') as f:
            json.dump(departments, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 已保存到 department_map.json")
    
    # 方法2: 从 localStorage 或页面变量获取
    print("\n🔍 方法2: 从页面变量获取...")
    
    vuex = page.evaluate('() => JSON.parse(localStorage.getItem("vuex") || "{}")')
    if vuex and 'user' in vuex:
        company = vuex['user'].get('company', {})
        print(f"   Company: {company.get('name')} (ID: {company.get('id')})")
    
    browser.close()
    
    print("\n✅ 完成！")
