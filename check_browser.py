#!/usr/bin/env python3
"""
连接已登录的 Comet 浏览器实例 - 轻量版
"""

from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        print("🔌 正在连接到调试端口 9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        print("✅ 成功连接到浏览器！")
        
        # 获取默认上下文
        contexts = browser.contexts
        print(f"📊 浏览器上下文数量: {len(contexts)}")
        
        for ctx_idx, context in enumerate(contexts):
            pages = context.pages
            print(f"\n  上下文[{ctx_idx}] 有 {len(pages)} 个页面:")
            
            for page_idx, page in enumerate(pages):
                url = page.url
                print(f"    [{page_idx}] URL: {url[:80]}...")
                
                # 检查是否是财税通页面
                if "uf-tree" in url:
                    print(f"    ✅ 找到财税通页面！")
                    
                    # 尝试截图
                    try:
                        screenshot_path = f"/tmp/caishui_page_{ctx_idx}_{page_idx}.png"
                        page.screenshot(path=screenshot_path)
                        print(f"    📸 截图: {screenshot_path}")
                    except Exception as e:
                        print(f"    ⚠️ 截图失败: {e}")
        
        print("\n✅ 检查完成！")
        browser.close()

if __name__ == "__main__":
    main()
