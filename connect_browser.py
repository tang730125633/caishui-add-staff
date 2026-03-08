#!/usr/bin/env python3
"""
连接已登录的 Comet 浏览器实例
"""

from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        print("🔌 正在连接到调试端口 9222...")
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        
        print("✅ 成功连接到浏览器！")
        
        contexts = browser.contexts
        print(f"📊 找到 {len(contexts)} 个浏览器上下文")
        
        all_pages = []
        for context in contexts:
            all_pages.extend(context.pages)
        
        print(f"📄 找到 {len(all_pages)} 个页面")
        
        if not all_pages:
            print("⚠️ 没有找到任何页面，请先在 Comet 里打开财税通网站")
            return
        
        for i, page in enumerate(all_pages):
            try:
                url = page.url
                title = page.title()
                print(f"\n  [{i}] 标题: {title}")
                print(f"      URL: {url}")
                
                # 检查是否是财税通页面
                if "uf-tree" in url or "财税" in title:
                    print("  ✅ 找到财税通页面！")
                    
                    # 截图
                    try:
                        screenshot_path = f"/tmp/caishui_page_{i}.png"
                        page.screenshot(path=screenshot_path, full_page=True)
                        print(f"  📸 截图已保存: {screenshot_path}")
                    except Exception as e:
                        print(f"  ⚠️ 截图失败: {e}")
                        
            except Exception as e:
                print(f"  ⚠️ 获取页面信息失败: {e}")
        
        print("\n✅ 浏览器连接成功！")
        print("⏸️ 按 Ctrl+C 结束")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 断开连接")

if __name__ == "__main__":
    main()
