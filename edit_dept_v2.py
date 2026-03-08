#!/usr/bin/env python3
"""
财税通修改员工部门脚本 v2
点击员工姓名进入编辑页面
"""

from playwright.sync_api import sync_playwright
import csv
import time

CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def find_staff_list_page(browser):
    """查找员工列表页面"""
    for ctx in browser.contexts:
        for page in ctx.pages:
            if "uf-tree.com" in page.url and "staff" in page.url:
                add_btn = page.query_selector('button:has-text("添加员工")')
                if add_btn:
                    return page
    return None

def edit_employee_dept(page, name, new_dept):
    """编辑员工部门"""
    print(f"\n  修改: {name} -> {new_dept}")
    
    try:
        # 1. 搜索员工
        print("    搜索...", end="")
        search_input = page.query_selector('input[placeholder*="手机或姓名或部门"]')
        if search_input:
            search_input.fill("")
            time.sleep(0.3)
            search_input.fill(name)
            time.sleep(0.5)
            search_input.press('Enter')
            time.sleep(2)
        print("✅")
        
        # 2. 点击员工姓名进入编辑
        print("    点击姓名进入编辑...", end="")
        
        # 方法1: 直接通过文字查找链接
        name_link = page.query_selector(f'a:has-text("{name}"), td:has-text("{name}")')
        if name_link and name_link.is_visible():
            # 如果是td，找里面的链接或点击td本身
            link_in_td = name_link.query_selector('a')
            if link_in_td:
                link_in_td.click()
            else:
                name_link.click()
            print("✅")
            time.sleep(2)
        else:
            print("❌ 未找到")
            return False
        
        # 3. 检查是否进入编辑页面
        title = page.query_selector('.title')
        if title:
            print(f"    当前页面: {title.inner_text()}")
        
        # 4. 修改部门
        print(f"    修改部门...", end="")
        
        # 点击部门选择框
        treeselect = page.query_selector('.vue-treeselect__control, .vue-treeselect__input')
        if treeselect:
            treeselect.click()
            time.sleep(1)
            
            # 选择部门
            option = page.query_selector(f'.vue-treeselect__option:has-text("{new_dept}"), .vue-treeselect__label:has-text("{new_dept}")')
            if option and option.is_visible():
                option.click()
                print("✅")
                time.sleep(0.5)
            else:
                print(f"⚠️ 未找到 {new_dept}")
                page.keyboard.press('Escape')
        else:
            print("⚠️ 无部门选择框")
        
        # 5. 保存
        print("    保存...", end="")
        save_btn = page.query_selector('button:has-text("保存"), button:has-text("确定")')
        if save_btn and save_btn.is_visible():
            save_btn.click()
            print("✅")
            time.sleep(2)
            
            msg = page.query_selector('.el-message--success')
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
    print("🤖 财税通修改员工部门脚本 v2")
    print("=" * 60)
    
    # 读取数据
    employees = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(row)
    
    print(f"\n📋 需要修改: {len(employees)} 人")
    for emp in employees:
        print(f"   - {emp['姓名']} -> {emp['部门']}")
    
    # 连接浏览器
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        print("\n✅ 连接浏览器")
        
        target_page = find_staff_list_page(browser)
        
        if not target_page:
            print("❌ 未找到员工列表页面")
            browser.close()
            return
        
        target_page.bring_to_front()
        print("✅ 找到页面\n")
        
        # 修改部门
        success = fail = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}]", end="")
            if edit_employee_dept(target_page, emp['姓名'], emp['部门']):
                success += 1
            else:
                fail += 1
            
            # 返回列表页
            target_page.goto("https://cst.uf-tree.com/company/staff")
            time.sleep(2)
            
            if i < len(employees):
                time.sleep(1)
        
        print("\n" + "=" * 60)
        print(f"📊 完成: 成功 {success} / 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
