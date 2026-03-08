#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - v3 修正版
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
        print("    🔍 查找'添加员工'按钮...")
        
        # 精确匹配"添加员工"文字
        add_btn = page.query_selector('button:has-text("添加员工")')
        
        if not add_btn or not add_btn.is_visible():
            # 备选：找包含 el-icon-plus 的按钮
            buttons = page.query_selector_all('button')
            for btn in buttons:
                try:
                    text = btn.inner_text()
                    if '添加员工' in text and btn.is_visible():
                        add_btn = btn
                        break
                except:
                    continue
        
        if not add_btn:
            print("    ❌ 未找到'添加员工'按钮")
            return False
        
        add_btn.click()
        print("    ✅ 点击'添加员工'按钮")
        time.sleep(2)  # 等待弹窗出现
        
        # 2. 截图看弹窗
        page.screenshot(path=f'/tmp/dialog_{name}.png')
        
        # 3. 填写表单 - 找弹窗中的输入框
        print("    📝 填写表单...")
        
        # 获取弹窗中的所有输入框
        dialog = page.query_selector('.el-dialog, .el-dialog__wrapper, [role="dialog"]')
        if dialog:
            inputs = dialog.query_selector_all('input')
            print(f"    弹窗中找到 {len(inputs)} 个输入框")
        else:
            inputs = page.query_selector_all('.el-dialog input, .el-dialog__wrapper input')
            print(f"    页面中找到 {len(inputs)} 个输入框（在弹窗中）")
        
        # 显示输入框信息
        for i, inp in enumerate(inputs):
            try:
                if inp.is_visible():
                    placeholder = inp.get_attribute('placeholder') or ''
                    input_type = inp.get_attribute('type') or 'text'
                    print(f"      [{i}] type={input_type}, placeholder='{placeholder}'")
            except:
                pass
        
        # 填写姓名和手机号
        filled_count = 0
        for inp in inputs:
            try:
                if not inp.is_visible():
                    continue
                    
                placeholder = inp.get_attribute('placeholder') or ''
                input_type = inp.get_attribute('type') or 'text'
                
                # 根据 placeholder 判断填写内容
                if '姓名' in placeholder or ('name' in placeholder.lower() and filled_count == 0):
                    inp.fill(name)
                    print(f"    ✅ 填写姓名: {name}")
                    filled_count += 1
                    
                elif '手机' in placeholder or '电话' in placeholder or input_type == 'tel':
                    inp.fill(phone)
                    print(f"    ✅ 填写手机号: {phone}")
                    filled_count += 1
                    
            except Exception as e:
                print(f"    ⚠️ 填写出错: {e}")
        
        # 如果没有根据placeholder找到，按顺序填前两个
        if filled_count < 2:
            visible_inputs = [inp for inp in inputs if inp.is_visible()]
            if len(visible_inputs) >= 1 and filled_count == 0:
                try:
                    visible_inputs[0].fill(name)
                    print(f"    ✅ 填写姓名(备用): {name}")
                    filled_count += 1
                except:
                    pass
            if len(visible_inputs) >= 2 and filled_count == 1:
                try:
                    visible_inputs[1].fill(phone)
                    print(f"    ✅ 填写手机号(备用): {phone}")
                    filled_count += 1
                except:
                    pass
        
        # 4. 选择部门
        print("    🏢 选择部门...")
        
        # 找部门选择框
        dept_selectors = [
            'input[placeholder*="部门"]',
            '.el-select input',
        ]
        
        dept_clicked = False
        for selector in dept_selectors:
            try:
                dept_input = page.query_selector(selector)
                if dept_input and dept_input.is_visible():
                    dept_input.click()
                    print(f"    ✅ 点击部门选择框")
                    dept_clicked = True
                    time.sleep(1)
                    break
            except:
                continue
        
        if dept_clicked:
            # 在下拉列表中选择部门
            option_selectors = [
                f'.el-select-dropdown__item:has-text("{department}")',
                f'li:has-text("{department}")',
                f'xpath=//li[contains(text(), "{department}")]',
            ]
            
            for opt_sel in option_selectors:
                try:
                    option = page.query_selector(opt_sel)
                    if option and option.is_visible():
                        option.click()
                        print(f"    ✅ 选择部门: {department}")
                        time.sleep(0.5)
                        break
                except:
                    continue
            else:
                print(f"    ⚠️ 未找到部门: {department}")
                # ESC关闭下拉
                page.keyboard.press('Escape')
        
        # 5. 点击保存
        print("    💾 点击保存...")
        
        save_selectors = [
            '.el-dialog__footer button.el-button--primary',
            '.el-dialog button:has-text("保存")',
            '.el-dialog button:has-text("确定")',
            'button:has-text("保存")',
            'button:has-text("确定")',
        ]
        
        save_clicked = False
        for selector in save_selectors:
            try:
                save_btn = page.query_selector(selector)
                if save_btn and save_btn.is_visible():
                    text = save_btn.inner_text()
                    save_btn.click()
                    print(f"    ✅ 点击保存按钮: {text}")
                    save_clicked = True
                    break
            except:
                continue
        
        if not save_clicked:
            print("    ❌ 未找到保存按钮")
            page.screenshot(path=f'/tmp/save_error_{name}.png')
            return False
        
        # 等待保存完成
        time.sleep(2)
        
        # 检查成功提示
        try:
            success_tip = page.query_selector('.el-message--success')
            if success_tip and success_tip.is_visible():
                msg = success_tip.inner_text()
                print(f"    ✅ 成功提示: {msg}")
        except:
            pass
        
        print(f"    ✅ 员工 {name} 添加完成")
        return True
        
    except Exception as e:
        print(f"    ❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v3")
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
        
        print("\n" + "=" * 60)
        print(f"📊 结果: 成功 {success}, 失败 {fail}")
        print("=" * 60)
        
        browser.close()

if __name__ == "__main__":
    main()
