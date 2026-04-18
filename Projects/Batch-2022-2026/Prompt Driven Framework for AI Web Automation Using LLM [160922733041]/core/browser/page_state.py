"""DOM extraction and element indexing for the AI agent."""

INTERACTIVE_SELECTORS = (
    "a, button, input, select, textarea, [role='button'], "
    "[role='link'], [role='checkbox'], [role='radio'], [role='tab']"
)


async def extract_page_state(page):
    """Extract current page state: URL, title, interactive elements, visible text."""
    url = page.url
    title = await page.title()

    elements = await page.evaluate(f"""
    () => {{
        const els = document.querySelectorAll("{INTERACTIVE_SELECTORS}");
        const results = [];
        let idx = 0;
        for (const el of els) {{
            if (!el.offsetParent && el.tagName !== 'BODY' && el.tagName !== 'HTML') continue;
            const rect = el.getBoundingClientRect();
            if (rect.width === 0 && rect.height === 0) continue;

            const tag = el.tagName.toLowerCase();
            const role = el.getAttribute('role') || '';
            const text = (el.innerText || el.textContent || '').trim().substring(0, 80);
            const name = el.getAttribute('name') || '';
            const placeholder = el.getAttribute('placeholder') || '';
            const href = el.getAttribute('href') || '';
            const elType = el.getAttribute('type') || '';
            const value = el.value || '';
            const ariaLabel = el.getAttribute('aria-label') || '';
            const id_attr = el.getAttribute('id') || '';

            let options = [];
            if (tag === 'select') {{
                for (const opt of el.options) {{
                    options.push({{ value: opt.value, text: opt.text.trim() }});
                }}
            }}

            results.push({{
                idx: idx,
                tag: tag,
                role: role,
                type: elType,
                text: text,
                name: name,
                placeholder: placeholder,
                href: href,
                value: value,
                ariaLabel: ariaLabel,
                id_attr: id_attr,
                options: options
            }});
            idx++;
        }}
        return results;
    }}
    """)

    visible_text = await page.evaluate("""
    () => {
        const body = document.body;
        if (!body) return '';
        const text = body.innerText || body.textContent || '';
        return text.substring(0, 1200);
    }
    """)

    return {
        "url": url,
        "title": title,
        "elements": elements,
        "visible_text": visible_text.strip(),
    }


def format_state_for_llm(state):
    """Format page state into a compact text for the LLM."""
    lines = []
    lines.append(f"Page: {state['title']}")
    lines.append(f"URL: {state['url']}")
    lines.append("")
    lines.append("Interactive Elements:")

    for el in state["elements"]:
        idx = el["idx"]
        tag = el["tag"]
        el_type = el.get("type", "")
        role = el.get("role", "")
        text = el.get("text", "")
        name = el.get("name", "")
        placeholder = el.get("placeholder", "")
        href = el.get("href", "")
        value = el.get("value", "")
        aria = el.get("ariaLabel", "")
        options = el.get("options", [])

        # Build compact description
        label = text[:40] or aria[:40] or name or placeholder or ""
        if tag == "a":
            desc = f'[{idx}] link "{label or href[:40]}"'
        elif tag == "button" or role == "button":
            desc = f'[{idx}] btn "{label or "button"}"'
        elif tag == "input":
            desc = f"[{idx}] {el_type or 'text'}"
            if name: desc += f' n="{name}"'
            elif placeholder: desc += f' p="{placeholder[:30]}"'
            elif aria: desc += f' l="{aria[:30]}"'
            if value: desc += f' v="{value[:20]}"'
        elif tag == "select":
            desc = f"[{idx}] select"
            if name: desc += f' n="{name}"'
            elif aria: desc += f' l="{aria[:30]}"'
            if options:
                opt_strs = [o["text"][:20] for o in options[:6]]
                desc += f' opts=[{",".join(opt_strs)}]'
            if value: desc += f' v="{value[:20]}"'
        elif tag == "textarea":
            desc = f"[{idx}] textarea"
            if name: desc += f' n="{name}"'
            elif placeholder: desc += f' p="{placeholder[:30]}"'
        else:
            desc = f'[{idx}] {tag} "{label}"'

        lines.append(desc)

    lines.append("")
    lines.append("Visible Text:")
    lines.append(state["visible_text"][:800])

    return "\n".join(lines)
