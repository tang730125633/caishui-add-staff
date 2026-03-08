#!/usr/bin/env python3
"""
财税通修改员工部门脚本
搜索员工 -> 编辑 -> 修改部门 -> 保存
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
                # 检查是否是列表页（不是添加页）
                title = page.query_selector(".title")
                if title:
                    title_text = title.inner_text()
                    if "员工" in title_text and "添加" not in title_text:
                        return page
                else:
                    # 通过页面特征判断
                    add_btn = page.query_selector('button:has-text("添加员工")')
                    if add_btn:
                        return page
    return None

def search_and_edit_employee(page, name, new_dept):
    """搜索员工并修改部门"""
    print(f"\n  修改: {name} -> {new_dept}")
    
    try:
        # 1. 在搜索框输入姓名
        print("    搜索员工...", end="")
        search_input = page.query_selector('input[placeholder*="手机或姓名或部门"]')
        if not search_input:
            print("❌ 未找到搜索框")
            return False
        
        # 清空并输入
        search_input.fill("")
        time.sleep(0.3)
        search_input.fill(name)
        time.sleep(0.5)
        
        # 按回车搜索
        search_input.press('Enter')
        time.sleep(2)
        print("✅")
        
        # 2. 查找员工行并点击编辑
        print("    查找编辑按钮...", end="")
        
        # 方法1: 找包含员工姓名的行，然后找编辑按钮
        rows = page.query_selector_all('tr, .el-table__row')
        found = False
        
        for row in rows:
            try:
                row_text = row.inner_text()
                if name in row_text:
                    # 在这一行找编辑按钮
                    edit_btn = row.query_selector('button:has-text("编辑"), .el-button--text, [title="编辑"]')
                    if edit_btn and edit_btn.is_visible():
                        edit_btn.click()
                        print("✅")
                        found = True
                        time.sleep(2)
                        break
            except:
                pass
        
        if not found:
            print("❌ 未找到编辑按钮")
            return False
        
        # 3. 修改部门
        print(f"    修改部门为 {new_dept}...", end="")
        
        # 点击部门选择框（vue-treeselect）
        treeselect = page.query_selector('.vue-treeselect__input, .vue-treeselect__control')
        if treeselect:
            treeselect.click()
            time.sleep(1)
            
            # 查找部门选项
            option = page.query_selector(f'.vue-treeselect__option:has-text("{new_dept}"), .vue-treeselect__label:has-text("{new_dept}")')
            if option and option.is_visible():
                option.click()
                print("✅")
                time.sleep(0.5)
            else:
                print(f"⚠️ 未找到部门 {new_dept}")
                page.keyboard.press('Escape')
        else:
            print("⚠️ 未找到部门选择框")
        
        # 4. 保存
        print("    保存修改...", end="")
        save_btn = page.query_selector('button:has-text("保存"), button:has-text("确定")')
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
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🤖 财税通修改员工部门脚本")
    print("=" * 60)
    
    # 读取数据
    employees = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employees.append(row)
    
    print(f"\n📋 需要修改的员工: {len(employees)} 人")
    for emp in employees:
        print(f"   - {emp['姓名']} -> {emp['部门']}")
    
    # 连接浏览器
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        print("\n✅ 连接浏览器")
        
        # 查找员工列表页面
        target_page = find_staff_list_page(browser)
        
        if not target_page:
            print("❌ 未找到员工列表页面")
            print("💡 请手动在Comet浏览器中打开员工管理页面")
            browser.close()
            return
        
        target_page.bring_to_front()
        print(f"✅ 找到员工列表页面\n")
        
        # 确保在列表页
        target_page.goto("https://cst.uf-tree.com/company/staff")
        time.sleep(2)
        
        # 修改部门
        success = fail = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}]", end="")
            if search_and_edit_employee(target_page, emp['姓名'], emp['部门']):
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
