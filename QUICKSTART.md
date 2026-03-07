# 快速开始指南 (5分钟上手)

⏱️ **预计时间：5分钟**

---

## 🎯 目标

完成本指南后，您将能够：
- ✅ 批量添加员工到财税通系统
- ✅ 自动处理Excel数据
- ✅ 验证添加结果

---

## 📋 准备工作

### 1. 检查清单

在开始之前，请确认：

- [ ] Python 3.8+ 已安装
- [ ] Chrome/Edge 浏览器已安装
- [ ] 财税通账号已注册并有添加权限

### 2. 一键安装（复制粘贴运行）

**macOS/Linux:**
```bash
# 1. 下载代码
git clone https://github.com/yourusername/caishui-add-staff.git
cd caishui-add-staff

# 2. 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. 安装浏览器
playwright install chromium
```

**Windows:**
```cmd
:: 1. 下载代码
git clone https://github.com/yourusername/caishui-add-staff.git
cd caishui-add-staff

:: 2. 创建虚拟环境并安装依赖
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

:: 3. 安装浏览器
playwright install chromium
```

---

## 🚀 3步完成批量添加

### 第1步：启动浏览器（30秒）

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
```

**Windows:**
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

⚠️ **浏览器窗口不要关闭！**

---

### 第2步：登录财税通（1分钟）

1. 在刚启动的浏览器中访问：https://cst.uf-tree.com
2. 输入账号密码登录
3. 选择企业进入

---

### 第3步：准备Excel并运行（3分钟）

#### 创建Excel文件

新建 `employees.xlsx`，内容如下：

| 姓名 | 手机号 | 门店 |
|------|--------|------|
| 张三 | 13800138000 | 测试门店1 |
| 李四 | 13800138001 | 测试门店2 |

⚠️ **手机号必须是11位，不要有空格！**

#### 运行脚本

```bash
python caishui_add_staff.py employees.xlsx
```

#### 确认添加

看到提示时输入 `y`：
```
确认添加以上员工? (y/n): y
```

---

## ✅ 完成！

您将看到：
```
============================================================
📊 添加完成
============================================================
成功: 2/2
失败: 0/2

🔍 验证结果...
验证通过: 2/2
```

---

## 🆘 常见问题速查

### Q: 提示"连接浏览器失败"
**A:** 浏览器没启动调试模式，重新执行第1步

### Q: 提示"找不到页面"
**A:** 浏览器没登录，执行第2步

### Q: 手机号保存失败
**A:** 检查Excel，手机号必须是11位数字，不能有其他字符

---

## 📖 下一步

- 查看 [详细文档](README.md) 了解更多功能
- 查看 [安装教程](SETUP.md) 了解完整安装过程
- 查看 [使用文档](SKILL.md) 了解高级用法

---

**🎉 恭喜！您已成功批量添加员工！**
