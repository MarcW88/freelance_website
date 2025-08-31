import json
from pathlib import Path

def generate_form(config_path: str, output_path: str | None = None) -> str:
    """Generate HTML form based on JSON configuration.

    Args:
        config_path: Path to JSON file with form description.
        output_path: Optional path to write the generated HTML.

    Returns:
        The generated HTML string.
    """
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    styles = config.get("styles", {})
    form_class = styles.get("form_class", "")
    group_class = styles.get("group_class", "")
    input_class = styles.get("input_class", "")
    textarea_class = styles.get("textarea_class", input_class)
    button_class = styles.get("button_class", "")

    html = [
        f'<form id="contact-form" action="{config.get("action", "#")}" '
        f'method="{config.get("method", "post")}" class="{form_class}">' 
    ]

    for field in config.get("fields", []):
        field_type = field.get("type", "text")
        name = field.get("name", "")
        label = field.get("label", "")
        placeholder = field.get("placeholder", "")
        required = " required" if field.get("required", False) else ""

        html.append(f'  <div class="{group_class}">')
        if label:
            html.append(f'    <label for="{name}">{label}</label>')
        if field_type == "textarea":
            html.append(
                f'    <textarea id="{name}" name="{name}" placeholder="{placeholder}"'
                f' class="{textarea_class}"{required}></textarea>'
            )
        else:
            html.append(
                f'    <input id="{name}" type="{field_type}" name="{name}" '
                f'placeholder="{placeholder}" class="{input_class}"{required}/>'
            )
        html.append("  </div>")

    html.append(f'  <button type="submit" class="{button_class}">Envoyer</button>')
    html.append("</form>")

    result = "\n".join(html)
    if output_path:
        Path(output_path).write_text(result, encoding="utf-8")
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate HTML form from JSON config")
    parser.add_argument(
        "--json", default="forms/contact_form.json", help="Path to JSON config"
    )
    parser.add_argument("--out", help="Optional output HTML file")
    args = parser.parse_args()

    generated_html = generate_form(args.json, args.out)
    if not args.out:
        print(generated_html)
