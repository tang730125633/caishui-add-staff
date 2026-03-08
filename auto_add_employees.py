#!/usr/bin/env python3
"""
财税通自动添加员工脚本
从 CSV 文件读取员工信息，自动添加到系统
"""

from playwright.sync_api import sync_playwright
import csv
import time
import random

# 配置文件
CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def wait_for_element(page, selector, timeout=5000):
    """等待元素出现"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        return True
    except:
        return False

def add_employee(page, name, phone, department):
    """添加单个员工"""
    print(f"\n  正在添加: {name} ({phone}) - {department}")
    
    try:
        # 1. 点击"添加员工"按钮
        # 根据页面截图，需要找到添加员工的按钮
        add_button_selectors = [
            'button:has-text("添加")',
            'button:has-text("新增")',
            'a:has-text("添加")',
            'a:has-text("新增")',
            '.add-btn',
            '.add-employee',
            '[class*="add"]',
        ]
        
        add_clicked = False
        for selector in add_button_selectors:
            try:
                button = page.query_selector(selector)
                if button and button.is_visible():
                    button.click()
                    print(f"    ✅ 点击添加按钮: {selector}")
                    add_clicked = True
                    break
            except:
                continue
        
        if not add_clicked:
            print("    ⚠️ 未找到添加按钮，尝试通用方法...")
            # 尝试点击页面上的第一个主要按钮
            buttons = page.query_selector_all('button')
            for btn in buttons:
                if btn.is_visible():
                    text = btn.inner_text()
                    if '添加' in text or '新增' in text or '+' in text:
                        btn.click()
                        add_clicked = True
                        print(f"    ✅ 点击按钮: {text}")
                        break
        
        if not add_clicked:
            print("    ❌ 无法找到添加按钮")
            return False
        
        # 等待弹窗出现
        time.sleep(1)
        
        # 2. 填写姓名
        name_selectors = [
            'input[placeholder*="姓名"]',
            'input[name*="name"]',
            'input[name*="姓名"]',
            'input[id*="name"]',
            'input[label*="姓名"]',
        ]
        
        name_filled = False
        for selector in name_selectors:
            try:
                input_field = page.query_selector(selector)
                if input_field and input_field.is_visible():
                    input_field.fill(name)
                    print(f"    ✅ 填写姓名: {name}")
                    name_filled = True
                    break
            except:
                continue
        
        if not name_filled:
            # 尝试找到所有文本输入框，填第一个
            inputs = page.query_selector_all('input[type="text"]')
            for i, inp in enumerate(inputs):
                if inp.is_visible():
                    inp.fill(name)
                    print(f"    ✅ 填写姓名(备用): {name}")
                    name_filled = True
                    break
        
        # 3. 填写手机号
        phone_selectors = [
            'input[placeholder*="手机"]',
            'input[placeholder*="电话"]',
            'input[name*="phone"]',
            'input[name*="mobile"]',
            'input[type="tel"]',
        ]
        
        phone_filled = False
        for selector in phone_selectors:
            try:
                input_field = page.query_selector(selector)
                if input_field and input_field.is_visible():
                    input_field.fill(phone)
                    print(f"    ✅ 填写手机号: {phone}")
                    phone_filled = True
                    break
            except:
                continue
        
        # 4. 选择部门
        # 先点击部门选择框
        dept_selectors = [
            'input[placeholder*="部门"]',
            '.el-select',  # Element UI 常见选择器
            '[class*="select"]',
            'input[readonly]',  # 有些下拉框是 readonly 的 input
        ]
        
        dept_selected = False
        for selector in dept_selectors:
            try:
                dept_input = page.query_selector(selector)
                if dept_input and dept_input.is_visible():
                    dept_input.click()
                    time.sleep(0.5)
                    
                    # 在下拉列表中查找部门
                    dept_option_selectors = [
                        f'.el-select-dropdown__item:has-text("{department}")',
                        f'li:has-text("{department}")',
                        f'[class*="option"]:has-text("{department}")',
                        f'div:has-text("{department}")',
                    ]
                    
                    for opt_selector in dept_option_selectors:
                        try:
                            option = page.query_selector(opt_selector)
                            if option and option.is_visible():
                                option.click()
                                print(f"    ✅ 选择部门: {department}")
                                dept_selected = True
                                break
                        except:
                            continue
                    
                    if dept_selected:
                        break
            except:
                continue
        
        # 5. 点击保存/确认按钮
        save_selectors = [
            'button:has-text("保存")',
            'button:has-text("确认")',
            'button:has-text("确定")',
            'button:has-text("提交")',
            '.el-button--primary',
        ]
        
        save_clicked = False
        for selector in save_selectors:
            try:
                save_btn = page.query_selector(selector)
                if save_btn and save_btn.is_visible():
                    save_btn.click()
                    print(f"    ✅ 点击保存")
                    save_clicked = True
                    break
            except:
                continue
        
        # 等待保存完成
        time.sleep(1.5)
        
        print(f"    ✅ 员工 {name} 添加流程完成")
        return True
        
    except Exception as e:
        print(f"    ❌ 添加失败: {e}")
        return False

def main():
    print("=" * 50)
    print("🤖 财税通自动添加员工脚本")
    print("=" * 50)
    
    # 读取员工数据
    print(f"\n📁 读取员工数据: {CSV_FILE}")
    employees = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                employees.append(row)
        print(f"✅ 读取到 {len(employees)} 条员工数据")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return
    
    # 连接到浏览器
    print(f"\n🔌 连接到浏览器: {DEBUG_PORT}")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(DEBUG_PORT)
            print("✅ 连接成功!")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print("💡 请确保 Comet 浏览器已用调试模式启动")
            return
        
        # 找到财税通页面
        target_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "uf-tree.com" in page.url and "staff" in page.url:
                    target_page = page
                    break
            if target_page:
                break
        
        if not target_page:
            print("❌ 未找到财税通员工管理页面")
            print("💡 请确保已在 Comet 中打开: https://cst.uf-tree.com/company/staff")
            browser.close()
            return
        
        print(f"✅ 找到目标页面: {target_page.url}")
        
        # 激活页面
        target_page.bring_to_front()
        
        # 开始添加员工
        print("\n" + "=" * 50)
        print("🚀 开始添加员工")
        print("=" * 50)
        
        success_count = 0
        fail_count = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}] ", end="")
            result = add_employee(
                target_page,
                emp['姓名'],
                emp['手机号'],
                emp['部门']
            )
            
            if result:
                success_count += 1
            else:
                fail_count += 1
            
            # 添加间隔，避免操作过快
            if i < len(employees):
                wait_time = random.uniform(2, 3)
                print(f"\n  ⏳ 等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
        
        # 总结
        print("\n" + "=" * 50)
        print("📊 执行结果")
        print("=" * 50)
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"📈 总计: {len(employees)}")
        
        browser.close()
        print("\n🏁 脚本执行完毕!")

if __name__ == "__main__":
    main()
