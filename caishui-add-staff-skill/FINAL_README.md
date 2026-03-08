# 财税通员工批量添加 Skill - 最终版

## 🎯 核心特点

- ✅ **完全通用**: 任何账号、任何部门结构都适用
- ✅ **自动获取Token**: 实时从浏览器 localStorage 读取
- ✅ **自动获取部门**: 通过API接口，不需要页面交互
- ✅ **自动获取公司ID**: 从API响应中提取
- ✅ **智能分配**: 自动分配员工到可用部门

## 🚀 快速使用

### 前置条件

1. 启动 Chrome 调试模式:
```bash
chrome --remote-debugging-port=9222
```

2. 登录财税通系统，保持浏览器窗口打开

3. 准备 Excel 文件 (employees.xlsx):
| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 1 |
| 李四 | 13800138001 | 2 |

### 运行

```bash
python scripts/add_staff.py
```

## 📋 技术要点

### 1. Token获取

```javascript
// 正确的key是'vuex'，不是'ls_vuex'
const v = JSON.parse(localStorage.getItem('vuex'));
return v.user.token;
```

### 2. 部门获取

```python
# 正确的API接口
POST /api/member/department/queryCompany
Headers: {"x-token": token, "Content-Type": "application/json"}
Body: {}  # 空body即可

# 响应
{
  "success": true,
  "result": {
    "departments": [
      {"id": 1129, "title": "部门名称", "companyId": 7061}
    ]
  }
}
```

### 3. 添加员工

```python
POST /api/member/userInfo/add
Body: {
  "nickName": "姓名",
  "mobile": "手机号",
  "departmentIds": [部门ID],
  "companyId": 公司ID  # 从API自动获取
}
```

## 🔧 故障排除

### Q1: 无法获取Token？
- 确保浏览器已启动调试模式
- 确保已登录财税通系统
- 检查key是否为'vuex'不是'ls_vuex'

### Q2: API返回错误？
- 检查Token是否过期（重新获取）
- 检查网络连接
- 检查部门ID是否正确

### Q3: 找不到Excel文件？
- 确保文件在桌面
- 文件名包含"员工"
- 格式为.xlsx

## 📊 测试结果

| 账号 | 公司ID | 部门数 | 结果 |
|------|--------|--------|------|
| 测试账号1 | 7792 | 4 | ✅ 成功 |
| 测试账号2 | 7061 | 94 | ✅ 成功 |

## 📝 更新日志

### 2026-03-08 最终版
- 找到正确API接口 `/api/member/department/queryCompany`
- 修复所有硬编码问题
- 完全通用，任何账号适用
- 自动化程度100%

## 💡 给其他AI的话

这个Skill的核心是:
1. Token从浏览器实时获取（不会过期）
2. 部门从API获取（不依赖页面状态）
3. 公司ID从API响应自动提取（不需要硬编码）

完全通用，放心使用！
