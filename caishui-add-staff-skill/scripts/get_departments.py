#!/usr/bin/env python3
"""
获取部门ID映射工具
从页面 Vue 实例中提取部门数据
"""

from playwright.sync_api import sync_playwright
import json

def get_department_map():
    """获取部门ID映射"""
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
        
        # 从页面 Vue 实例获取部门数据
        depts = page.evaluate('''() => {
            const vueEl = document.querySelector('.vue-treeselect');
            if (vueEl && vueEl.__vue__) {
                return vueEl.__vue__.options;
            }
            return null;
        }''')
        
        if not depts:
            print("❌ 未找到部门数据")
            browser.close()
            return None
        
        # 构建映射
        dept_map = {}
        for dept in depts:
            dept_id = dept.get('id')
            label = dept.get('label')
            if dept_id and label:
                dept_map[label] = dept_id
                print(f"   - {label}: {dept_id}")
        
        browser.close()
        return dept_map

if __name__ == "__main__":
    print("="*60)
    print("🔍 获取部门ID映射")
    print("="*60)
    
    dept_map = get_department_map()
    
    if dept_map:
        # 保存到文件
        with open('department_map.json', 'w', encoding='utf-8') as f:
            json.dump(dept_map, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 已保存到 department_map.json")
        print("\n✅ 完成！")
    else:
        print("\n❌ 获取失败")
