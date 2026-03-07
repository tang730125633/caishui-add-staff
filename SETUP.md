# 详细安装教程

本教程将指导您从零开始安装和配置财税通员工批量添加工具。

---

## 📋 目录

1. [环境检查](#1-环境检查)
2. [安装Python](#2-安装python)
3. [安装依赖](#3-安装依赖)
4. [安装浏览器](#4-安装浏览器)
5. [配置浏览器](#5-配置浏览器)
6. [登录系统](#6-登录系统)
7. [测试运行](#7-测试运行)

---

## 1. 环境检查

### 检查Python版本

```bash
# macOS/Linux
python3 --version

# Windows
python --version
```

要求：Python 3.8 或更高版本

如果未安装，请继续下一步。

---

## 2. 安装Python

### macOS

**方式1: 使用Homebrew（推荐）**
```bash
# 安装Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装Python
brew install python
```

**方式2: 从官网下载**
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11+
3. 双击安装包，按提示安装

### Windows

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11+ Windows installer
3. 运行安装程序
4. **重要**: 勾选 "Add Python to PATH"
5. 点击 "Install Now"

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

---

## 3. 安装依赖

### 步骤1: 下载项目代码

```bash
# 使用git克隆（需要安装git）
git clone https://github.com/yourusername/caishui-add-staff.git
cd caishui-add-staff

# 或者下载ZIP文件并解压
# 1. 访问 https://github.com/yourusername/caishui-add-staff
# 2. 点击 "Code" → "Download ZIP"
# 3. 解压到任意目录
```

### 步骤2: 创建虚拟环境

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

您应该看到命令行前面出现了 `(venv)` 标识。

### 步骤3: 安装Python包

```bash
pip install -r requirements.txt
```

这将安装：
- playwright (浏览器自动化)
- pandas (数据处理)
- openpyxl (Excel文件读取)

---

## 4. 安装浏览器

### 安装Playwright浏览器

```bash
playwright install chromium
```

这将下载：
- Chromium 浏览器 (~100MB)
- 可能需要几分钟时间

**如果遇到网络问题：**

```bash
# 使用国内镜像（中国用户）
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright playwright install chromium
```

---

## 5. 配置浏览器

### 启动浏览器调试模式

**macOS:**

```bash
# 方法1: 使用Google Chrome
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-profile"

# 方法2: 使用Microsoft Edge
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/edge-debug-profile"
```

**Windows:**

```cmd
# Google Chrome
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\temp\chrome-debug-profile"

# Microsoft Edge
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\temp\edge-debug-profile"
```

**Linux:**

```bash
# Google Chrome
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-profile"

# Chromium
chromium-browser \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-debug-profile"
```

### 参数说明

- `--remote-debugging-port=9222`: 开启调试端口（必需）
- `--user-data-dir`: 用户数据目录（可选，避免污染默认配置）

### 验证浏览器是否启动成功

```bash
# 在另一个终端窗口运行
curl http://localhost:9222/json/version
```

如果看到JSON输出，说明浏览器已正确启动。

---

## 6. 登录系统

### 步骤1: 访问财税通

在启动的浏览器中访问：
```
https://cst.uf-tree.com
```

### 步骤2: 登录

1. 输入您的账号和密码
2. 完成短信验证（如果需要）
3. 选择要操作的企业

### 步骤3: 验证权限

确保您有权限：
- 查看员工管理页面
- 添加新员工

**测试方法：**
1. 点击左侧菜单 "企业管理" → "员工管理"
2. 确认能看到员工列表
3. 点击右上角 "添加员工" 按钮
4. 确认能看到下拉菜单

---

## 7. 测试运行

### 准备测试数据

创建 `test_employees.xlsx`:

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 测试员工1 | 13800138001 | 测试门店1 |
| 测试员工2 | 13800138002 | 测试门店2 |

**注意事项：**
- 手机号必须是11位
- 门店名称必须与您系统中的完全一致
- 建议使用测试数据先验证

### 运行脚本

```bash
python caishui_add_staff.py test_employees.xlsx
```

### 预期输出

```
[CaishuiStaff] 读取到 2 个员工

============================================================
📋 员工数据预览
============================================================
 1. 测试员工1 | 13800138001 | 测试门店1
 2. 测试员工2 | 13800138002 | 测试门店2

============================================================
确认添加以上员工? (y/n): y

[CaishuiStaff] 连接浏览器...

[1/2] 添加: 测试员工1
  ✅ 成功

[2/2] 添加: 测试员工2
  ✅ 成功

============================================================
📊 添加完成
============================================================
成功: 2/2
失败: 0/2

🔍 验证结果...
验证通过: 2/2
[CaishuiStaff] 完成！
```

---

## 🎉 恭喜！

您已成功安装并配置了财税通员工批量添加工具！

### 下一步

1. 准备您的真实员工数据
2. 按照上述步骤运行脚本
3. 享受自动化带来的便利！

---

## ❓ 遇到问题？

查看 [README.md](README.md) 中的常见问题部分，或提交 GitHub Issue。

### 常见错误

**错误1: `ModuleNotFoundError: No module named 'playwright'`**
```bash
# 解决：确保在虚拟环境中安装依赖
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

**错误2: `Error: Browser.connect_over_cdp: Timeout`**
```bash
# 解决：浏览器未启动调试模式
# 请按照步骤5重新启动浏览器
```

**错误3: `playwright install chromium` 卡住**
```bash
# 解决：使用镜像源
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
  playwright install chromium
```

---

## 📚 更多资源

- [详细使用文档](SKILL.md)
- [API参考](API.md)
- [更新日志](CHANGELOG.md)
