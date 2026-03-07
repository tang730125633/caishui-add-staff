# 财税通API开发计划

## 📊 测试结果总结

### ✅ 已验证的API（可用且稳定）

| API | 端点 | 状态 | 速度 | 说明 |
|-----|------|------|------|------|
| 添加员工 | POST /api/member/userInfo/add | ✅ 可用 | 0.8秒/人 | 已验证38人 |
| 更新员工 | PUT /api/member/userInfo/update | ⚠️ 待验证 | - | 文档中有 |
| 删除员工 | DELETE /api/member/userInfo/{id} | ⚠️ 待验证 | - | 文档中有 |

### ⚠️ 需要重新登录验证的API

由于当前Token和浏览器会话已过期，以下API需要重新登录后验证：

#### 1. 费用类型管理
```
GET /ccs/bill/feeTemplate/queryFeeTypes
参数: companyId
功能: 查询企业所有费用类型
用途: 自动同步费用类型到本地系统
```

#### 2. 单据模板管理
```
GET /ccs/bill/template/queryTemplateTree
参数: companyId
功能: 查询单据模板树
用途: 查看可用的报销单模板
```

#### 3. 借款单查询
```
POST /ccs/bill/loan/queryLoanByParam
参数: {pageNumber, pageSize, companyId}
功能: 分页查询借款单
用途: 批量导出借款数据
```

#### 4. 还款单查询
```
POST /ccs/bill/loan/queryRepaymentByParam
参数: {pageNumber, pageSize, companyId}
功能: 查询还款单
用途: 统计还款情况
```

#### 5. 报销单查询
```
GET /ccs/bill/expenses/queryLoanByExpenses
参数: {companyId, currentUserId, templateId}
功能: 查询可关联的借款单
用途: 报销时关联借款
```

#### 6. 部门列表
```
GET /api/member/department/list
参数: companyId
功能: 查询部门列表
用途: 获取部门ID映射
状态: ⚠️ 之前测试返回"无操作权限"
```

---

## 🎯 优先级建议

### 🔥 高优先级（建议优先开发）

1. **员工管理模块** ✅ 已完成
   - 添加员工（已验证）
   - 更新员工信息（待验证）
   - 删除员工（待验证）

2. **部门同步模块**
   - 查询部门列表
   - 建立部门ID映射
   - 自动更新配置

### ⭐ 中优先级（推荐开发）

3. **费用类型同步**
   - 查询费用类型
   - 导出费用类型列表
   - 对比检查差异

4. **借款单导出**
   - 查询借款单
   - 按状态筛选（待还、已还）
   - 导出Excel报表

### 📋 低优先级（可选开发）

5. **单据模板查询**
   - 查询模板树
   - 查看模板详情

6. **报销单关联**
   - 查询可关联借款单
   - 辅助报销流程

---

## 🛠️ 开发建议

### 阶段1: 完善员工管理（1-2天）
- [ ] 验证更新员工API
- [ ] 验证删除员工API
- [ ] 添加员工查询功能（如果可用）
- [ ] 完善错误处理

### 阶段2: 部门同步（1天）
- [ ] 重新登录并测试部门列表API
- [ ] 开发部门同步功能
- [ ] 自动更新config.json中的部门映射

### 阶段3: 费用类型（1天）
- [ ] 测试费用类型查询API
- [ ] 开发导出功能
- [ ] 生成费用类型报表

### 阶段4: 借款单（2天）
- [ ] 测试借款单查询API
- [ ] 开发分页查询
- [ ] 开发筛选功能（按状态、按人员）
- [ ] 生成借款统计报表

---

## 💡 技术实现建议

### 统一API客户端
```python
class CaishuiAPI:
    def __init__(self, token, company_id):
        self.token = token
        self.company_id = company_id
        
    def call_api(self, endpoint, method='GET', data=None, params=None):
        # 统一处理认证、错误、重试
        pass
        
    def validate_token(self):
        # 检查Token是否有效
        pass
```

### 模块化设计
```
caishui_api/
├── __init__.py
├── client.py          # 核心客户端
├── staff.py           # 员工管理
├── department.py      # 部门管理
├── fee_template.py    # 费用类型
├── loan.py            # 借款单
└── expenses.py        # 报销单
```

---

## ⚠️ 已知限制

1. **Token有效期**
   - Token会过期，需要定期刷新
   - 解决方案: auto_config_helper.py 重新获取

2. **权限限制**
   - 部分API需要特定权限
   - 如部门列表查询之前返回"无操作权限"

3. **浏览器依赖**
   - 获取Token需要浏览器调试模式
   - 解决方案: 使用Playwright连接已登录浏览器

---

## 🚀 下一步行动

### 选项A: 重新登录验证所有API
1. 启动浏览器调试模式
2. 重新登录财税通
3. 运行 auto_config_helper.py 获取新Token
4. 逐一测试上述API

### 选项B: 基于文档开发，后续验证
1. 根据docs/中的API文档编写代码
2. 使用示例数据开发功能
3. 等重新登录后再测试调试

### 选项C: 优先完善现有功能
1. 先完善员工管理模块（添加更新/删除功能）
2. 添加Token过期检测和提示
3. 优化用户体验

---

## 📞 建议

**推荐选项B+选项C并行：**
- 基于已知可用的员工添加API，完善员工管理功能
- 同时编写其他API的代码框架（基于文档）
- 等方便重新登录时，再一次性验证所有API

这样既可以快速推进开发，又可以在验证后立即投入使用。
