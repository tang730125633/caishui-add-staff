# 财税通员工批量添加工具 (Caishui Staff Auto-Add)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🚀 **自动化批量添加员工到财税通（凯旋创智）系统**，支持从Excel/CSV读取数据并自动填写表单。

---

## 📋 目录

- [功能特性](#功能特性)
- [系统要求](#系统要求)
- [安装指南](#安装指南)
- [快速开始](#快速开始)
- [详细使用说明](#详细使用说明)
- [常见问题](#常见问题)
- [故障排除](#故障排除)

---

## ✨ 功能特性

- ✅ **Excel/CSV批量导入** - 自动读取员工数据
- ✅ **智能字段映射** - 自动识别姓名、手机号、部门
- ✅ **自动部门选择** - 支持vue-treeselect树形组件
- ✅ **批量添加模式** - 支持"保存并继续添加"
- ✅ **错误重试机制** - 自动处理超时和异常
- ✅ **结果验证** - 自动验证添加结果
- ✅ **详细日志** - 实时显示添加进度

---

## 💻 系统要求

### 必需软件

| 软件 | 版本 | 说明 |
|------|------|------|
| Python | 3.8+ | 编程语言运行环境 |
| Chrome/Edge | 最新版 | 浏览器自动化 |
| Git | 任意版本 | 代码管理（可选） |

### 支持的操作系统

- ✅ macOS 10.15+
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+)

---

## 📦 安装指南

### 步骤 1: 克隆仓库

```bash
git clone https://github.com/yourusername/caishui-add-staff.git
cd caishui-add-staff
```

### 步骤 2: 安装Python依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 3: 安装浏览器

```bash
# 安装Playwright浏览器
playwright install chromium
```

### 步骤 4: 启动浏览器调试模式

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-dev-profile"
```

**Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\temp\chrome-dev-profile"
```

**或使用Microsoft Edge:**

```bash
# macOS
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge \
  --remote-debugging-port=9222

# Windows
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" ^
  --remote-debugging-port=9222
```

⚠️ **重要:** 浏览器窗口不要关闭，保持运行状态！

### 步骤 5: 登录财税通系统

1. 在启动的浏览器中访问: https://cst.uf-tree.com
2. 使用您的账号登录
3. 选择企业进入系统
4. 保持浏览器窗口打开

---

## 🚀 快速开始

### 1. 准备Excel文件

创建 `employees.xlsx` 或 `employees.csv`:

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 测试门店1 |
| 李四 | 13800138001 | 测试门店2 |
| 王五 | 13800138002 | 测试门店3 |

⚠️ **注意:**
- 手机号必须是 **11位数字**
- 不要包含空格、横线或其他字符
- 门店名称必须与系统中的一致

### 2. 运行脚本

```bash
python caishui_add_staff.py /path/to/employees.xlsx
```

### 3. 查看结果

脚本会自动：
- 显示添加进度
- 统计成功/失败数量
- 验证添加结果

---

## 📖 详细使用说明

### 命令行参数

```bash
python caishui_add_staff.py <excel_or_csv_file> [options]

Options:
  --debug-port PORT    浏览器调试端口 (默认: 9222)
  --timeout SECONDS    操作超时时间 (默认: 10)
  --verify             添加后验证结果
```

### Python API 调用

```python
from caishui_staff import CaishuiStaffManager

# 初始化管理器
manager = CaishuiStaffManager(debug_port="http://localhost:9222")

# 连接浏览器
manager.connect()

# 批量添加
results = manager.add_from_excel("/path/to/employees.xlsx")

# 查看结果
print(f"成功: {results['success']}")
print(f"失败: {results['failed']}")

# 关闭连接
manager.close()
```

### 在Claude Code/OpenClaw中使用

```bash
# 使用Skill命令
@caishui-add-staff /path/to/employees.xlsx
```

---

## ⚙️ 配置文件

### 环境变量

```bash
# 设置浏览器调试端口
export CAISHUI_DEBUG_PORT=9222

# 设置操作超时时间（秒）
export CAISHUI_TIMEOUT=10

# 设置日志级别
export CAISHUI_LOG_LEVEL=INFO
```

### 配置文件示例 (`config.json`)

```json
{
  "debug_port": "http://localhost:9222",
  "base_url": "https://cst.uf-tree.com",
  "timeout": 10000,
  "retry_count": 3,
  "headless": false
}
```

---

## ❓ 常见问题

### Q1: 提示"连接浏览器失败"

**原因:** 浏览器未启动调试模式

**解决:**
```bash
# 确保使用 --remote-debugging-port=9222 启动浏览器
chrome --remote-debugging-port=9222
```

### Q2: 点击"添加员工"后跳转到选择企业页面

**原因:** 点到了"添加子部门"而不是"直接添加"

**解决:**
脚本会自动选择正确的选项。如果仍然跳转，请检查：
- 浏览器是否已登录
- 是否有权限添加员工

### Q3: 手机号保存失败或提示格式错误

**原因:** 手机号格式不正确

**解决:**
- 确保是11位数字
- 不要包含空格、+86前缀或其他字符
- Excel中设置为文本格式，避免科学计数法

### Q4: 部门选择失败

**原因:** 部门名称不匹配

**解决:**
- 检查Excel中的部门名称是否与系统完全一致
- 注意空格和特殊字符

### Q5: 添加成功但验证时找不到员工

**原因:** 系统有延迟或分页显示

**解决:**
- 等待几秒后刷新页面
- 使用搜索功能查找
- 检查是否添加了筛选条件

---

## 🔧 故障排除

### 调试模式

启用详细日志：
```bash
python caishui_add_staff.py employees.xlsx --verbose
```

### 截图调试

脚本会自动保存截图到 `/tmp/` 目录：
- `before_save.png` - 填写表单后
- `after_save.png` - 点击保存后

### 检查元素

使用Playwright Inspector：
```bash
PWDEBUG=1 python caishui_add_staff.py employees.xlsx
```

---

## 🛡️ 安全提示

1. **不要分享登录凭据** - 每个人应该使用自己的账号
2. **定期更换密码** - 确保账号安全
3. **在受信任的网络环境下使用** - 避免在公共WiFi下操作
4. **备份数据** - 操作前备份重要数据

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 提交Issue

请包含以下信息：
- 操作系统和版本
- Python版本
- 错误信息和日志
- 复现步骤

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/caishui-add-staff.git
cd caishui-add-staff

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/
```

---

## 📝 更新日志

### v1.0.0 (2024-03-07)
- 🎉 初始版本发布
- ✅ 支持Excel/CSV批量导入
- ✅ 支持自动部门选择
- ✅ 添加错误重试机制
- ✅ 添加结果验证功能

---

## 📄 许可证

[MIT License](LICENSE)

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 👨‍💻 作者

- **开发者** - [Your Name](https://github.com/yourusername)
- **Email** - your.email@example.com

---

## 🙏 致谢

- [Playwright](https://playwright.dev/python/) - 浏览器自动化框架
- [Pandas](https://pandas.pydata.org/) - 数据处理库
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel文件处理

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues: [https://github.com/yourusername/caishui-add-staff/issues](https://github.com/yourusername/caishui-add-staff/issues)
- Email: your.email@example.com

---

**如果这个项目对你有帮助，请给个 ⭐ Star！**
