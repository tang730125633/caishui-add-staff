#!/usr/bin/env python3
"""
财税通自动添加员工脚本 - 改进版
从 CSV 文件读取员工信息，自动添加到系统
"""

from playwright.sync_api import sync_playwright
import csv
import time

# 配置文件
CSV_FILE = "/Users/tang/Desktop/caishui_bot/员工数据.csv"
DEBUG_PORT = "http://localhost:9222"

def add_employee_v2(page, name, phone, department):
    """添加单个员工 - 改进版"""
    print(f"\n  正在添加: {name} ({phone}) - {department}")
    
    try:
        # 1. 点击"添加"按钮（右上角蓝色按钮）
        print("    🔍 查找添加按钮...")
        
        # 根据页面结构，尝试多种选择器
        add_btn = None
        selectors = [
            'button:has-text("添加")',
            'button.el-button--primary',
            '.add-btn',
            'button i.el-icon-plus',  # 带+图标的按钮
        ]
        
        for selector in selectors:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible():
                    add_btn = btn
                    print(f"    ✅ 找到添加按钮: {selector}")
                    break
            except:
                continue
        
        if not add_btn:
            # 尝试找所有按钮，看哪个包含"添加"
            buttons = page.query_selector_all('button')
            for btn in buttons:
                try:
                    text = btn.inner_text()
                    if '添加' in text and btn.is_visible():
                        add_btn = btn
                        print(f"    ✅ 找到添加按钮(文字匹配): {text}")
                        break
                except:
                    continue
        
        if not add_btn:
            print("    ❌ 未找到添加按钮")
            return False
        
        # 点击添加按钮
        add_btn.click()
        print("    ✅ 点击添加按钮")
        time.sleep(1.5)  # 等待弹窗动画
        
        # 2. 填写表单
        print("    📝 填写表单...")
        
        # 获取所有可见的输入框
        inputs = page.query_selector_all('input')
        print(f"    找到 {len(inputs)} 个输入框")
        
        text_inputs = []
        for inp in inputs:
            try:
                if inp.is_visible():
                    input_type = inp.get_attribute('type') or 'text'
                    placeholder = inp.get_attribute('placeholder') or ''
                    text_inputs.append((inp, input_type, placeholder))
            except:
                continue
        
        print(f"    可见输入框: {len(text_inputs)} 个")
        for i, (inp, typ, ph) in enumerate(text_inputs):
            print(f"      [{i}] type={typ}, placeholder={ph}")
        
        # 填写姓名（第一个文本输入框）
        name_filled = False
        for inp, typ, ph in text_inputs:
            if typ == 'text' and not name_filled:
                try:
                    inp.fill(name)
                    print(f"    ✅ 填写姓名: {name}")
                    name_filled = True
                    break
                except:
                    continue
        
        # 填写手机号（找tel类型或第二个text输入框）
        phone_filled = False
        for inp, typ, ph in text_inputs:
            if typ == 'tel' and not phone_filled:
                try:
                    inp.fill(phone)
                    print(f"    ✅ 填写手机号: {phone}")
                    phone_filled = True
                    break
                except:
                    continue
        
        if not phone_filled:
            # 找第二个text输入框
            text_count = 0
            for inp, typ, ph in text_inputs:
                if typ == 'text':
                    text_count += 1
                    if text_count == 2 and not phone_filled:
                        try:
                            inp.fill(phone)
                            print(f"    ✅ 填写手机号(第二个文本框): {phone}")
                            phone_filled = True
                            break
                        except:
                            continue
        
        # 3. 选择部门
        print("    🏢 选择部门...")
        
        # 找部门下拉框（通常是 readonly 或带箭头的 input）
        dept_clicked = False
        
        # 尝试点击所有带 placeholder 包含"部门"的 input
        for inp, typ, ph in text_inputs:
            if '部门' in ph:
                try:
                    inp.click()
                    print(f"    ✅ 点击部门选择框")
                    dept_clicked = True
                    time.sleep(0.8)
                    break
                except:
                    continue
        
        if not dept_clicked:
            # 尝试点击 .el-select（Element UI 下拉框）
            selects = page.query_selector_all('.el-select')
            for sel in selects:
                try:
                    if sel.is_visible():
                        sel.click()
                        print(f"    ✅ 点击 el-select 下拉框")
                        dept_clicked = True
                        time.sleep(0.8)
                        break
                except:
                    continue
        
        if dept_clicked:
            # 在下拉列表中找部门
            time.sleep(0.5)
            
            # 尝试多种选择器找部门选项
            dept_options = [
                f'.el-select-dropdown__item:has-text("{department}")',
                f'.el-scrollbar__view .el-select-dropdown__item:has-text("{department}")',
                f'li:has-text("{department}")',
                f'xpath=//li[contains(text(), "{department}")]',
            ]
            
            dept_selected = False
            for opt_selector in dept_options:
                try:
                    option = page.query_selector(opt_selector)
                    if option and option.is_visible():
                        option.click()
                        print(f"    ✅ 选择部门: {department}")
                        dept_selected = True
                        time.sleep(0.5)
                        break
                except Exception as e:
                    continue
            
            if not dept_selected:
                print(f"    ⚠️ 未找到部门选项: {department}")
                # 打印当前可见的所有选项
                all_options = page.query_selector_all('.el-select-dropdown__item')
                print(f"    当前可见选项: {len(all_options)} 个")
                for opt in all_options[:5]:  # 只显示前5个
                    try:
                        text = opt.inner_text()
                        print(f"      - {text}")
                    except:
                        pass
        else:
            print("    ⚠️ 未找到部门选择框")
        
        # 4. 点击确定/保存按钮
        print("    💾 点击保存...")
        
        save_btn = None
        save_selectors = [
            '.el-dialog__footer button.el-button--primary',  # 弹窗底部的主按钮
            '.el-dialog__footer button:has-text("确")',  # 确定/确认
            '.el-dialog__footer button:has-text("保")',  # 保存
            'button:has-text("确定")',
            'button:has-text("确认")',
            'button:has-text("保存")',
            '.el-button--primary',
        ]
        
        for selector in save_selectors:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible():
                    save_btn = btn
                    text = btn.inner_text()
                    print(f"    ✅ 找到保存按钮: {text}")
                    break
            except:
                continue
        
        if save_btn:
            save_btn.click()
            print("    ✅ 点击保存按钮")
            time.sleep(2)  # 等待保存完成
            
            # 检查是否有成功提示
            try:
                success_msg = page.query_selector('.el-message--success')
                if success_msg and success_msg.is_visible():
                    msg_text = success_msg.inner_text()
                    print(f"    ✅ 成功提示: {msg_text}")
            except:
                pass
            
            print(f"    ✅ 员工 {name} 添加完成")
            return True
        else:
            print("    ❌ 未找到保存按钮")
            # 截图看看当前状态
            try:
                page.screenshot(path=f'/tmp/error_{name}.png')
                print(f"    📸 已保存错误截图: /tmp/error_{name}.png")
            except:
                pass
            return False
        
    except Exception as e:
        print(f"    ❌ 添加失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🤖 财税通自动添加员工脚本 v2")
    print("=" * 60)
    
    # 读取员工数据
    print(f"\n📁 读取员工数据: {CSV_FILE}")
    employees = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                employees.append(row)
        print(f"✅ 读取到 {len(employees)} 条员工数据")
        for emp in employees:
            print(f"   - {emp['姓名']} | {emp['手机号']} | {emp['部门']}")
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
            browser.close()
            return
        
        print(f"✅ 找到目标页面")
        target_page.bring_to_front()
        
        # 开始添加员工
        print("\n" + "=" * 60)
        print("🚀 开始添加员工")
        print("=" * 60)
        
        success_count = 0
        fail_count = 0
        
        for i, emp in enumerate(employees, 1):
            print(f"\n[{i}/{len(employees)}] ", end="")
            result = add_employee_v2(
                target_page,
                emp['姓名'],
                emp['手机号'],
                emp['部门']
            )
            
            if result:
                success_count += 1
            else:
                fail_count += 1
            
            # 添加间隔
            if i < len(employees):
                wait_time = 2
                print(f"\n  ⏳ 等待 {wait_time} 秒...")
                time.sleep(wait_time)
        
        # 总结
        print("\n" + "=" * 60)
        print("📊 执行结果")
        print("=" * 60)
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"📈 总计: {len(employees)}")
        
        browser.close()
        print("\n🏁 脚本执行完毕!")

if __name__ == "__main__":
    main()
