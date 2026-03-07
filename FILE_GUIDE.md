# 📁 项目文件说明

本目录包含所有用于财税通员工批量添加的工具和文档。

---

## 🚀 快速开始（选择你的方式）

### 方式A：小白友好版（推荐！）
**适合：完全不懂代码的新手**

1. 打开 `QUICKSTART_FOR_BEGINNERS.md`
2. 按照步骤一步步操作
3. 运行 `auto_config_helper.py` 自动获取配置
4. 运行 `caishui_add_staff_api.py` 批量添加

### 方式B：标准版
**适合：有一定技术基础的用户**

1. 打开 `QUICKSTART.md`
2. 按照5分钟快速指南操作
3. 手动配置或运行配置助手
4. 使用API方式批量添加

### 方式C：开发版
**适合：开发者或高级用户**

1. 阅读 `README.md` 了解完整功能
2. 查看 `SKILL.md` 了解技术细节
3. 参考 `API_PRINCIPLE.md` 理解原理
4. 根据需要修改源码

---

## 📄 文件详解

### 🎯 核心脚本（直接运行）

| 文件 | 功能 | 使用场景 |
|------|------|---------|
| `caishui_add_staff_api.py` | **API方式**批量添加员工 | ⭐ 推荐！速度最快（0.8秒/人） |
| `caishui_add_staff.py` | **浏览器方式**批量添加员工 | 备用方案，兼容性更好 |
| `auto_config_helper.py` | **自动获取配置**工具 | ⭐ 小白福音！一键获取所有参数 |

### 📖 文档（选择阅读）

| 文件 | 内容 | 适合人群 |
|------|------|---------|
| `QUICKSTART_FOR_BEGINNERS.md` | **小白专用**详细步骤 | 👶 完全不懂代码 |
| `QUICKSTART.md` | **5分钟快速上手指南** | ⏱️ 想快速开始 |
| `README.md` | **完整功能文档** | 📚 全面了解 |
| `SETUP.md` | **详细安装教程** | 🔧 安装遇到问题 |
| `API_PRINCIPLE.md` | **技术原理解析** | 🎓 想深入理解 |
| `SKILL.md` | **完整Skill文档** | 🤖 OpenClaw用户使用 |

### ⚙️ 配置文件

| 文件 | 功能 | 说明 |
|------|------|------|
| `config.example.json` | **配置模板** | 参考模板，复制为 `config.json` |
| `config.json` | **实际配置文件** | 由 `auto_config_helper.py` 自动生成 |
| `requirements.txt` | **Python依赖列表** | 运行 `pip install -r requirements.txt` 安装 |

### 📊 示例数据

| 文件 | 功能 | 说明 |
|------|------|------|
| `employees_example.csv` | **示例员工数据** | 参考格式，包含20个示例员工 |

### 📝 其他文档

| 文件 | 功能 | 说明 |
|------|------|------|
| `CHANGELOG.md` | **更新日志** | 版本历史和功能更新 |
| `CONTRIBUTING.md` | **贡献指南** | 如何参与项目开发 |
| `LICENSE` | **许可证** | MIT开源许可证 |
| `SKILL.json` | **OpenClaw配置** | Skill元数据 |

---

## 🎬 典型使用流程

### 场景1：第一次使用（小白路线）

```bash
# 1. 安装（5分钟）
pip install -r requirements.txt

# 2. 启动浏览器并登录财税通
chrome --remote-debugging-port=9222

# 3. 自动生成配置（1分钟）
python auto_config_helper.py
# 输出：config.json 已生成

# 4. 准备员工表格 employees.xlsx

# 5. 批量添加（20秒）
python caishui_add_staff_api.py employees.xlsx
```

### 场景2：再次使用（已有配置）

```bash
# 直接运行，自动读取 config.json
python caishui_add_staff_api.py new_employees.xlsx
```

### 场景3：没有API权限（备用方案）

```bash
# 使用浏览器方式（较慢但更稳定）
python caishui_add_staff.py employees.xlsx
```

---

## 🔧 常见问题速查

### Q1: 不知道该用哪个文件？
**A:** 
- 第一次使用 → `QUICKSTART_FOR_BEGINNERS.md`
- 快速开始 → `QUICKSTART.md`
- 遇到问题 → `SETUP.md`
- 想了解原理 → `API_PRINCIPLE.md`

### Q2: 脚本运行报错？
**A:** 
1. 检查是否安装了依赖：`pip install -r requirements.txt`
2. 检查是否有 `config.json`（运行 `auto_config_helper.py` 生成）
3. 检查浏览器是否启动调试模式
4. 查看错误信息中的具体提示

### Q3: 配置文件怎么生成？
**A:** 运行配置助手：
```bash
python auto_config_helper.py
```
会自动从浏览器中提取：
- x-token
- companyId
- 部门列表

### Q4: 可以同时使用多种方式吗？
**A:** 可以！两种方式都是往同一个系统添加数据，不会冲突。

---

## 📊 性能对比

| 方式 | 20人耗时 | 速度 | 适用场景 |
|------|---------|------|---------|
| API方式 (`caishui_add_staff_api.py`) | ~17秒 | ⚡ 0.8秒/人 | 推荐日常使用 |
| 浏览器方式 (`caishui_add_staff.py`) | ~5分钟 | 🐢 15秒/人 | API不可用时 |

---

## 💡 最佳实践

### 1. 首次使用
- ✅ 阅读 `QUICKSTART_FOR_BEGINNERS.md`
- ✅ 运行 `auto_config_helper.py` 生成配置
- ✅ 先用 `employees_example.csv` 测试
- ✅ 确认无误后再处理真实数据

### 2. 日常使用
- ✅ 每次只需运行 `caishui_add_staff_api.py`
- ✅ 自动读取已生成的 `config.json`
- ✅ 保持浏览器登录状态即可

### 3. 分享给同事
- ✅ 提供 `QUICKSTART_FOR_BEGINNERS.md`
- ✅ 提供 `auto_config_helper.py`
- ✅ 说明需要安装 Python
- ✅ 提供示例 Excel 模板

### 4. 数据备份
- ✅ 添加前备份原有员工名单
- ✅ 保留每次添加的 Excel 文件
- ✅ 记录添加日志

---

## 🆘 技术支持

遇到问题？

1. **查看文档**：先查阅相关 `.md` 文件
2. **检查配置**：确认 `config.json` 是否正确
3. **查看错误**：终端会显示详细错误信息
4. **提交Issue**：在 GitHub 上提交问题

---

## 📝 文件版本

- **当前版本**: v1.0.0
- **最后更新**: 2024-03-07
- **兼容系统**: 财税通（凯旋创智）
- **Python版本**: 3.8+

---

**现在选择你的方式，开始使用吧！** 🚀
