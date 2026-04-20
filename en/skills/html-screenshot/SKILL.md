---
name: html-screenshot
description: Batch-screenshot HTML interactive prototype pages. Uses Playwright to open an HTML file, walk through pages, and save full-viewport screenshots. Fits Pencil design exports, HTML prototype documentation, UI page archival. Trigger words: screenshot HTML, prototype screenshots, batch capture pages.
---

# HTML Batch Screenshot

## Quick start

When the user needs batch screenshots of HTML pages:

1. Confirm the HTML file path
2. Run the screenshot script
3. Pick up the images from the output directory

## Usage

```bash
cd path/to/project

# First-time setup
pip install playwright
playwright install chromium

# Run
python scripts/screenshot_pages.py
```

## Script config

Edit the constants at the top of the script:

```python
HTML_FILE = "P1_config_prototype.html"   # HTML filename
OUTPUT_DIR = "screenshots"                # output dir
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900
PAGE_NAMES = {                            # page-id → display name
    "page-id": "Page Name",
}
```

## Output format

Filename pattern: `{index}_{page-name}.png`

Example:
```
screenshots/
├── 01_dashboard.png
├── 02_model-training.png
└── 13_reference-library.png
```

## Handling special pages

For child pages reached via button (modals, edit views), special-case them in the script:

```python
if page_id == "indoor-zone-edit":
    # switch to parent page first
    nav_item = page.query_selector('.nav-sub[data-page="indoor-loc"]')
    nav_item.click()
    time.sleep(0.5)
    # click into child page
    edit_btn = page.query_selector('button[onclick="enterZoneEdit()"]')
    edit_btn.click()
    time.sleep(0.5)
```

## Install

```bash
pip install playwright
playwright install chromium
python -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## Troubleshooting

| Problem | Fix |
|---|---|
| Page not found | Check the CSS selector in the HTML |
| Blank screenshot | Increase `time.sleep(0.5)` |
| Viewport too small | Tune `VIEWPORT_WIDTH` / `VIEWPORT_HEIGHT` |
| Font glitches | Ensure HTML file is UTF-8 |

## Advanced

### Capture a specific element

```python
element = page.query_selector('.content')
element.screenshot(path="element.png")
```

### Full-page (scrolling) capture

```python
page.screenshot(full_page=True)
```

## Further reading

- Script readme: [README.md](README.md)
- Source: [scripts/screenshot_pages.py](scripts/screenshot_pages.py)
