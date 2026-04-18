"""Execute browser actions resolved from element IDs."""

INTERACTIVE_SELECTORS = (
    "a, button, input, select, textarea, [role='button'], "
    "[role='link'], [role='checkbox'], [role='radio'], [role='tab']"
)


async def execute_action(page, action_name, action_input, elements):
    """Execute a browser action.

    Args:
        page: Playwright page
        action_name: Tool name (click, fill, select_option, navigate, scroll)
        action_input: Tool input dict
        elements: List of element dicts from extract_page_state

    Returns:
        dict with 'success' (bool) and 'message' (str)
    """
    try:
        if action_name == "navigate":
            url = action_input.get("url", "")
            if not url.startswith("http"):
                url = "https://" + url
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            return {"success": True, "message": f"Navigated to {url}"}

        if action_name == "scroll":
            direction = action_input.get("direction", "down")
            amount = 500
            if direction == "down":
                await page.evaluate(f"window.scrollBy(0, {amount})")
            elif direction == "up":
                await page.evaluate(f"window.scrollBy(0, -{amount})")
            return {"success": True, "message": f"Scrolled {direction}"}

        # Actions that require an element
        element_id = action_input.get("element_id")
        if element_id is None:
            return {"success": False, "message": "No element_id provided"}

        element_id = int(element_id)
        if element_id < 0 or element_id >= len(elements):
            return {"success": False, "message": f"Element [{element_id}] not found (max: {len(elements) - 1})"}

        # Locate the element using nth-match on the page
        locator = await _get_element_locator(page, element_id)

        if action_name == "click":
            await locator.click(timeout=5000)
            await page.wait_for_timeout(500)
            return {"success": True, "message": f"Clicked element [{element_id}]"}

        elif action_name == "fill":
            value = action_input.get("value", "")
            await locator.click(timeout=5000)
            await locator.fill(value, timeout=5000)
            return {"success": True, "message": f"Filled element [{element_id}] with '{value}'"}

        elif action_name == "select_option":
            value = action_input.get("value", "")
            await locator.select_option(value=value, timeout=5000)
            return {"success": True, "message": f"Selected '{value}' in element [{element_id}]"}

        else:
            return {"success": False, "message": f"Unknown action: {action_name}"}

    except Exception as e:
        return {"success": False, "message": f"Action failed: {str(e)}"}


async def _get_element_locator(page, element_id):
    """Get a Playwright locator for the nth interactive element."""
    locator = page.locator(INTERACTIVE_SELECTORS)

    # Filter to visible elements and get the nth one
    visible_elements = await page.evaluate(f"""
    () => {{
        const els = document.querySelectorAll("{INTERACTIVE_SELECTORS}");
        const visible = [];
        for (const el of els) {{
            if (!el.offsetParent && el.tagName !== 'BODY' && el.tagName !== 'HTML') continue;
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) continue;
            visible.push(true);
        }}
        return visible.length;
    }}
    """)

    # Use evaluate to click/interact by index
    handle = await page.evaluate_handle(f"""
    () => {{
        const els = document.querySelectorAll("{INTERACTIVE_SELECTORS}");
        let idx = 0;
        for (const el of els) {{
            if (!el.offsetParent && el.tagName !== 'BODY' && el.tagName !== 'HTML') continue;
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) continue;
            if (idx === {element_id}) return el;
            idx++;
        }}
        return null;
    }}
    """)

    element = handle.as_element()
    if not element:
        raise Exception(f"Element [{element_id}] not found or not visible")

    return element
