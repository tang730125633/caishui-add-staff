#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - v4 精修版
"""

from playwright.sync_api import sync_playwright
import csv
import time

CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def add_employee(page, name, phone, department):
    """添加单个员工"""
    print(f"\n  正在添加: {name} ({phone}) - {department}")
    
    try:
        # 1. 点击"添加员工"按钮
        print("    🔍 点击'添加员工'按钮...")
        add_btn = page.query_selector('button:has-text("添加员工")')
        if add_btn and add_btn.is_visible():
            add_btn.click()
            print("    ✅ 已点击")
            time.sleep(1.5)
        else:
            print("    ❌ 未找到按钮")
            return False
        
        # 2. 填写手机号
        print("    📝 填写手机号...")
        phone_input = page.query_selector('input[placeholder*="手机号"]')
        if phone_input:
            phone_input.fill(phone)
            print(f"    ✅ 手机号: {phone}")
        else:
            print("    ❌ 未找到手机号输入框")
            return False
        
        # 3. 填写姓名
        print("    📝 填写姓名...")
        name_input = page.query_selector('input[placeholder*="姓名"]')
        if name_input:
            name_input.fill(name)
            print(f"    ✅ 姓名: {name}")
        else:
            print("    ❌ 未找到姓名输入框")
            return False
        
        # 4. 选择部门
        print("    🏢 选择部门...")
        
        # 点击部门下拉框
        dept_select = page.query_selector('.el-select:has(.el-input__inner[placeholder*="部门"])')
        if not dept_select:
            # 备选：找placeholder包含"部门"的input
            dept_select = page.query_selector('input[placeholder*="部门"]')
        
        if dept_select:
            dept_select.click()
            print("    ✅ 点击部门选择框")
            time.sleep(0.8)
            
            # 选择具体部门
            dept_option = page.query_selector(f'.el-select-dropdown__item:has-text("{department}")')
            if dept_option and dept_option.is_visible():
                dept_option.click()
                print(f"    ✅ 选择部门: {department}")
                time.sleep(0.5)
            else:
                # 打印可用选项
                options = page.query_selector_all('.el-select-dropdown__item')
                print(f"    ⚠️ 未找到'{department}'，可用选项:")
                for opt in options[:5]:
                    try:
                        text = opt.inner_text()
                        print(f"      - {text}")
                    except:
                        pass
                page.keyboard.press('Escape')
        else:
            print("    ⚠️ 未找到部门选择框")
        
        # 5. 点击保存
        print("    💾 点击保存...")
        
        # 找弹窗中的保存按钮
        save_btn = page.query_selector('.el-dialog__footer button.el-button--primary')
        if not save_btn:
            save_btn = page.query_selector('.el-dialog button:has-text("保存")')
        
        if save_btn and save_btn.is_visible():
            save_btn.click()
            print("    ✅ 已点击保存")
            time.sleep(2)
            
            # 检查成功消息
            try:
                msg = page.query_selector('.el-message--success, .el-message--error')
                if msg and msg.is_visible():
                    print(f"    📢 提示: {msg.inner_text()}")
            except:
                pass
            
            print(f"    ✅ 完成添加: {name}")
            return True
        else:
            print("    ❌ 未找到保存按钮")
            page.screenshot(path=f'/tmp/error_save_{name}.png')
            return False
        
    except Exception as e:
        print(f"    ❌ 错误: {e}")
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v4")
    print("=" * 60)
    
    # 读取数据
    employees = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(row)
    
    print(f"\n📁 读取到 {len(employees)} 条员工数据")
    for emp in employees:
        print(f"   - {emp['姓名']} | {emp['手机号']} | {emp['部门']}")
    
    # 连接浏览器
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        print("\n✅ 连接浏览器成功")
        
        # 找到目标页面
        target_page = None
        for ctx in browser.contexts:
            for page in ctx.pages:
                if "uf-tree.com" in page.url and "staff" in page.url:
                    target_page = page
                    break
            if target_page:
                break
        
        if not target_page:
            print("❌ 未找到财税通页面")
            return
        
        target_page.bring_to_front()
        print("✅ 找到目标页面\n")
        
        # 添加员工
        success = 0
        fail = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"[{i}/{len(employees)}]", end="")
            result = add_employee(target_page, emp['姓名'], emp['手机号'], emp['部门'])
            if result:
                success += 1
            else:
                fail += 1
            
            if i < len(employees):
                time.sleep(2)
        
        # 刷新页面查看结果
        print("\n🔄 刷新页面查看结果...")
        target_page.reload()
        time.sleep(2)
        target_page.screenshot(path='/tmp/final_result.png', full_page=True)
        print("📸 结果截图: /tmp/final_result.png")
        
        print("\n" + "=" * 60)
        print(f"📊 结果: 成功 {success}, 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
