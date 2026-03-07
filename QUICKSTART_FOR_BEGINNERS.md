# 🎯 小白专用快速指南

**完全不懂代码？没关系！跟着步骤做就行！**

---

## 📦 第一步：下载工具

### 方式1：命令行下载（推荐）
打开终端（Terminal），粘贴运行：
```bash
git clone https://github.com/tang730125633/caishui-add-staff.git
cd caishui-add-staff
```

### 方式2：网页下载
1. 打开 https://github.com/tang730125633/caishui-add-staff
2. 点击绿色按钮 "Code" → "Download ZIP"
3. 解压下载的文件

---

## 🔧 第二步：安装环境

### macOS 用户
打开终端，依次运行：
```bash
# 进入文件夹
cd caishui-add-staff

# 安装Python环境
python3 -m venv venv
source venv/bin/activate

# 安装必要组件
pip install -r requirements.txt
```

### Windows 用户
打开命令提示符（CMD）或 PowerShell：
```cmd
cd caishui-add-staff
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**看到 `(venv)` 字样就说明成功了！**

---

## 🌐 第三步：启动浏览器

### macOS
打开终端，运行：
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

### Windows
按 `Win + R`，输入：
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**会弹出一个新的浏览器窗口，保持它打开！**

---

## 🔑 第四步：登录系统

在弹出的浏览器中：
1. 访问 https://cst.uf-tree.com
2. 输入你的账号密码登录
3. 选择企业要操作的企业
4. 进入「员工管理」页面

**保持浏览器窗口不要关闭！**

---

## 🤖 第五步：自动获取配置（最神奇的一步！）

在终端中运行：
```bash
python auto_config_helper.py
```

你会看到：
```
🔧 财税通配置自动获取工具

本工具将自动从浏览器中提取：
  1. x-token (认证令牌)
  2. companyId (企业ID)
  3. 部门列表 (名称和ID映射)

...

✅ 配置已保存到: config.json

现在可以运行：
  python caishui_add_staff_api.py your_employees.xlsx
```

**不用手动找任何东西，脚本自动帮你搞定！** 🎉

---

## 📊 第六步：准备员工表格

创建一个 Excel 文件 `employees.xlsx`，内容如下：

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 测试门店1 |
| 李四 | 13800138001 | 测试门店2 |
| 王五 | 13800138002 | 测试门店3 |

**注意：**
- 第一行必须是「姓名、手机号、门店」
- 手机号要写11位
- 门店名称要和系统里的一致

---

## 🚀 第七步：批量添加员工！

运行：
```bash
python caishui_add_staff_api.py employees.xlsx
```

你会看到：
```
🚀 API 高速批量导入（20人）
[ 1/20] 张三     ... ✅
[ 2/20] 李四     ... ✅
[ 3/20] 王五     ... ✅
...
[20/20] 赵六     ... ✅

📊 API 批量导入完成
总耗时: 17.12 秒
成功添加: 20/20
🎉 全部处理成功！
```

**20个员工，17秒搞定！** ⚡

---

## ❓ 常见问题

### Q1: 运行 `auto_config_helper.py` 提示连接失败？
**A:** 确保：
1. 浏览器已启动调试模式（看第三步）
2. 浏览器窗口没有关闭
3. 已登录财税通系统

### Q2: 提示 "未找到 config.json"？
**A:** 先运行配置获取工具：
```bash
python auto_config_helper.py
```

### Q3: 添加失败，提示 "该用户已在本企业"？
**A:** 说明这个员工已经添加过了，可以跳过或删除这行数据

### Q4: 提示 "未知部门"？
**A:** 检查Excel中的门店名称是否和系统里完全一致（包括空格）

### Q5: 手机号保存失败？
**A:** 确保手机号是11位数字，不要带空格、横线或其他字符

---

## 🆘 还是搞不定？

**终极解决方案：**

1. **录制视频**：把你操作的整个过程录下来
2. **发送错误截图**：把报错信息截图
3. **联系帮助**：发邮件到 xxx@example.com 或提交 GitHub Issue

---

## 📝 使用流程图

```
下载工具 → 安装环境 → 启动浏览器 → 登录系统
                                          ↓
运行 auto_config_helper.py（自动获取配置）
                                          ↓
准备 Excel 文件（员工名单）
                                          ↓
运行 caishui_add_staff_api.py（批量添加）
                                          ↓
🎉 完成！
```

---

## 💡 小技巧

### 1. 如何快速准备Excel？
- 从HR系统导出员工名单
- 复制粘贴到 Excel
- 确保三列：姓名、手机号、门店

### 2. 如何验证是否添加成功？
- 打开财税通网页
- 进入员工管理
- 搜索刚添加的员工姓名
- 能看到就说明成功了！

### 3. 如果一次要添加几百人？
- Excel可以分批次，每次20-50人
- 或者一次性导入，API会自动处理

---

## 🎯 记住这三个命令

```bash
# 1. 启动浏览器（只需要一次）
chrome --remote-debugging-port=9222

# 2. 获取配置（只需要一次）
python auto_config_helper.py

# 3. 批量添加（每次有新人就运行）
python caishui_add_staff_api.py employees.xlsx
```

---

**恭喜你！现在你可以像专业人士一样批量添加员工了！** 🎉
