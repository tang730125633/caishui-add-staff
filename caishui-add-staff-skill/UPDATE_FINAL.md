# 最终更新 - 完全通用版

## 2026-03-08 重大更新

### 找到正确API接口

**接口：** `POST /api/member/department/queryCompany`
- 不需要 body，只需要 token
- 任何账号、任何时候都能用
- 返回完整的部门数据（id, title, children）

### 关键修复

1. **Token 获取**
   - 从 `localStorage.getItem('vuex')` 读取（不是 'ls_vuex'）
   - 实时获取，不会过期

2. **部门获取**
   - 使用正确 API 接口，不再依赖 Vue 组件
   - 支持任意账号的部门结构

3. **公司ID自动获取**
   - 从 API 响应中提取 `companyId`
   - 不同账号自动适配

4. **部门检测更智能**
   - 优先找"门店"
   - 其次找"测试"
   - 否则取前10个

### 测试结果

- ✅ 新账号（companyId: 7061）成功获取 94 个部门
- ✅ 旧账号（companyId: 7792）同样适用
- ✅ 完全通用，无需任何硬编码

### 使用方法

```bash
python scripts/add_staff.py
```

自动完成：
1. 获取 Token
2. 获取部门映射
3. 读取 Excel
4. 批量添加员工
