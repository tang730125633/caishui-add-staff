# API 方案问题反思与解决方案

## ❌ 错误复盘

### 我犯的错误

1. **想当然地使用错误的部门ID**
   - ❌ 错误：使用了 `departmentIds: [1]` 
   - ✅ 正确：应该从页面获取真实的部门ID（如 9151, 9152, 9153）

2. **缺少关键参数**
   - ❌ 错误：API 调用时缺少 `companyId`
   - ✅ 正确：必须包含 `"companyId": 7792`

3. **测试方法不当**
   - ❌ 错误：直接调用 API 获取部门列表返回 403，就认为 API 不可用
   - ✅ 正确：应该从已登录的页面 JavaScript 变量中获取部门数据

4. **陷入思维定势**
   - ❌ 错误：看到 403 就认为是权限问题，没有深入分析
   - ✅ 正确：403 是因为部门ID不对，不是账号权限问题

---

## ✅ 正确解决方案

### 关键发现

**获取部门ID的正确方式：**

```python
# 从页面 Vue 实例获取部门数据
depts = page.evaluate('''() => {
    const vueEl = document.querySelector('.vue-treeselect');
    if (vueEl && vueEl.__vue__) {
        return vueEl.__vue__.options;
    }
    return null;
}''')
```

**返回的部门数据：**
```json
[
  {"id": 9147, "label": "凯旋创智测试集团"},
  {"id": 9151, "label": "测试门店1"},
  {"id": 9152, "label": "测试门店2"},
  {"id": 9153, "label": "测试门店3"}
]
```

### 正确的 API 调用方式

```python
import requests

headers = {
    "x-token": "你的Token",
    "Content-Type": "application/json"
}

payload = {
    "nickName": "员工姓名",
    "mobile": "手机号",
    "departmentIds": [9151],  # 真实的部门ID
    "companyId": 7792         # 关键参数！
}

response = requests.post(
    "https://cst.uf-tree.com/api/member/userInfo/add",
    headers=headers,
    json=payload
)
```

---

## 📋 部门ID映射

| Excel 部门编号 | 部门名称 | 真实部门ID |
|--------------|---------|-----------|
| 1 | 测试门店1 | 9151 |
| 2 | 测试门店2 | 9152 |
| 3 | 测试门店3 | 9153 |

---

## 🎯 经验总结

1. **不要假设默认值**：部门ID不是 1/2/3，而是系统分配的真实ID
2. **从页面获取数据**：当 API 返回权限错误时，尝试从页面 JS 变量获取
3. **完整的参数检查**：确保所有必需参数都已提供（特别是 companyId）
4. **保持积极心态**：遇到困难不要轻易放弃，多角度尝试

---

## 🔧 工具改进

添加了新的工具脚本：

1. `get_departments.py` - 从页面获取部门ID映射
2. `batch_add_api.py` - 使用API批量添加员工
3. 更新了 `caishui_add_staff_api.py` 支持自动获取部门映射

---

*反思日期: 2026-03-08*
*教训: 不要轻易说"不行"，要深入分析问题的根本原因*
