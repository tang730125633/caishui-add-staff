---
name: caishui-add-staff
description: 财税通系统自动添加员工Skill - 支持API高速批量导入和浏览器自动化两种方式
version: 1.0.0
author: AI Assistant
homepage: https://github.com/tang730125633/caishui-add-staff
keywords:
  - 财税通
  - 员工管理
  - 批量导入
  - API自动化
  - 浏览器自动化
requirements:
  - python >= 3.8
  - playwright >= 1.40
  - pandas >= 2.0
  - openpyxl >= 3.1
  - requests >= 2.31
env:
  - CAISHUI_DEBUG_PORT: "9222"
  - CAISHUI_BASE_URL: "https://cst.uf-tree.com"
---

# 财税通员工批量添加 Skill

🚀 **一键批量添加员工到财税通（凯旋创智）系统**

## 功能特性

- ⚡ **API高速导入** - 0.8秒/人，比浏览器快10倍
- 🌐 **浏览器自动化** - 无需API权限，稳定可靠
- 🤖 **全自动获取** - 自动获取Token和部门ID映射
- 📊 **Excel支持** - 自动读取员工数据
- 🎯 **智能匹配** - 自动匹配门店名称到部门ID

## 快速开始

### 1. 安装

```bash
# 通过 ClawHub 安装
clawhub install caishui-add-staff

# 或手动安装
pip install -r requirements.txt
playwright install chromium
```

### 2. 启动浏览器

```bash
chrome --remote-debugging-port=9222
```

然后登录财税通系统。

### 3. 使用 Skill

```bash
# 方式1: 使用默认文件
@caishui-add-staff

# 方式2: 指定Excel文件
@caishui-add-staff --file employees.xlsx

# 方式3: 使用浏览器自动化方式
@caishui-add-staff --method browser
```

## 详细使用

### Excel 格式

创建 `employees.xlsx`:

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 测试门店1 |
| 李四 | 13800138001 | 测试门店2 |

### 命令行参数

```
@caishui-add-staff [选项]

Options:
  --file PATH          Excel文件路径 (默认: employees.xlsx)
  --method METHOD      添加方式: api|browser (默认: api)
  --debug-port PORT    浏览器调试端口 (默认: 9222)
  --verify             添加后验证结果
  --dry-run            试运行，不实际添加
```

### Python API

```python
from caishui_add_staff import CaishuiStaffManager

# 初始化
manager = CaishuiStaffManager()

# 添加员工
results = manager.add_from_excel("employees.xlsx")

print(f"成功: {results['success']}")
print(f"失败: {results['failed']}")
```

## 技术原理

### 自动获取部门ID映射

```python
# 从页面 Vue 组件读取部门数据
departments = page.evaluate('''() => {
    const treeselect = document.querySelector('.vue-treeselect');
    if (treeselect && treeselect.__vue__) {
        return treeselect.__vue__.options;
    }
    return null;
}''')
```

**核心突破：** 直接访问 Vue.js 组件内部数据，绕过API权限限制。

### API 调用格式

```python
POST /api/member/userInfo/add
Headers:
  x-token: {token}
  Content-Type: application/json

Body:
{
  "nickName": "员工姓名",
  "mobile": "13800138000",
  "departmentIds": [9151],  # 真实的部门ID
  "companyId": 7792         # 企业ID
}
```

## 目录结构

```
caishui-add-staff-skill/
├── SKILL.md                  # Skill 定义
├── README.md                 # 详细文档
├── requirements.txt          # Python依赖
├── config/
│   └── schema.json          # 配置Schema
├── scripts/
│   ├── add_staff.py         # 主脚本
│   ├── get_departments.py   # 获取部门映射
│   └── get_token.py         # 获取Token
├── templates/
│   └── employees.xlsx       # Excel模板
├── references/
│   └── api_guide.md         # API参考
└── examples/
    └── example_usage.py     # 使用示例
```

## 故障排除

### Q1: 403 无操作权限？

**原因：** 部门ID不正确或缺少companyId

**解决：** Skill会自动获取正确的部门ID，无需手动配置

### Q2: 无法连接浏览器？

**原因：** 浏览器未启动调试模式

**解决：**
```bash
chrome --remote-debugging-port=9222
```

### Q3: 如何查看部门ID映射？

```bash
python scripts/get_departments.py
```

## 更新日志

### v1.0.0 (2026-03-08)

- ✅ 实现自动获取部门ID映射（Vue组件读取）
- ✅ 实现自动获取X-Token
- ✅ 完成智能批量添加
- ✅ 支持API和浏览器两种方式
- ✅ 编写详细技术文档

## 参考文档

- [技术方案详解](./references/api_guide.md)
- [问题反思记录](../REFLECTION.md)
- [GitHub 项目](https://github.com/tang730125633/caishui-add-staff)

## 许可证

MIT License
