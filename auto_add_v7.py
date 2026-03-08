#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - v7 完整版
包含部门选择
"""

from playwright.sync_api import sync_playwright
import csv
import time

CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def navigate_to_add_page(page):
    """导航到添加员工页面"""
    # 进入员工管理页面
    page.goto('https://cst.uf-tree.com/company/staff')
    time.sleep(2)
    
    # 关闭可能的弹窗
    page.keyboard.press('Escape')
    time.sleep(0.5)
    
    # 查找并点击添加新员工入口
    # 方法1: 找卡片式入口
    cards = page.query_selector_all('.staff-item, .add-staff-card, .card')
    for card in cards:
        try:
            if card.is_visible():
                text = card.inner_text()
                if '添加' in text or '新增' in text:
                    card.click()
                    time.sleep(2)
                    return True
        except:
            pass
    
    # 方法2: 直接尝试通过JavaScript点击
    try:
        page.evaluate('''() => {
            // 找包含"添加新员工"的元素
            const elements = document.querySelectorAll('*');
            for (const el of elements) {
                if (el.textContent && el.textContent.includes('添加新员工')) {
                    el.click();
                    return true;
                }
            }
            return false;
        }''')
        time.sleep(2)
        return True
    except:
        pass
    
    return False

def find_and_click_department(page, dept_name):
    """查找并点击部门选择框"""
    print(f"    选择部门: {dept_name}...", end="")
    
    # 方法1: 找placeholder为"请选择"的input
    dept_input = page.query_selector('input[placeholder="请选择"]')
    if dept_input and dept_input.is_visible():
        dept_input.click()
        time.sleep(0.8)
        
        # 查找部门选项
        option_selectors = [
            f'.el-select-dropdown__item:has-text("{dept_name}")',
            f'li:has-text("{dept_name}")',
            f'.el-scrollbar__view li:has-text("{dept_name}")',
        ]
        
        for selector in option_selectors:
            try:
                option = page.query_selector(selector)
                if option and option.is_visible():
                    option.click()
                    print(f"✅")
                    time.sleep(0.5)
                    return True
            except:
                pass
        
        # 如果没找到，打印可用选项
        print(f"⚠️ 未找到'{dept_name}'")
        all_options = page.query_selector_all('.el-select-dropdown__item, .el-scrollbar__view li')
        print(f"      可用选项({len(all_options)}个):")
        for opt in all_options[:10]:
            try:
                if opt.is_visible():
                    text = opt.inner_text()
                    print(f"        - {text}")
            except:
                pass
        
        page.keyboard.press('Escape')
        return False
    
    print("⚠️ 未找到部门选择框")
    return False

def add_employee(page, name, phone, department):
    """添加单个员工"""
    print(f"\n  添加: {name} | {phone} | {department}")
    
    try:
        # 1. 填写手机
        print("    填写手机...", end="")
        phone_input = page.query_selector('input[placeholder="请输入员工手机"]')
        if phone_input:
            phone_input.fill(phone)
            print(f"✅")
        else:
            print("❌ 未找到")
            return False
        
        # 2. 填写姓名
        print("    填写姓名...", end="")
        name_input = page.query_selector('input[placeholder="请输入员工姓名"]')
        if name_input:
            name_input.fill(name)
            print(f"✅")
        else:
            print("❌ 未找到")
            return False
        
        # 3. 选择部门
        find_and_click_department(page, department)
        
        # 4. 点击保存并继续添加
        print("    点击保存...", end="")
        save_btn = page.query_selector('button:has-text("保存并继续添加")')
        if save_btn and save_btn.is_visible():
            save_btn.click()
            print("✅")
            time.sleep(2)
            
            # 检查结果
            msg = page.query_selector('.el-message--success, .el-message--error, .el-message')
            if msg and msg.is_visible():
                msg_text = msg.inner_text()
                print(f"    📢 {msg_text}")
                if '成功' in msg_text:
                    return True
                elif '已存在' in msg_text:
                    print("    ⚠️ 用户已存在，跳过")
                    return True
            
            return True
        else:
            print("❌ 未找到保存按钮")
            return False
        
    except Exception as e:
        print(f"\n    ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v7")
    print("=" * 60)
    
    # 读取数据
    employees = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(row)
    
    print(f"\n📋 数据: {len(employees)} 人")
    for emp in employees:
        print(f"   - {emp['姓名']} -> {emp['部门']}")
    
    # 连接浏览器
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        print("\n✅ 连接浏览器")
        
        # 找到目标页面
        target_page = None
        for ctx in browser.contexts:
            for page in ctx.pages:
                if "uf-tree.com" in page.url:
                    target_page = page
                    break
            if target_page:
                break
        
        if not target_page:
            print("❌ 未找到页面")
            return
        
        target_page.bring_to_front()
        
        # 导航到添加页面
        print("\n🔄 导航到添加页面...")
        if not navigate_to_add_page(target_page):
            print("⚠️ 导航可能失败，尝试继续...")
        
        # 检查当前页面
        title = target_page.query_selector('.title')
        if title:
            print(f"📄 当前页面: {title.inner_text()}")
        
        # 添加员工
        success = fail = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}]", end="")
            if add_employee(target_page, emp['姓名'], emp['手机号'], emp['部门']):
                success += 1
            else:
                fail += 1
            
            if i < len(employees):
                time.sleep(1.5)
        
        print("\n" + "=" * 60)
        print(f"📊 完成: 成功 {success} / 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
