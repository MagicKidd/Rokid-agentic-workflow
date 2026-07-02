#!/usr/bin/env python3
"""
HTML 页面批量截图工具
使用 Playwright 自动化浏览器，逐页切换并保存 HTML 页面的全屏截图。
适用于 UI 设计稿导出、原型文档化、页面存档等场景。
功能特性：
- 自动遍历页面列表，逐页截图
- 支持侧边栏导航和按钮跳转
- 可配置视口尺寸和截图清晰度
- 支持子页面（弹窗、编辑页）截图
- 完善的错误处理和进度显示
使用前请确保已安装 Playwright：
    pip install playwright
    playwright install chromium
作者：AI Assistant
日期：2026-02-11
"""
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("错误：未安装 Playwright。请先安装：")
    print("    pip install playwright")
    print("    playwright install chromium")
    sys.exit(1)

# ==================== 配置区域 ====================
# HTML 文件配置
HTML_FILE = "P1_配置后台_交互原型.html"
# 输出目录配置
OUTPUT_DIR = "screenshots"
# 视口配置（像素）
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900
# 截图清晰度：1=普通，2=高清
DEVICE_SCALE_FACTOR = 2
# 页面切换等待时间（秒）
PAGE_WAIT_TIME = 0.5
# 页面映射：HTML 元素 ID → 截图文件名
PAGE_NAMES: Dict[str, str] = {
    "text-training": "01_专属模型训练",
    "img-training": "02_多模态识别训练",
    "data-review": "03_人工审核",
    "venue-basic": "04_场馆基础信息",
    "desc-model": "05_描述模型配置",
    "exhibit-tags": "06_展品运营标签",
    "op-info": "07_运营信息配置",
    "indoor-loc": "08_室内位置配置",
    "indoor-zone-edit": "09_室内位置_点位配置",
    "outdoor-nav": "10_室外导航地图",
    "hotwords": "11_热词配置",
    "rare-char": "12_生僻字替换",
    "sample-lib": "13_参考资料库",
}

def create_output_dir() -> Path:
    """创建输出目录"""
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path

def get_html_path() -> Path:
    """获取 HTML 文件绝对路径"""
    script_dir = Path(__file__).parent.parent
    html_path = script_dir / HTML_FILE
    if not html_path.exists():
        cwd_html = Path.cwd() / HTML_FILE
        if cwd_html.exists():
            html_path = cwd_html
    return html_path.resolve()

def get_browser_context(playwright) -> Tuple:
    """创建浏览器上下文和页面"""
    context = playwright.chromium.launch(headless=True).new_context(
        viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
        device_scale_factor=DEVICE_SCALE_FACTOR,
    )
    page = context.new_page()
    return context, page

def load_html_page(page: object, html_path: Path) -> bool:
    """加载 HTML 页面"""
    file_url = f"file://{html_path}"
    page.goto(file_url)
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
        return True
    except Exception:
        print(f"警告：页面加载超时，尝试继续...")
        return True

def navigate_to_page(page: object, page_id: str, page_name: str) -> bool:
    """导航到指定页面"""
    if page_id == "indoor-zone-edit":
        parent_nav = page.query_selector('.nav-sub[data-page="indoor-loc"]')
        if parent_nav:
            parent_nav.click()
            time.sleep(PAGE_WAIT_TIME)
        else:
            print(f"错误：找不到父页面导航项 indoor-loc")
            return False
        edit_btn = page.query_selector('button[onclick="enterZoneEdit()"]')
        if edit_btn:
            edit_btn.click()
            time.sleep(PAGE_WAIT_TIME)
        else:
            print(f"错误：找不到进入区域编辑按钮")
            return False
        return True
    nav_item = page.query_selector(f'.nav-sub[data-page="{page_id}"]')
    if nav_item:
        nav_item.click()
        time.sleep(PAGE_WAIT_TIME)
        return True
    else:
        print(f"警告：找不到页面 {page_name} 的导航元素（ID: {page_id}）")
        return False

def take_screenshot(page: object, output_path: Path, page_name: str) -> bool:
    """截取当前页面"""
    filename = f"{page_name}.png"
    filepath = output_path / filename
    try:
        page.screenshot(path=str(filepath), full_page=True)
        return True
    except Exception as e:
        print(f"错误：截图失败 - {e}")
        return False

def print_banner():
    """打印横幅信息"""
    print("=" * 60)
    print("HTML 页面批量截图工具")
    print("=" * 60)
    print()

def print_summary(total: int, success: int, failed: int, output_path: Path, elapsed_time: float):
    """打印执行摘要"""
    print()
    print("=" * 60)
    print(f"📊 截图完成：{success}/{total} 个页面")
    print(f"⏱️  用时：{elapsed_time:.1f} 秒")
    print("=" * 60)
    if failed > 0:
        print()
        print(f"⚠️  以下页面截图失败：")
    print()
    print(f"📁 截图保存在：{output_path}/")

def run_screenshots(html_file: Optional[str] = None, output_dir: Optional[str] = None,
                    viewport_width: Optional[int] = None, viewport_height: Optional[int] = None) -> Dict[str, bool]:
    """执行批量截图"""
    if html_file:
        globals()["HTML_FILE"] = html_file
    if output_dir:
        globals()["OUTPUT_DIR"] = output_dir
    if viewport_width:
        globals()["VIEWPORT_WIDTH"] = viewport_width
    if viewport_height:
        globals()["VIEWPORT_HEIGHT"] = viewport_height

    print_banner()
    html_path = get_html_path()
    if not html_path.exists():
        print(f"错误：找不到 HTML 文件：{html_path}")
        print()
        print("请确认 HTML 文件存在于脚本同目录或当前工作目录")
        return {}

    print(f"📄 HTML 文件：{html_path}")
    print(f"📁 输出目录：{OUTPUT_DIR}")
    print(f"📐 视口大小：{VIEWPORT_WIDTH} x {VIEWPORT_HEIGHT}")
    print()

    output_path = create_output_dir()
    results: Dict[str, bool] = {}
    start_time = time.time()

    try:
        with sync_playwright() as p:
            context, page = get_browser_context(p)
            if not load_html_page(page, html_path):
                print("错误：页面加载失败")
                return {}
            print("✅ 页面加载完成")
            print()

            for page_id, page_name in PAGE_NAMES.items():
                print(f"📸 {page_name}...", end=" ")
                if not navigate_to_page(page, page_id, page_name):
                    print("⏭️  跳过")
                    results[page_id] = False
                    continue
                if take_screenshot(page, output_path, page_name):
                    file_size = (output_path / f"{page_name}.png").stat().st_size
                    print(f"✅ ({file_size // 1024} KB)")
                    results[page_id] = True
                else:
                    print("❌ 失败")
                    results[page_id] = False
            context.close()

    except KeyboardInterrupt:
        print()
        print("用户中断执行")
        return results
    except Exception as e:
        print(f"错误：{e}")
        return results

    elapsed_time = time.time() - start_time
    success_count = sum(results.values())
    total_count = len(results)
    print_summary(total=total_count, success=success_count, failed=total_count - success_count,
                  output_path=output_path, elapsed_time=elapsed_time)
    return results

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="HTML 页面批量截图工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例：
  python screenshot_pages.py                          # 使用默认配置
  python screenshot_pages.py --output-dir my-screens   # 指定输出目录
  python screenshot_pages.py --html-file demo.html     # 指定 HTML 文件
  python screenshot_pages.py --viewport 1920 1080      # 指定视口大小""")
    parser.add_argument("-o", "--output-dir", type=str, help=f"输出目录（默认：{OUTPUT_DIR}）")
    parser.add_argument("-f", "--html-file", type=str, help=f"HTML 文件名（默认：{HTML_FILE}）")
    parser.add_argument("-w", "--width", type=int, help=f"视口宽度像素（默认：{VIEWPORT_WIDTH}）")
    parser.add_argument("-H", "--height", type=int, help=f"视口高度像素（默认：{VIEWPORT_HEIGHT}）")
    parser.add_argument("-v", "--version", action="version", version="screenshot_pages.py 1.0.0")
    return parser.parse_args()

def main():
    """主函数"""
    args = parse_args()
    run_screenshots(html_file=args.html_file, output_dir=args.output_dir,
                    viewport_width=args.width, viewport_height=args.height)

if __name__ == "__main__":
    main()
