#!/usr/bin/env python3
"""
财税通员工自动添加脚本
使用 Playwright 控制 Comet 浏览器
"""

from playwright.sync_api import sync_playwright
import time

# 财税通配置
CAISHUI_URL = "https://cst.uf-tree.com/company/staff"
COMET_PATH = "/Applications/Comet.app/Contents/MacOS/Comet"

def main():
    with sync_playwright() as p:
        # 启动 Comet 浏览器
        print("🚀 正在启动 Comet 浏览器...")
        browser = p.chromium.launch(
            executable_path=COMET_PATH,
            headless=False,  # 显示浏览器窗口，方便调试
            slow_mo=100  # 操作间隔100ms，方便观察
        )
        
        # 创建新页面
        context = browser.new_context(
            viewport={'width': 1400, 'height': 900}
        )
        page = context.new_page()
        
        print(f"🌐 正在打开财税通页面: {CAISHUI_URL}")
        page.goto(CAISHUI_URL, wait_until='networkidle')
        
        # 等待页面加载
        time.sleep(2)
        
        # 获取页面标题
        title = page.title()
        print(f"📄 页面标题: {title}")
        
        # 截图查看当前状态
        screenshot_path = "/tmp/caishui_login_page.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 已截图保存到: {screenshot_path}")
        
        # 尝试查找登录表单元素
        print("\n🔍 正在分析页面结构...")
        
        # 常见的登录输入框选择器
        input_selectors = [
            'input[type="text"]',
            'input[type="email"]',
            'input[name*="user"]',
            'input[name*="login"]',
            'input[name*="phone"]',
            'input[name*="account"]',
            'input[placeholder*="账号"]',
            'input[placeholder*="用户"]',
            'input[placeholder*="手机"]',
        ]
        
        password_selectors = [
            'input[type="password"]',
            'input[name*="pass"]',
            'input[placeholder*="密码"]',
        ]
        
        login_button_selectors = [
            'button[type="submit"]',
            'button:has-text("登录")',
            'button:has-text("Login")',
            'input[type="submit"]',
            'a:has-text("登录")',
        ]
        
        print("\n📋 找到以下输入框:")
        for selector in input_selectors:
            try:
                elements = page.query_selector_all(selector)
                for i, el in enumerate(elements):
                    placeholder = el.get_attribute('placeholder') or ''
                    name = el.get_attribute('name') or ''
                    input_type = el.get_attribute('type') or ''
                    print(f"  - 选择器: {selector}[{i}], placeholder={placeholder}, name={name}, type={input_type}")
            except:
                pass
        
        print("\n🔐 找到以下密码框:")
        for selector in password_selectors:
            try:
                elements = page.query_selector_all(selector)
                for i, el in enumerate(elements):
                    print(f"  - 选择器: {selector}[{i}]")
            except:
                pass
        
        print("\n🖱️ 找到以下按钮:")
        for selector in login_button_selectors:
            try:
                elements = page.query_selector_all(selector)
                for i, el in enumerate(elements):
                    text = el.inner_text() if el else ''
                    print(f"  - 选择器: {selector}[{i}], 文字: {text}")
            except:
                pass
        
        print("\n⏸️ 浏览器保持打开状态，请手动检查页面...")
        print("按 Ctrl+C 结束程序")
        
        # 保持浏览器打开
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 正在关闭浏览器...")
        
        browser.close()
        print("✅ 浏览器已关闭")

if __name__ == "__main__":
    main()
