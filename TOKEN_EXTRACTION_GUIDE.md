# 🔑 Token获取方法详解

## 核心发现

Token不是从开发者工具（F12）手动复制的，而是通过 **Playwright连接已登录的浏览器** 自动提取的！

---

## 🎯 获取Token的三种方法

### 方法1: 从localStorage提取（推荐！）

财税通系统使用Vue.js框架，登录信息存储在localStorage中：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    
    # 从localStorage获取vuex数据
    vuex_data = page.evaluate('''() => {
        return JSON.parse(localStorage.getItem('vuex') || '{}');
    }''')
    
    # Token在user模块中
    token = vuex_data.get('user', {}).get('token')
    company_id = vuex_data.get('user', {}).get('userInfo', {}).get('companyId')
    
    print(f"Token: {token}")
    print(f"CompanyId: {company_id}")
```

**优点**：
- ✅ 完全自动化，无需手动操作
- ✅ 同时获取Token和companyId
- ✅ 还包含用户信息

---

### 方法2: 从Cookies提取

```python
cookies = page.context.cookies()
for cookie in cookies:
    if 'uf-tree.com' in cookie.get('domain', ''):
        if 'token' in cookie['name'].lower():
            print(f"Token: {cookie['value']}")
```

**缺点**：
- ⚠️ 可能包含多个token，需要筛选
- ⚠️ 不一定有companyId

---

### 方法3: 从页面全局变量提取

```python
page_vars = page.evaluate('''() => {
    return {
        token: window.token,
        xToken: window.xToken,
        vuexToken: window.__VUE__?.$store?.state?.user?.token
    };
}''')
```

**缺点**：
- ⚠️ 变量名可能变化
- ⚠️ 不稳定

---

## 📋 完整流程（实际使用的方案）

### Step 1: 启动浏览器调试模式
```bash
chrome --remote-debugging-port=9222
```

### Step 2: 用户手动登录
- 访问 https://cst.uf-tree.com
- 输入账号密码
- 点击进入企业

### Step 3: 自动提取配置
```python
import json
from playwright.sync_api import sync_playwright

def extract_config():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # 从localStorage获取vuex数据
        vuex = page.evaluate('''() => {
            return JSON.parse(localStorage.getItem('vuex') || '{}');
        }''')
        
        # 提取关键信息
        config = {
            "token": vuex.get('user', {}).get('token'),
            "company_id": vuex.get('user', {}).get('userInfo', {}).get('companyId'),
            "user_info": vuex.get('user', {}).get('userInfo', {})
        }
        
        # 保存配置
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        return config
```

---

## 🎯 获取部门ID映射的方法

部门ID不能直接从API获取（之前测试返回"无操作权限"），所以我们通过 **用户配置** + **API验证** 的方式：

### 方法1: 手动配置（当前使用）

```json
{
  "department_map": {
    "测试门店1": 9151,
    "测试门店2": 9152,
    "测试门店3": 9153
  }
}
```

获取方法：
1. 在财税通网页中添加一个测试员工
2. 选择部门时抓包（浏览器F12 → Network）
3. 查看请求中的departmentIds参数

### 方法2: 从浏览器自动化提取

```python
# 打开添加员工页面
page.goto("https://cst.uf-tree.com/company/staff")
page.click('button:has-text("添加员工")')
page.click('.el-dropdown-menu__item:has-text("直接添加")')

# 点击部门选择
page.click('.vue-treeselect__control')
time.sleep(2)

# 从DOM提取部门选项
departments = page.evaluate('''() => {
    const opts = document.querySelectorAll('.vue-treeselect__option');
    const map = {};
    opts.forEach(opt => {
        const text = opt.innerText.trim();
        const id = opt.id.match(/-(\d+)$/)?.[1];
        if (text && id) map[text] = parseInt(id);
    });
    return map;
}''')
```

**限制**：需要页面有添加员工权限，且部门下拉已加载

---

## 🚀 完整自动化流程

### 用户视角（超简单）
```bash
# 1. 启动浏览器（一次性）
chrome --remote-debugging-port=9222

# 2. 手动登录（30秒）
# 访问财税通 → 输入账号 → 输入密码 → 点击进入企业

# 3. 自动获取配置（1秒）
python auto_config_helper.py
# 自动提取Token、companyId，保存到config.json

# 4. 批量添加员工（秒级）
python caishui_add_staff_api.py employees.xlsx
```

### AI视角（代码实现）
```python
# 1. 连接已登录的浏览器
browser = p.chromium.connect_over_cdp("http://localhost:9222")
page = browser.contexts[0].pages[0]

# 2. 从localStorage提取Token
vuex = json.loads(page.evaluate('localStorage.getItem("vuex")'))
token = vuex['user']['token']
company_id = vuex['user']['userInfo']['companyId']

# 3. 调用API
headers = {"x-token": token}
data = {
    "nickName": "员工姓名",
    "mobile": "手机号",
    "departmentIds": [9151],
    "companyId": company_id
}
response = requests.post(API_URL, headers=headers, json=data)
```

---

## 💡 关键洞察

### 为什么不用开发者工具？
1. **自动化**：Playwright可以直接读取浏览器数据
2. **一体化**：同时获取Token、companyId、用户信息
3. **可复制**：其他OpenClaw可以复用相同代码

### 为什么部门ID需要配置？
1. API权限限制（查询部门列表返回403）
2. 部门ID是数字，映射需要人工确认
3. 不同企业的部门结构不同

---

## 📦 给其他OpenClaw的完整方案

```python
# caishui_add_staff_api.py
import requests
import json
from playwright.sync_api import sync_playwright

def get_token_from_browser():
    """从已登录的浏览器提取Token"""
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        vuex = page.evaluate('() => JSON.parse(localStorage.getItem("vuex") || "{}")')
        return {
            "token": vuex.get('user', {}).get('token'),
            "company_id": vuex.get('user', {}).get('userInfo', {}).get('companyId')
        }

def add_employee(name, phone, dept_id, config):
    """添加单个员工"""
    headers = {"x-token": config["token"]}
    data = {
        "nickName": name,
        "mobile": phone,
        "departmentIds": [dept_id],
        "companyId": config["company_id"]
    }
    response = requests.post(
        "https://cst.uf-tree.com/api/member/userInfo/add",
        headers=headers,
        json=data
    )
    return response.json()

# 使用
config = get_token_from_browser()
result = add_employee("张三", "13800138000", 9151, config)
```

---

## ✅ 总结

**获取Token的核心**：
1. 启动浏览器调试模式 `--remote-debugging-port=9222`
2. 用户手动登录
3. Playwright连接浏览器
4. 从localStorage读取vuex数据
5. 提取 `vuex.user.token` 和 `vuex.user.userInfo.companyId`

**获取部门ID的核心**：
1. 先手动配置映射（测试确认）
2. 或使用浏览器自动化提取（如果API无权限）

这就是完整的自动化方案！🎉
