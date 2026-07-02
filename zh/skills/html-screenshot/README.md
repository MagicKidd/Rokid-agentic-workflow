# HTML 批量截图工具

本工具使用 Playwright 自动化浏览器，实现对 HTML 页面的一键批量截图。支持页面导航切换、子页面跳转、等待时间控制等功能。

## 功能特性

| 功能 | 说明 |
|------|------|
| 批量截图 | 自动遍历所有页面，逐页截图 |
| 页面导航 | 支持侧边栏导航和按钮跳转 |
| 子页面支持 | 可处理弹窗、编辑页等二级页面 |
| 高清输出 | 支持 2x Retina 清晰度 |
| 灵活配置 | 可调整视口大小、等待时间、输出路径 |

## 安装步骤

### 环境要求

- Python 3.8 或更高版本
- macOS / Linux / Windows
- 至少 500MB 磁盘空间（Chromium 浏览器）

### 安装 Playwright

```bash
# 使用 pip 安装
pip install playwright

# 或使用 conda
conda install playwright

# 安装 Chromium 浏览器（约 330MB）
playwright install chromium
```

### 验证安装

```bash
# 检查 Python 包
pip show playwright

# 测试导入
python -c "from playwright.sync_api import sync_playwright; print('OK')"

# 检查浏览器
playwright --version
```

## 快速开始

### 基础用法

```bash
# 进入项目目录
cd /path/to/project

# 直接运行截图脚本
python scripts/screenshot_pages.py
```

### 配置说明

打开 `scripts/screenshot_pages.py`，修改以下配置项：

```python
# HTML 文件配置
HTML_FILE = "P1_配置后台_交互原型.html"

# 输出目录配置
OUTPUT_DIR = "screenshots"

# 视口配置（像素）
VIEWPORT_WIDTH = 1440   # 桌面端宽度
VIEWPORT_HEIGHT = 900   # 桌面端高度

# 页面映射：HTML 元素 ID → 截图文件名
PAGE_NAMES = {
    "text-training": "01_专属模型训练",
    "img-training": "02_多模态识别训练",
    "data-review": "03_人工审核",
    "venue-basic": "04_场馆基础信息",
}
```

### HTML 页面要求

脚本期望 HTML 页面满足以下结构：

```html
<!-- 侧边栏导航使用 data-page 属性 -->
<div class="nav-sub" data-page="page-id">页面名称</div>

<!-- 子页面跳转使用 onclick 属性 -->
<button onclick="enterZoneEdit()">进入编辑</button>
```

## 高级配置

### 视口尺寸

根据目标设备选择合适的视口尺寸：

| 设备类型 | 宽度 | 高度 | 配置示例 |
|----------|------|------|----------|
| 桌面端 | 1440 | 900 | 默认配置 |
| 笔记本 | 1280 | 800 | 降低高度 |
| 平板 | 768 | 1024 | 竖屏平板 |
| 手机 | 375 | 667 | 移动端 |

```python
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800
```

### 页面等待时间

根据页面复杂度调整等待时间：

```python
# 简单页面：0.3 秒
# 复杂页面：1.0 秒以上
time.sleep(0.5)
```

### 自定义选择器

如果 HTML 结构不符合默认格式，可以自定义选择器：

```python
# 修改导航选择器
nav_item = page.query_selector(f'.menu-item[data-target="{page_id}"]')

# 修改按钮选择器
edit_btn = page.query_selector(f'.btn-edit[data-page="{page_id}"]')
```

## 输出示例

### 截图文件列表

```
project/
├── screenshots/
│   ├── 01_专属模型训练.png   (226 KB)
│   ├── 02_多模态识别训练.png   (167 KB)
│   ├── 03_人工审核.png        (267 KB)
│   └── ...
├── index.html
└── scripts/
    └── screenshot_pages.py
```

### 截图质量

| 配置 | 文件大小 | 清晰度 |
|------|----------|--------|
| 1x 分辨率 | 约 100KB | 普通 |
| 2x 分辨率（默认） | 约 200KB | 高清 |
| 全屏截图 | 约 300KB | 完整页面 |

## 常见问题

### 问题一：依赖安装失败

```bash
# 错误信息
ModuleNotFoundError: No module named 'playwright'

# 解决方案
pip install --upgrade pip
pip install playwright
```

### 问题二：浏览器下载超时

```bash
# 使用镜像加速
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
playwright install chromium

# 或手动下载后指定路径
playwright install --with-deps chromium
```

### 问题三：截图不完整

```bash
# 症状：页面底部内容缺失

# 解决方案：增加等待时间
time.sleep(1.0)  # 等待页面完全加载

# 或使用全屏截图
page.screenshot(full_page=True)
```

### 问题四：字体显示异常

```bash
# 检查 HTML 编码
# 确保文件保存为 UTF-8 编码

# 在 HTML 头部指定字体
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="fonts.css">
</head>
```

### 问题五：页面元素找不到

```bash
# 症状：NoSuchElementError

# 调试方法：在浏览器控制台测试选择器
document.querySelector('.nav-sub[data-page="page-id"]')

# 解决方案：更新选择器
nav_item = page.query_selector('button.primary')
```

## 最佳实践

### 项目结构

建议将截图工具集成到项目中：

```
project/
├── .cursor/
│   └── skills/
│       └── html-screenshot/
│           ├── SKILL.md
│           ├── README.md
│           └── scripts/
│               └── screenshot_pages.py
├── docs/
│   └── screenshots/
├── src/
└── tests/
```

### 截图时机

| 场景 | 推荐时机 |
|------|----------|
| UI 变更后 | 立即截图存档 |
| 版本发布前 | 全量截图 |
| 文档更新时 | 按需截图 |
| 自动化测试 | 失败时截图 |

### 命名规范

采用「序号_页面名称」格式：

```
01_首页.png
02_登录页.png
03_注册页.png
...
10_设置页.png
```

## 脚本源码

完整脚本源码见 [scripts/screenshot_pages.py](scripts/screenshot_pages.py)。

### 核心代码解析

```python
def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = context.new_page()

        # 打开 HTML 文件
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")

        # 遍历页面截图
        for page_id, name in PAGE_NAMES.items():
            # 切换页面
            nav_item = page.query_selector(f'.nav-sub[data-page="{page_id}"]')
            nav_item.click()
            time.sleep(0.5)

            # 截图
            page.screenshot(
                path=f"{OUTPUT_DIR}/{name}.png",
                full_page=True,
            )
```

## 相关资源

- Playwright 官方文档：https://playwright.dev/python/
- Python 截图示例：https://playwright.dev/python/docs/screenshots
- Cursor Skills 指南：https://cursor.sh/docs/skills

## 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-02-11 | 初始版本，支持批量截图 |
