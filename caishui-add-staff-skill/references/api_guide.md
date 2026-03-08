# API 参考指南

## 基础信息

- **Base URL**: `https://cst.uf-tree.com`
- **认证方式**: Header `x-token`
- **Content-Type**: `application/json`

## API 端点

### 1. 添加员工

**Endpoint:**
```
POST /api/member/userInfo/add
```

**Headers:**
```json
{
  "x-token": "你的Token",
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "nickName": "员工姓名",
  "mobile": "13800138000",
  "email": "optional@email.com",
  "remark": "备注",
  "departmentIds": [9151],
  "companyId": 7792
}
```

**Response:**
```json
{
  "success": true,
  "message": "添加用户成功",
  "code": 200,
  "result": {
    "id": 16468,
    "userId": 14919,
    "companyId": 7792,
    "name": "员工姓名",
    "mobile": "13800138000"
  }
}
```

### 2. 获取部门列表

**Endpoint:**
```
GET /api/member/department/list
```

**Headers:**
```json
{
  "x-token": "你的Token"
}
```

**Response:**
```json
{
  "code": 200,
  "success": true,
  "data": [
    {
      "id": 9147,
      "name": "凯旋创智测试集团",
      "children": [
        {"id": 9151, "name": "测试门店1"},
        {"id": 9152, "name": "测试门店2"},
        {"id": 9153, "name": "测试门店3"}
      ]
    }
  ]
}
```

## 关键参数说明

### departmentIds

必须使用系统分配的真实部门ID，不是 1/2/3：

| 部门名称 | 部门ID |
|---------|--------|
| 测试门店1 | 9151 |
| 测试门店2 | 9152 |
| 测试门店3 | 9153 |

### companyId

**必需参数！** 企业ID，通常为 7792（凯旋创智测试集团）

## 错误码

| 状态码 | 说明 | 解决方案 |
|--------|------|---------|
| 200 | 成功 | - |
| 400 | 参数错误 | 检查参数完整性 |
| 401 | 登录失效 | 重新获取Token |
| 403 | 无权限 | 检查部门ID是否正确 |
| 500 | 服务器错误 | 稍后重试 |

## 技术实现

### 自动获取 Token

```python
vuex = page.evaluate('() => JSON.parse(localStorage.getItem("vuex") || "{}")')
token = vuex.get('user', {}).get('token', '')
```

### 自动获取部门映射

```python
departments = page.evaluate('''() => {
    const treeselect = document.querySelector('.vue-treeselect');
    if (treeselect && treeselect.__vue__) {
        return treeselect.__vue__.options;
    }
    return null;
}''')
```

## 参考资料

- [财税通系统](https://cst.uf-tree.com)
- [Playwright 文档](https://playwright.dev/)
- [Vue.js 文档](https://vuejs.org/)
