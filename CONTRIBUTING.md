# 贡献指南

感谢您对本项目的兴趣！我们欢迎各种形式的贡献。

---

## 🤝 如何贡献

### 报告问题

如果您发现了bug或有功能建议：

1. 检查是否已有相关 [Issue](https://github.com/yourusername/caishui-add-staff/issues)
2. 如果没有，创建新的 Issue
3. 使用模板填写详细信息

### 提交代码

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📋 开发环境

### 设置开发环境

```bash
# 1. Fork并克隆仓库
git clone https://github.com/YOUR_USERNAME/caishui-add-staff.git
cd caishui-add-staff

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 安装pre-commit钩子
pre-commit install
```

### 代码风格

我们使用以下工具保持代码质量：

- **black**: 代码格式化
- **flake8**: 代码风格检查
- **mypy**: 类型检查

运行检查：
```bash
# 格式化代码
black caishui_add_staff.py

# 检查代码风格
flake8 caishui_add_staff.py

# 类型检查
mypy caishui_add_staff.py
```

---

## 📝 提交规范

### Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type 类型:**
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例:**
```
feat(add): 支持从CSV文件导入员工

- 添加CSV格式解析
- 自动检测文件编码
- 更新文档

Closes #123
```

---

## 🧪 测试

### 运行测试

```bash
pytest tests/
```

### 添加测试

在 `tests/` 目录下添加测试文件：

```python
# tests/test_add_staff.py
def test_parse_phone():
    from caishui_staff import parse_phone
    assert parse_phone("13800138000") == "13800138000"
    assert parse_phone("138001380000") == "13800138000"  # 截断到11位
```

---

## 📚 文档

### 更新文档

如果您更改了功能，请同时更新：
- `README.md` - 主要文档
- `SETUP.md` - 安装教程
- `SKILL.md` - 详细使用说明
- `CHANGELOG.md` - 更新日志

---

## 🎯 路线图

### 短期计划 (v1.1)
- [ ] 支持更多数据格式（JSON, YAML）
- [ ] 添加图形界面（GUI）
- [ ] 支持批量编辑员工

### 中期计划 (v1.2)
- [ ] 支持多企业切换
- [ ] 支持批量导入历史数据
- [ ] 添加数据验证功能

### 长期计划 (v2.0)
- [ ] 支持API直连模式
- [ ] 支持定时任务
- [ ] 支持多账号管理

---

## 💡 建议

有任何建议或想法？欢迎：
- 创建 [Discussion](https://github.com/yourusername/caishui-add-staff/discussions)
- 发送邮件到: your.email@example.com

---

## 📄 许可证

通过贡献代码，您同意您的贡献将在 [MIT 许可证](LICENSE) 下发布。

---

## 🙏 致谢

感谢所有贡献者！

<a href="https://github.com/yourusername/caishui-add-staff/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/caishui-add-staff" />
</a>
