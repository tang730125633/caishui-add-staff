#!/usr/bin/env python3
"""
检查财税通页面上的所有按钮
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    
    for ctx in browser.contexts:
        for page in ctx.pages:
            if "uf-tree.com" in page.url and "staff" in page.url:
                print("=" * 60)
                print("🔍 分析财税通员工页面")
                print("=" * 60)
                
                page.bring_to_front()
                
                # 截图
                page.screenshot(path='/tmp/page_check.png', full_page=True)
                print("\n📸 页面截图已保存: /tmp/page_check.png")
                
                # 查找所有按钮
                print("\n🎛️ 页面上的所有按钮:")
                buttons = page.query_selector_all('button')
                for i, btn in enumerate(buttons):
                    try:
                        if btn.is_visible():
                            text = btn.inner_text().strip()
                            classes = btn.get_attribute('class') or ''
                            print(f"\n  按钮 [{i}]:")
                            print(f"    文字: '{text}'")
                            print(f"    class: {classes[:80]}")
                            
                            # 检查是否有子元素（图标等）
                            children = btn.query_selector_all('*')
                            for child in children:
                                child_class = child.get_attribute('class') or ''
                                if 'icon' in child_class or 'svg' in child_class:
                                    print(f"    子元素: {child_class[:50]}")
                    except Exception as e:
                        print(f"  按钮 [{i}]: 获取信息失败 - {e}")
                
                # 查找所有带 click 事件的元素
                print("\n\n🖱️ 所有可点击的元素:")
                clickable = page.query_selector_all('button, a, [role="button"]')
                for i, el in enumerate(clickable[:20]):  # 只显示前20个
                    try:
                        if el.is_visible():
                            tag = el.evaluate('el => el.tagName')
                            text = el.inner_text().strip()[:30]
                            print(f"  [{i}] <{tag}> '{text}'")
                    except:
                        pass
    
    browser.close()
    print("\n✅ 检查完成")
