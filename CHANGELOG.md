# 更新日志

所有重要的变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.0.0] - 2024-03-07

### 🎉 初始版本发布

#### 新增
- ✅ 支持从Excel批量导入员工数据
- ✅ 支持从CSV批量导入员工数据
- ✅ 自动识别姓名、手机号、部门字段
- ✅ 支持vue-treeselect树形部门选择
- ✅ 智能错误重试机制（最多3次）
- ✅ 添加结果自动验证
- ✅ 详细的日志输出
- ✅ 支持Playwright浏览器调试模式
- ✅ 完整的文档和示例

#### 功能特性
- 自动处理12位手机号（截断为11位）
- 支持"保存并继续添加"批量模式
- 自动识别并跳过重复手机号
- 支持Windows/macOS/Linux多平台

#### 文档
- 创建完整README文档
- 创建详细安装教程SETUP.md
- 创建快速开始指南QUICKSTART.md
- 创建使用说明SKILL.md
- 创建贡献指南CONTRIBUTING.md

---

## [Unreleased]

### 计划中的功能

#### 新增
- [ ] 支持JSON/YAML数据格式
- [ ] 添加图形界面（GUI）版本
- [ ] 支持批量编辑现有员工
- [ ] 支持批量删除员工
- [ ] 支持员工数据导出
- [ ] 支持多企业切换
- [ ] 支持API直连模式（无需浏览器）

#### 改进
- [ ] 优化部门选择逻辑
- [ ] 添加更多错误提示
- [ ] 支持自定义字段映射
- [ ] 添加进度条显示
- [ ] 支持并发添加

#### 文档
- [ ] 添加视频教程
- [ ] 添加常见问题视频解答
- [ ] 添加最佳实践指南

---

## 版本说明

### 版本号规则
- **主版本号**：重大功能变更或破坏性更新
- **次版本号**：新增功能，向下兼容
- **修订号**：问题修复，向下兼容

### 标签说明
- 🎉 重大版本发布
- ✅ 新增功能
- 🔧 问题修复
- ⚡ 性能优化
- 📚 文档更新
- 🔒 安全更新

---

## 历史版本

### [0.9.0] - 2024-03-06
**Beta测试版本**
- 内部测试版本
- 基础功能实现

### [0.1.0] - 2024-03-05
**原型版本**
- 项目初始化
- 基础架构搭建

---

## 如何更新

### 从旧版本升级

```bash
# 1. 备份数据
cp employees.xlsx employees_backup.xlsx

# 2. 拉取最新代码
git pull origin main

# 3. 更新依赖
pip install -r requirements.txt --upgrade

# 4. 验证安装
python caishui_add_staff.py --version
```

### 检查更新

```bash
# 查看最新版本
git fetch origin
git log HEAD..origin/main --oneline
```

---

## 反馈与建议

如果您有任何建议或发现了问题，请：

1. 查看 [Issues](https://github.com/yourusername/caishui-add-staff/issues) 是否已存在
2. 创建新的 Issue 或 Discussion
3. 发送邮件到: your.email@example.com

---

**注意**: 此项目与财税通（凯旋创智）官方无关，是社区开发的第三方工具。
