#!/usr/bin/env python3
"""
自动监听网络请求获取部门ID映射 - 使用现有页面
"""

from playwright.sync_api import sync_playwright
import json
import time

def get_dept_map_from_network():
    """
    通过监听网络请求获取部门映射
    """
    departments = {}
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        # 找到已登录的页面
        page = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if "uf-tree.com" in pg.url and "login" not in pg.url:
                    page = pg
                    break
            if page:
                break
        
        if not page:
            print("❌ 未找到已登录的页面")
            browser.close()
            return None
        
        print(f"✅ 使用现有页面: {page.url}")
        page.bring_to_front()
        
        # 设置响应监听器
        captured_data = []
        
        def handle_response(response):
            url = response.url
            
            # 拦截部门列表API
            if '/api/member/department' in url:
                print(f"\n📡 拦截到: {url[:80]}")
                
                try:
                    body = response.json()
                    captured_data.append(body)
                    
                    if body.get('code') == 200 and body.get('data'):
                        print(f"✅ 获取到部门数据！")
                        
                        def parse_dept(dept_list, parent=""):
                            for dept in dept_list:
                                dept_id = dept.get('id')
                                name = dept.get('name') or dept.get('label')
                                
                                if dept_id and name:
                                    full_name = f"{parent}/{name}" if parent else name
                                    departments[full_name] = dept_id
                                    print(f"   📁 {full_name}: {dept_id}")
                                
                                # 子部门
                                children = dept.get('children', [])
                                if children:
                                    parse_dept(children, name)
                        
                        parse_dept(body['data'])
                        
                except Exception as e:
                    print(f"⚠️ 解析失败: {e}")
        
        # 监听响应
        page.on("response", handle_response)
        
        # 刷新页面触发请求
        print("\n🔄 刷新页面触发请求...")
        page.reload()
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        # 如果没有数据，尝试点击部门选择框
        if not departments:
            print("\n🖱️  尝试点击部门选择框...")
            try:
                page.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
                time.sleep(2)
                
                page.click('button:has-text("添加员工")', timeout=5000)
                page.click('text=直接添加', timeout=5000)
                time.sleep(2)
                
                page.click('.vue-treeselect__input', timeout=5000)
                time.sleep(3)
                
            except Exception as e:
                print(f"⚠️ {e}")
        
        # 等待一段时间
        time.sleep(3)
        
        browser.close()
        
        return departments

def main():
    print("="*60)
    print("🔍 自动获取部门ID映射（网络监听）")
    print("="*60)
    
    depts = get_dept_map_from_network()
    
    if depts:
        print(f"\n{'='*60}")
        print(f"✅ 共获取 {len(depts)} 个部门")
        print(f"{'='*60}")
        
        # 保存完整映射
        with open('department_map.json', 'w', encoding='utf-8') as f:
            json.dump(depts, f, indent=2, ensure_ascii=False)
        
        # 保存简化映射
        simple = {k.split('/')[-1]: v for k, v in depts.items()}
        with open('department_map_simple.json', 'w', encoding='utf-8') as f:
            json.dump(simple, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 已保存到:")
        print(f"   - department_map.json")
        print(f"   - department_map_simple.json")
        
        print(f"\n📊 建议的 Excel 映射:")
        for i, (name, dept_id) in enumerate(sorted(simple.items()), 1):
            if any(x in name for x in ['门店', '部门', '集团']):
                print(f"   Excel 部门={i} → {name} (ID:{dept_id})")
    else:
        print("\n❌ 未获取到数据")
    
    print("\n✅ 完成！")

if __name__ == "__main__":
    main()
