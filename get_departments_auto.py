#!/usr/bin/env python3
"""
通过页面 JavaScript 获取部门数据
在页面上下文中执行 fetch，自动携带正确的 cookie
"""

from playwright.sync_api import sync_playwright
import json
import time

def get_departments_js():
    """
    使用页面 JavaScript 获取部门数据
    """
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
        
        print(f"✅ 页面: {page.url}")
        page.bring_to_front()
        
        # 方法1: 尝试从页面 Vue 变量获取（之前成功过）
        print("\n🔍 方法1: 从 Vue 实例获取...")
        
        depts_vue = page.evaluate('''() => {
            // 尝试多种方式获取 Vue 中的部门数据
            
            // 方式1: 从 vue-treeselect 组件
            const treeselect = document.querySelector('.vue-treeselect');
            if (treeselect && treeselect.__vue__) {
                return {
                    source: 'vue-treeselect',
                    data: treeselect.__vue__.options
                };
            }
            
            // 方式2: 从 Vuex store
            if (window.__VUE__ && window.__VUE__.$store) {
                const state = window.__VUE__.$store.state;
                if (state.department || state.departments) {
                    return {
                        source: 'vuex',
                        data: state.department || state.departments
                    };
                }
            }
            
            // 方式3: 查找全局变量
            for (const key of Object.keys(window)) {
                const val = window[key];
                if (val && Array.isArray(val) && val.length > 0 && val[0] && (val[0].id || val[0].label)) {
                    return {
                        source: `window.${key}`,
                        data: val
                    };
                }
            }
            
            return null;
        }''')
        
        if depts_vue and depts_vue.get('data'):
            print(f"✅ 从 {depts_vue['source']} 获取到数据！")
            return parse_departments(depts_vue['data'])
        
        # 方法2: 导航到添加页面，触发部门选择框加载数据
        print("\n🔍 方法2: 导航到添加员工页面...")
        
        page.goto("https://cst.uf-tree.com/company/staff", timeout=15000)
        time.sleep(2)
        
        # 点击添加员工
        page.click('button:has-text("添加员工")')
        page.click('text=直接添加')
        time.sleep(2)
        
        # 点击部门选择框，触发数据加载
        page.click('.vue-treeselect__input')
        time.sleep(2)
        
        # 再次尝试获取 Vue 数据
        depts_vue2 = page.evaluate('''() => {
            const treeselect = document.querySelector('.vue-treeselect');
            if (treeselect && treeselect.__vue__) {
                return treeselect.__vue__.options;
            }
            return null;
        }''')
        
        if depts_vue2:
            print(f"✅ 成功获取部门数据！")
            return parse_departments(depts_vue2)
        
        # 方法3: 直接从页面元素解析
        print("\n🔍 方法3: 从页面元素解析...")
        
        options = page.query_selector_all('.vue-treeselect__option')
        print(f"   找到 {len(options)} 个选项")
        
        depts_from_dom = {}
        for opt in options:
            text = opt.inner_text() if opt.inner_text() else ''
            # 尝试从 data-value 或其他属性获取ID
            opt_id = opt.get_attribute('data-value') or opt.get_attribute('aria-label') or ''
            if text:
                depts_from_dom[text] = opt_id
                print(f"   - {text}: {opt_id}")
        
        if depts_from_dom:
            return depts_from_dom
        
        browser.close()
        return None

def parse_departments(data):
    """解析部门数据"""
    departments = {}
    
    if not isinstance(data, list):
        return departments
    
    for item in data:
        if not isinstance(item, dict):
            continue
        
        dept_id = item.get('id')
        name = item.get('label') or item.get('name')
        
        if dept_id and name:
            departments[name] = dept_id
            print(f"   📁 {name}: {dept_id}")
        
        # 递归处理子部门
        children = item.get('children', [])
        if children:
            for child in children:
                child_id = child.get('id')
                child_name = child.get('label') or child.get('name')
                if child_id and child_name:
                    full_name = f"{name}/{child_name}"
                    departments[full_name] = child_id
                    print(f"   📁 {full_name}: {child_id}")
    
    return departments

def main():
    print("="*60)
    print("🔍 自动获取部门ID映射（JavaScript方式）")
    print("="*60)
    
    depts = get_departments_js()
    
    if depts:
        print(f"\n{'='*60}")
        print(f"✅ 共获取 {len(depts)} 个部门")
        print(f"{'='*60}")
        
        # 保存
        with open('department_map.json', 'w', encoding='utf-8') as f:
            json.dump(depts, f, indent=2, ensure_ascii=False)
        
        # 简化版本
        simple = {}
        for name, dept_id in depts.items():
            short_name = name.split('/')[-1]
            simple[short_name] = dept_id
        
        with open('department_map_simple.json', 'w', encoding='utf-8') as f:
            json.dump(simple, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 已保存到 department_map.json")
        print(f"\n📊 部门列表:")
        for i, (name, dept_id) in enumerate(sorted(simple.items()), 1):
            print(f"   {i}. {name} (ID: {dept_id})")
        
        print(f"\n💡 Excel 使用建议:")
        print(f"   在Excel的'部门'列中填入编号 1-{len(simple)}")
        print(f"   脚本会自动映射到对应的部门ID")
        
    else:
        print("\n❌ 未能获取部门数据")
    
    print("\n✅ 完成！")

if __name__ == "__main__":
    main()
