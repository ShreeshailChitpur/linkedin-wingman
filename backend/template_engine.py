from pathlib import Path
import yaml


TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_template(key: str) -> dict:
    template_path = TEMPLATES_DIR / f"{key}.yaml"

    if not template_path.exists():
        raise ValueError(f"Template '{key}' does not exist")

    with open(template_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_required_slots(key: str) -> list[str]:
    template = load_template(key)
    return template.get("slots", [])


def fill_slots(template: dict, values: dict) -> str:
    required_slots = template.get("slots", [])

    missing = [
        slot
        for slot in required_slots
        if not values.get(slot)
    ]

    if missing:
        raise ValueError(
            f"Missing required slots: {', '.join(missing)}"
        )

    return template["template"].format_map(values)


def list_templates() -> list[str]:
    return sorted(
        path.stem
        for path in TEMPLATES_DIR.glob("*.yaml")
    )


if __name__ == "__main__":

    dummy_values = {
        "name": "John Doe",
        "role": "Software Engineer",
        "company": "Google",
        "focus_area": "Cloud Engineering",
        "their_background": "B2B SaaS Sales",
    }

    for template_key in list_templates():

        print("=" * 60)
        print(f"TEMPLATE: {template_key}")

        template = load_template(template_key)

        print("Required Slots:")
        print(get_required_slots(template_key))

        print("\nRendered Output:\n")

        rendered = fill_slots(
            template,
            dummy_values,
        )

        print(rendered)
        print()