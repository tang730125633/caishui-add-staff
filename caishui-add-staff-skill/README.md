# 财税通员工批量添加 Skill

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.40+-green.svg)](https://playwright.dev/python/)

🚀 **一键批量添加员工到财税通（凯旋创智）系统**

## ✨ 功能特性

- ⚡ **API高速导入** - 0.8秒/人，比浏览器快10倍
- 🌐 **浏览器自动化** - 无需API权限，稳定可靠
- 🤖 **全自动获取** - 自动获取Token和部门ID映射
- 📊 **Excel支持** - 自动读取员工数据
- 🎯 **智能匹配** - 自动匹配门店名称到部门ID

## 🚀 快速开始

### 安装

```bash
# 安装依赖
pip install playwright pandas openpyxl requests
playwright install chromium
```

### 启动浏览器

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Windows
chrome --remote-debugging-port=9222
```

然后登录财税通系统。

### 使用

```bash
# 基本使用
python scripts/add_staff.py

# 指定Excel文件
python scripts/add_staff.py --file employees.xlsx

# 使用浏览器方式
python scripts/add_staff.py --method browser
```

## 📋 Excel 格式

创建 `employees.xlsx`:

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 测试门店1 |
| 李四 | 13800138001 | 测试门店2 |
| 王五 | 13800138002 | 测试门店3 |

## 🔧 命令行参数

```
python scripts/add_staff.py [选项]

Options:
  --file PATH          Excel文件路径 (默认: employees.xlsx)
  --method METHOD      添加方式: api|browser (默认: api)
  --debug-port PORT    浏览器调试端口 (默认: 9222)
  --verify             添加后验证结果
```

## 📝 技术原理

### 自动获取部门ID映射

**核心代码：**
```python
departments = page.evaluate('''() => {
    const treeselect = document.querySelector('.vue-treeselect');
    if (treeselect && treeselect.__vue__) {
        return treeselect.__vue__.options;
    }
    return null;
}''')
```

**原理：** 直接访问 Vue.js 组件内部数据，绕过API权限限制。

### API 调用

```python
POST /api/member/userInfo/add
Headers:
  x-token: {token}
  Content-Type: application/json

Body:
{
  "nickName": "员工姓名",
  "mobile": "13800138000",
  "departmentIds": [9151],
  "companyId": 7792
}
```

## 🐛 故障排除

### Q1: 403 无操作权限？

Skill会自动获取正确的部门ID，无需手动配置。

### Q2: 无法连接浏览器？

确保 Chrome 已启动调试模式：`--remote-debugging-port=9222`

### Q3: 查看部门ID映射？

```bash
python scripts/get_departments.py
```

## 📚 文档

- [技术方案详解](./references/api_guide.md)
- [配置说明](./config/schema.json)
- [使用示例](./examples/example_usage.py)

## 📄 许可证

MIT License
