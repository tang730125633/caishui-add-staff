#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - v5 最终版
"""

from playwright.sync_api import sync_playwright
import csv
import time

CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def add_employee(page, name, phone, department):
    """添加单个员工"""
    print(f"\n  添加: {name} | {phone} | {department}")
    
    try:
        # 1. 点击"添加员工"按钮
        print("    点击'添加员工'...", end="")
        add_btn = page.query_selector('button:has-text("添加员工")')
        if add_btn and add_btn.is_visible():
            add_btn.click()
            print("✅")
            time.sleep(1.5)
        else:
            print("❌ 未找到按钮")
            return False
        
        # 2. 填写手机号
        print("    填写手机号...", end="")
        phone_input = page.query_selector('input[placeholder="请输入员工手机"]')
        if phone_input:
            phone_input.fill(phone)
            print(f"✅ {phone}")
        else:
            print("❌ 未找到")
            return False
        
        # 3. 填写姓名
        print("    填写姓名...", end="")
        name_input = page.query_selector('input[placeholder="请输入员工姓名"]')
        if name_input:
            name_input.fill(name)
            print(f"✅ {name}")
        else:
            print("❌ 未找到")
            return False
        
        # 4. 选择部门（如果有部门选择框）
        print("    选择部门...", end="")
        dept_input = page.query_selector('input[placeholder="请选择"]')
        if dept_input:
            dept_input.click()
            time.sleep(0.5)
            
            # 尝试选择部门
            dept_option = page.query_selector(f'li:has-text("{department}"), .el-select-dropdown__item:has-text("{department}")')
            if dept_option and dept_option.is_visible():
                dept_option.click()
                print(f"✅ {department}")
                time.sleep(0.3)
            else:
                print(f"⚠️ 未找到'{department}'，跳过")
                page.keyboard.press('Escape')
        else:
            print("⚠️ 无部门选择框")
        
        # 5. 点击保存
        print("    点击保存...", end="")
        save_btn = page.query_selector('button:has-text("保存")')
        if save_btn and save_btn.is_visible():
            save_btn.click()
            print("✅")
            time.sleep(1.5)
            
            # 检查结果
            success_msg = page.query_selector('.el-message--success')
            error_msg = page.query_selector('.el-message--error')
            
            if success_msg and success_msg.is_visible():
                print(f"    📢 {success_msg.inner_text()}")
                return True
            elif error_msg and error_msg.is_visible():
                print(f"    ❌ 错误: {error_msg.inner_text()}")
                return False
            else:
                print("    ✅ 完成")
                return True
        else:
            print("❌ 未找到保存按钮")
            return False
        
    except Exception as e:
        print(f"\n    ❌ 异常: {e}")
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v5")
    print("=" * 60)
    
    # 读取数据
    employees = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(row)
    
    print(f"\n📋 数据: {len(employees)} 人")
    for emp in employees:
        print(f"   - {emp['姓名']}")
    
    # 连接浏览器
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        print("\n✅ 连接浏览器")
        
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
        print("✅ 找到员工页面\n")
        
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
        
        # 查看结果
        print("\n\n🔄 刷新查看结果...")
        target_page.reload()
        time.sleep(2)
        target_page.screenshot(path='/tmp/result_v5.png', full_page=True)
        
        print("\n" + "=" * 60)
        print(f"📊 完成: 成功 {success} / 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
