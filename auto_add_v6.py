#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - v6 直接填写版
当前页面已经是添加新员工表单
"""

from playwright.sync_api import sync_playwright
import csv
import time

CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def add_employee_direct(page, name, phone, department):
    """直接在表单中填写"""
    print(f"\n  添加: {name} | {phone} | {department}")
    
    try:
        # 1. 填写手机
        print("    填写手机...", end="")
        phone_input = page.query_selector('input[placeholder="请输入员工手机"]')
        if phone_input:
            phone_input.fill(phone)
            print(f"✅ {phone}")
        else:
            print("❌ 未找到")
            return False
        
        # 2. 填写姓名
        print("    填写姓名...", end="")
        name_input = page.query_selector('input[placeholder="请输入员工姓名"]')
        if name_input:
            name_input.fill(name)
            print(f"✅ {name}")
        else:
            print("❌ 未找到")
            return False
        
        # 3. 选择部门
        print("    选择部门...", end="")
        dept_select = page.query_selector('input[placeholder="请选择"]')
        if dept_select:
            dept_select.click()
            time.sleep(0.5)
            
            # 找部门选项
            option = page.query_selector(f'.el-select-dropdown__item:has-text("{department}")')
            if option and option.is_visible():
                option.click()
                print(f"✅ {department}")
                time.sleep(0.3)
            else:
                print(f"⚠️ 未找到'{department}'，跳过")
                page.keyboard.press('Escape')
        else:
            print("⚠️ 无部门选择框")
        
        # 4. 点击保存并继续添加
        print("    点击保存...", end="")
        save_btn = page.query_selector('button:has-text("保存并继续添加")')
        if save_btn and save_btn.is_visible():
            save_btn.click()
            print("✅")
            time.sleep(2)
            
            # 检查提示
            msg = page.query_selector('.el-message--success, .el-message--error')
            if msg and msg.is_visible():
                print(f"    📢 {msg.inner_text()}")
            
            return True
        else:
            print("❌ 未找到保存按钮")
            return False
        
    except Exception as e:
        print(f"\n    ❌ 错误: {e}")
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v6")
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
                if "uf-tree.com" in page.url:
                    target_page = page
                    break
            if target_page:
                break
        
        if not target_page:
            print("❌ 未找到页面")
            return
        
        target_page.bring_to_front()
        print(f"✅ 当前页面: {target_page.url}\n")
        
        # 检查是否在添加员工页面
        title = target_page.query_selector('.title')
        if title:
            title_text = title.inner_text()
            print(f"📄 当前界面: {title_text}")
            
            if "添加新员工" not in title_text:
                print("⚠️ 不在添加员工页面，请先点击'添加员工'按钮")
                browser.close()
                return
        
        # 添加员工
        success = fail = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}]", end="")
            if add_employee_direct(target_page, emp['姓名'], emp['手机号'], emp['部门']):
                success += 1
            else:
                fail += 1
            
            if i < len(employees):
                time.sleep(1)
        
        print("\n" + "=" * 60)
        print(f"📊 完成: 成功 {success} / 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
