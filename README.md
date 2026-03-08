# 财税通员工批量添加工具

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/python/)

🚀 **自动化批量添加员工到财税通（凯旋创智）系统**，支持 API 高速导入和浏览器自动化两种方式。

---

## 📋 目录

- [功能特性](#功能特性)
- [快速开始](#快速开始)
- [两种使用方式](#两种使用方式)
- [详细教程](#详细教程)
- [常见问题](#常见问题)
- [更新日志](#更新日志)

---

## ✨ 功能特性

- ⚡ **API高速批量导入** - 0.8秒/人，比浏览器快10倍！
- 🌐 **浏览器自动化** - 无需API权限，稳定可靠
- 📊 **Excel/CSV支持** - 自动读取员工数据
- 🎯 **智能部门映射** - 自动匹配部门ID
- ✅ **自动获取Token** - 无需手动抓包
- 📈 **实时进度显示** - 查看添加进度和结果

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/tang730125633/caishui-add-staff.git
cd caishui-add-staff

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install playwright pandas openpyxl requests
playwright install chromium
```

### 2. 启动浏览器调试模式

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

### 3. 登录系统

1. 在启动的浏览器中访问 https://cst.uf-tree.com
2. 输入账号密码登录
3. 选择企业进入系统
4. **保持浏览器窗口打开**

### 4. 准备数据

创建 `employees.xlsx`:

| 姓名 | 手机号 | 部门 |
|------|--------|------|
| 张三 | 13800138000 | 1 |
| 李四 | 13800138001 | 2 |
| 王五 | 13800138002 | 3 |

**部门编号对应：**
- 1 → 测试门店1
- 2 → 测试门店2
- 3 → 测试门店3

### 5. 运行脚本

```bash
# 方式1: API高速导入（推荐！）
python batch_add_api.py

# 方式2: 浏览器自动化
python auto_add_v10.py
```

---

## 🎯 两种使用方式

### 方式一：API高速导入 ⭐ 推荐

**优点：**
- ⚡ 速度极快（0.8秒/人）
- 🎯 精准控制
- 📊 批量处理

**使用步骤：**

```bash
# 1. 获取部门ID映射
python get_department_map.py

# 2. 批量添加员工
python batch_add_api.py
```

**原理：**
- 调用系统API直接添加员工
- 需要正确的部门ID（从页面获取）
- 需要包含 companyId 参数

### 方式二：浏览器自动化

**优点：**
- ✅ 无需关心部门ID
- ✅ 稳定可靠
- ✅ 模拟真实用户操作

**使用步骤：**

```bash
python auto_add_v10.py
```

**原理：**
- 模拟人工点击"添加员工"
- 自动填写表单
- 自动选择部门

---

## 📖 详细教程

### API方式详解

#### 获取部门ID

```bash
python get_department_map.py
```

**输出示例：**
```
✅ 页面: https://cst.uf-tree.com/company/staff
🔍 从页面 Vue 实例获取部门数据...

✅ 找到部门数据:
   - 凯旋创智测试集团: 9147
   - 测试门店1: 9151
   - 测试门店2: 9152
   - 测试门店3: 9153

💾 已保存到 department_map.json
```

#### API调用示例

```python
import requests

headers = {
    "x-token": "你的Token",
    "Content-Type": "application/json"
}

payload = {
    "nickName": "员工姓名",
    "mobile": "13800138000",
    "departmentIds": [9151],  # 真实的部门ID
    "companyId": 7792         # 必须包含！
}

response = requests.post(
    "https://cst.uf-tree.com/api/member/userInfo/add",
    headers=headers,
    json=payload
)
```

### 浏览器自动化详解

#### 启动浏览器

```bash
# 启动Chrome调试模式
chrome --remote-debugging-port=9222
```

#### 运行脚本

```bash
python auto_add_v10.py
```

**流程：**
1. 连接已启动的浏览器
2. 导航到员工管理页面
3. 点击"添加员工" → "直接添加"
4. 填写手机号、姓名
5. 选择部门
6. 点击保存
7. 循环处理下一个员工

---

## ❓ 常见问题

### Q1: API返回403无操作权限？

**原因：** 部门ID不正确或缺少companyId

**解决：**
1. 运行 `python get_department_map.py` 获取真实部门ID
2. 确保API调用包含 `"companyId": 7792`

### Q2: 浏览器连接失败？

**原因：** 浏览器未启动调试模式

**解决：**
```bash
# 启动浏览器时添加参数
chrome --remote-debugging-port=9222
```

### Q3: 如何选择正确的部门？

**方式1：** 查看 department_map.json

**方式2：** 在Excel中使用部门编号：
- 1 → 测试门店1
- 2 → 测试门店2
- 3 → 测试门店3

### Q4: 添加失败怎么办？

1. 检查手机号格式（11位数字）
2. 检查部门ID是否正确
3. 检查浏览器是否保持登录状态
4. 尝试浏览器自动化方式

---

## 📝 更新日志

### 2026-03-08 重要更新

**修复：** API方式添加员工失败的问题

**问题原因：**
1. 使用了错误的部门ID（如 `[1]` 而不是真实的 `9151`）
2. 缺少关键的 `companyId` 参数
3. 没有正确获取系统分配的部门ID

**解决方案：**
1. ✅ 新增 `get_department_map.py` 从页面获取真实部门ID
2. ✅ 新增 `batch_add_api.py` 完整的批量添加示例
3. ✅ 新增 `REFLECTION.md` 详细的问题反思

**部门ID映射：**
```
测试门店1 → 9151
测试门店2 → 9152
测试门店3 → 9153
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**注意：** 本工具仅供学习和合法使用，请遵守相关法律法规。
