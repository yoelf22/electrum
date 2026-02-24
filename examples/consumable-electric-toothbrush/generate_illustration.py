#!/usr/bin/env python3
"""
Generate a cross-section illustration of the Consumable Electric Toothbrush
using ChatGPT's DALL-E via Playwright browser automation.

First run: browser opens, user logs into ChatGPT manually.
Subsequent runs: session persists (persistent browser profile).

Usage:
    python3 generate_illustration.py
"""

import base64
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout

# --- Config ---
PROFILE_DIR = os.path.expanduser("~/.chatgpt_playwright_profile")
CHATGPT_URL = "https://chatgpt.com/"
LOGIN_TIMEOUT_S = 180  # 3 minutes for manual login
GENERATION_TIMEOUT_S = 180  # 3 minutes for image generation
POLL_INTERVAL_S = 2

SCRIPT_DIR = Path(__file__).resolve().parent
DESIGN_FILES = [
    SCRIPT_DIR / "high_level_design.md",
    SCRIPT_DIR / "component_arrangement.md",
]
OUTPUT_FILE = SCRIPT_DIR / "cross_section_illustration_consumable_toothbrush.png"

PROMPT_PREFIX = """Create two illustrations of a consumable electric toothbrush product:

1. A detailed LONGITUDINAL CROSS-SECTION showing all internal components: AAA battery at the base with spring contact, latching push-button switch at mid-handle, cylindrical ERM vibration motor (axial orientation), eccentric mass, rigid PP linkage arm, TPE boot seal at the neck, and the split bristle head (one fixed half, one moving half connected via living hinge). Show the dual-injection construction: rigid PP inner body (white/light gray) with TPE overmold (blue/teal) covering the grip, button area, and head joint. Show the O-ring sealed threaded battery cap at the base. Label all components clearly.

2. An ISOMETRIC ARTIST CONCEPT showing the finished product exterior — a sleek, ergonomic toothbrush handle (~160mm long, ~15mm diameter) with visible TPE grip texture, a subtle button area at thumb position, and the split bristle head at the top. Clean, consumer-product rendering style.

Here are the design documents:

"""

# Selector fallback chains — ordered by reliability
SELECTORS = {
    "prompt_input": [
        "#prompt-textarea",
        "div[contenteditable='true']",
    ],
    "send_button": [
        "button[data-testid='send-button']",
        "button[aria-label='Send prompt']",
        "button[aria-label='Send message']",
    ],
    "stop_button": [
        "button[aria-label='Stop generating']",
        "button[data-testid='stop-button']",
    ],
    "completion": [
        "article:last-child button[aria-label='Copy']",
        "[data-testid*='conversation-turn']:last-child button[aria-label='Copy']",
    ],
}


def find_element(page, name, timeout_ms=5000):
    """Try each selector in the fallback chain for `name`. Return first match."""
    selectors = SELECTORS[name]
    for sel in selectors:
        try:
            el = page.wait_for_selector(sel, timeout=timeout_ms, state="visible")
            if el:
                print(f"  [{name}] matched: {sel}")
                return el
        except PwTimeout:
            continue
    return None


def dismiss_desktop_app_prompt(page):
    """Dismiss the 'Open in desktop app' prompt that ChatGPT shows."""
    dismiss_selectors = [
        "button:has-text('Stay in browser')",
        "button:has-text('Continue in browser')",
        "button:has-text('Use browser')",
        "button:has-text('No thanks')",
        "button:has-text('Dismiss')",
        "a:has-text('Stay in browser')",
        "a:has-text('Continue in browser')",
    ]
    for sel in dismiss_selectors:
        try:
            btn = page.query_selector(sel)
            if btn:
                btn.click()
                print(f"Dismissed desktop app prompt: {sel}")
                page.wait_for_timeout(1000)
                return
        except Exception:
            continue

    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    except Exception:
        pass


def wait_for_login(page):
    """Always go through login flow first, then wait until logged in."""
    print("Navigating to login page...")
    page.goto("https://chatgpt.com/auth/login", wait_until="domcontentloaded", timeout=30000)
    print("Please log in manually in the browser window.")
    print(f"Waiting up to {LOGIN_TIMEOUT_S}s for login to complete...")

    deadline = time.time() + LOGIN_TIMEOUT_S
    while time.time() < deadline:
        try:
            url = page.url
        except Exception:
            time.sleep(POLL_INTERVAL_S)
            continue

        on_chatgpt = "chatgpt.com" in url and "/auth/" not in url and "accounts.google" not in url
        if on_chatgpt:
            try:
                page.keyboard.press("Escape")
            except Exception:
                pass
            page.wait_for_timeout(1000)

            modal = page.query_selector("#modal-no-auth-login, [data-testid='modal-no-auth-login']")
            if not modal:
                el = find_element(page, "prompt_input", timeout_ms=3000)
                if el:
                    print("Login confirmed.")
                    return
                else:
                    print("  On chatgpt.com but prompt input not found yet...")
        time.sleep(POLL_INTERVAL_S)

    print("ERROR: Login timeout. Exiting.")
    sys.exit(1)


def build_prompt():
    """Build the full prompt with design file contents inlined."""
    content_parts = []
    for f in DESIGN_FILES:
        if not f.exists():
            print(f"ERROR: Design file not found: {f}")
            sys.exit(1)
        content_parts.append(f.read_text(encoding="utf-8"))

    combined = "\n\n---\n\n".join(content_parts)
    full_prompt = PROMPT_PREFIX + combined
    print(f"Prompt length: {len(full_prompt)} chars")
    return full_prompt


def type_and_send(page, prompt_text):
    """Paste the prompt into the input and send it."""
    input_el = find_element(page, "prompt_input", timeout_ms=10000)
    if not input_el:
        print("ERROR: Could not find prompt input.")
        sys.exit(1)

    input_el.click()
    page.wait_for_timeout(300)

    page.evaluate("""(text) => {
        const el = document.querySelector('#prompt-textarea') ||
                   document.querySelector("div[contenteditable='true']");
        if (el) {
            el.focus();
            document.execCommand('insertText', false, text);
        }
    }""", prompt_text)
    print(f"Pasted prompt ({len(prompt_text)} chars)")
    page.wait_for_timeout(1000)

    send_btn = find_element(page, "send_button", timeout_ms=3000)
    if send_btn:
        send_btn.click()
        print("Clicked send button.")
    else:
        print("Send button not found, pressing Enter.")
        page.keyboard.press("Enter")

    page.wait_for_timeout(1000)


def wait_for_generation(page):
    """Wait for DALL-E to finish by watching for the spinning/loading indicator to stop."""
    print("Waiting for generation to complete...")
    start = time.time()
    deadline = time.time() + GENERATION_TIMEOUT_S

    while time.time() < deadline:
        spinners = page.evaluate("""() => {
            const results = [];
            const all = document.querySelectorAll('*');
            for (const el of all) {
                const style = window.getComputedStyle(el);
                const anim = style.animationName || '';
                if (anim && anim !== 'none') {
                    const tag = el.tagName.toLowerCase();
                    const cls = (el.className && typeof el.className === 'string') ?
                                 el.className.substring(0, 80) : '';
                    const id = el.id || '';
                    const role = el.getAttribute('role') || '';
                    const ariaLabel = el.getAttribute('aria-label') || '';
                    const testId = el.getAttribute('data-testid') || '';
                    const size = el.getBoundingClientRect();
                    results.push({
                        tag, cls, id, role, ariaLabel, testId,
                        anim,
                        w: Math.round(size.width),
                        h: Math.round(size.height)
                    });
                }
            }
            return results;
        }""")

        elapsed = int(time.time() - start)
        if spinners:
            print(f"  [{elapsed}s] Found {len(spinners)} animated element(s):")
            for s in spinners:
                print(f"    <{s['tag']}> anim={s['anim']} {s['w']}x{s['h']} "
                      f"class={s['cls'][:60]} id={s['id']} role={s['role']} "
                      f"aria-label={s['ariaLabel']} data-testid={s['testId']}")
        else:
            print(f"  [{elapsed}s] No animated elements found.")

        time.sleep(3)

    print("DEBUG: timeout reached.")


def find_and_download_image(page):
    """Find the generated image in the last response and download it."""
    img_selectors = [
        "article:last-child img[src*='oaidalleapiprodscus']",
        "article:last-child img[src*='dalle']",
        "[data-testid*='conversation-turn']:last-child img[src*='dalle']",
        "article:last-child img[alt]",
        "[data-testid*='conversation-turn']:last-child img",
    ]

    img_el = None
    for sel in img_selectors:
        candidates = page.query_selector_all(sel)
        for c in candidates:
            box = c.bounding_box()
            if box and box["width"] > 100 and box["height"] > 100:
                img_el = c
                print(f"  Found image via: {sel}")
                break
        if img_el:
            break

    if not img_el:
        print("  Trying broad image search...")
        for img in page.query_selector_all("img"):
            box = img.bounding_box()
            if box and box["width"] > 200 and box["height"] > 200:
                src = img.get_attribute("src") or ""
                if "avatar" not in src and "logo" not in src:
                    img_el = img
                    print(f"  Found large image (broad search): {src[:80]}")
                    break

    if not img_el:
        all_imgs = page.query_selector_all("img")
        print(f"  DEBUG: Found {len(all_imgs)} total <img> elements on page:")
        for i, img in enumerate(all_imgs):
            src = (img.get_attribute("src") or "")[:100]
            box = img.bounding_box()
            size_str = f"{box['width']:.0f}x{box['height']:.0f}" if box else "hidden"
            print(f"    [{i}] {size_str} — {src}")

        debug_info = page.evaluate("""() => {
            const info = {};
            info.canvases = document.querySelectorAll('canvas').length;
            info.totalImages = document.querySelectorAll('img').length;
            const articles = document.querySelectorAll('article, [data-testid*="conversation-turn"]');
            info.articleCount = articles.length;
            const lastArticle = articles[articles.length - 1];
            if (lastArticle) {
                info.lastArticleHTML = lastArticle.innerHTML.substring(0, 10000);
                const allEls = lastArticle.querySelectorAll('*');
                const srcs = [];
                for (const el of allEls) {
                    for (const attr of el.attributes) {
                        if (attr.value && (attr.value.includes('http') || attr.value.includes('blob:') || attr.value.includes('data:'))) {
                            srcs.push(`${el.tagName}.${attr.name}=${attr.value.substring(0, 150)}`);
                        }
                    }
                }
                info.urlAttributes = srcs;
            }
            const allImgs = document.querySelectorAll('img');
            info.allImgSrcs = Array.from(allImgs).map(img => {
                const src = img.src || '';
                const box = img.getBoundingClientRect();
                return `${box.width.toFixed(0)}x${box.height.toFixed(0)} ${src.substring(0, 120)}`;
            });
            return info;
        }""")
        print(f"  DEBUG DOM info:")
        for k, v in debug_info.items():
            if k == "lastArticleHTML":
                print(f"    {k}: {str(v)[:500]}")
            else:
                print(f"    {k}: {v}")

        print("ERROR: No generated image found.")
        sys.exit(1)

    src = img_el.get_attribute("src") or ""
    print(f"Image src: {src[:120]}...")

    if src.startswith("blob:"):
        print("Blob URL detected — extracting via canvas...")
        data_url = page.evaluate("""(img) => {
            const canvas = document.createElement('canvas');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            return canvas.toDataURL('image/png');
        }""", img_el)
        if not data_url or not data_url.startswith("data:image"):
            print("ERROR: Canvas extraction failed.")
            sys.exit(1)
        b64 = data_url.split(",", 1)[1]
        image_bytes = base64.b64decode(b64)
    else:
        print("Downloading via page.request.get()...")
        response = page.request.get(src)
        if response.status != 200:
            print(f"ERROR: Download failed with status {response.status}")
            sys.exit(1)
        image_bytes = response.body()

    OUTPUT_FILE.write_bytes(image_bytes)
    size_kb = len(image_bytes) / 1024
    print(f"Saved: {OUTPUT_FILE} ({size_kb:.0f} KB)")


def main():
    print("=" * 60)
    print("ChatGPT DALL-E Illustration Generator")
    print("Consumable Electric Toothbrush")
    print("=" * 60)

    # Clean up stale lock files that cause crashes after unclean shutdown
    for lock_file in ["SingletonLock", "SingletonCookie", "SingletonSocket"]:
        lock_path = Path(PROFILE_DIR) / lock_file
        if lock_path.exists():
            lock_path.unlink()
            print(f"Removed stale lock: {lock_file}")

    with sync_playwright() as p:
        print(f"Launching browser (profile: {PROFILE_DIR})...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )

        page = context.pages[0] if context.pages else context.new_page()

        print(f"Navigating to {CHATGPT_URL}...")
        page.goto(CHATGPT_URL, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)

        dismiss_desktop_app_prompt(page)

        wait_for_login(page)
        page.wait_for_timeout(1000)

        dismiss_desktop_app_prompt(page)

        print("\n--- Building prompt ---")
        full_prompt = build_prompt()

        print("\n--- Sending prompt ---")
        type_and_send(page, full_prompt)

        print("\n--- Waiting for image generation ---")
        wait_for_generation(page)

        print("\n--- Downloading image ---")
        find_and_download_image(page)

        print("\nDone. Closing browser in 5s...")
        page.wait_for_timeout(5000)
        context.close()

    print("Finished.")


if __name__ == "__main__":
    main()
