#!/usr/bin/env python3
"""
财税通员工批量添加工具
用法: python caishui_add_staff.py <excel_file_path>
"""

import sys
import pandas as pd
from playwright.sync_api import sync_playwright, TimeoutError
import time

# 配置
DEBUG_PORT = "http://localhost:9222"
BASE_URL = "https://cst.uf-tree.com"

def log(msg):
    """打印日志"""
    print(f"[CaishuiStaff] {msg}")

def add_staff_from_excel(excel_path):
    """从Excel批量添加员工"""
    
    # 读取Excel
    try:
        df = pd.read_excel(excel_path)
        log(f"读取到 {len(df)} 个员工")
    except Exception as e:
        log(f"❌ 读取Excel失败: {e}")
        return
    
    # 显示预览
    print("\n" + "="*60)
    print("📋 员工数据预览")
    print("="*60)
    for idx, row in df.iterrows():
        name = str(row['姓名']).strip()
        phone = str(row['手机号']).strip()[:11]
        dept = str(row['门店']).strip()
        print(f"{idx+1:2d}. {name:8s} | {phone} | {dept}")
    
    print("\n" + "="*60)
    confirm = input("确认添加以上员工? (y/n): ")
    if confirm.lower() != 'y':
        log("已取消")
        return
    
    # 连接浏览器
    log("连接浏览器...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(DEBUG_PORT)
        except Exception as e:
            log(f"❌ 连接浏览器失败: {e}")
            log("请确保浏览器已启动调试模式: --remote-debugging-port=9222")
            return
        
        success_count = 0
        failed_count = 0
        
        for idx, row in df.iterrows():
            name = str(row['姓名']).strip()
            phone = str(row['手机号']).strip()[:11]
            dept = str(row['门店']).strip()
            
            print(f"\n[{idx+1}/{len(df)}] 添加: {name}")
            
            # 获取页面
            page = None
            for ctx in browser.contexts:
                for pg in ctx.pages:
                    if "uf-tree.com" in pg.url:
                        page = pg
                        break
                if page:
                    break
            
            if not page:
                print("  ❌ 未找到页面")
                failed_count += 1
                continue
            
            page.bring_to_front()
            
            try:
                # 1. 进入员工管理
                page.goto(f"{BASE_URL}/company/staff", timeout=10000)
                time.sleep(2)
                
                # 2. 点击添加员工
                page.click('button:has-text("添加员工")', timeout=5000)
                time.sleep(1)
                
                # 3. 选择直接添加
                page.click('.el-dropdown-menu__item:has-text("直接添加")', timeout=5000)
                time.sleep(2)
                
                # 4. 填写表单（使用正确的placeholder）
                page.fill('input[placeholder="请输入员工姓名"]', name, timeout=5000)
                page.fill('input[placeholder="请输入员工手机"]', phone, timeout=5000)
                
                # 5. 选择部门
                page.click('.vue-treeselect__control', timeout=5000)
                time.sleep(0.5)
                page.click(f'.vue-treeselect__option:has-text("{dept}")', timeout=5000)
                time.sleep(0.5)
                
                # 6. 点击保存并继续添加
                page.click('button:has-text("保存并继续添加")', timeout=5000)
                time.sleep(3)
                
                # 检查是否有错误
                error_msg = page.query_selector('.el-message--error')
                if error_msg:
                    error_text = error_msg.inner_text()
                    print(f"  ❌ 错误: {error_text[:50]}")
                    failed_count += 1
                else:
                    print(f"  ✅ 成功")
                    success_count += 1
                
            except TimeoutError:
                print(f"  ⏱️ 超时")
                failed_count += 1
            except Exception as e:
                print(f"  ❌ 失败: {e}")
                failed_count += 1
        
        # 统计
        print("\n" + "="*60)
        print("📊 添加完成")
        print("="*60)
        print(f"成功: {success_count}/{len(df)}")
        print(f"失败: {failed_count}/{len(df)}")
        
        # 验证
        if success_count > 0:
            print("\n🔍 验证结果...")
            page.goto(f"{BASE_URL}/company/staff")
            time.sleep(3)
            
            text = page.evaluate("() => document.body.innerText")
            found = 0
            for idx, row in df.iterrows():
                name = str(row['姓名']).strip()
                if name in text:
                    found += 1
            
            print(f"验证通过: {found}/{len(df)}")
        
        browser.close()
        log("完成！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python caishui_add_staff.py <excel_file_path>")
        print("示例: python caishui_add_staff.py /Users/tang/Desktop/employees.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    add_staff_from_excel(excel_file)
