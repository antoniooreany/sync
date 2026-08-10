from typing import Iterable

def infer_type_label(filenames: Iterable[str]) -> str:
    """Infer a single type:* label from changed paths."""
    paths = list(filenames)

    if any(p.startswith(".github/workflows/") for p in paths):
        return "type:ci"
    if any(p.startswith("docs/") or p.endswith(".md") for p in paths):
        return "type:docs"
    if any(p.startswith("tests/") for p in paths):
        return "type:test"
    if any(p.startswith("src/") for p in paths):
        return "type:feat"

    return "type:chore"

def infer_area_labels(filenames: Iterable[str]) -> list[str]:
    """Infer one or more area:* labels from changed paths."""
    areas: set[str] = set()
    for path in filenames:
        if path.startswith(".github/workflows/"):
            areas.add("area:ci")
        if path.startswith("docs/") or path.endswith(".md"):
            areas.add("area:docs")
        if path.startswith("tests/"):
            areas.add("area:tests")
        if path.startswith("src/"):
            areas.add("area:core")
    if not areas:
        areas.add("area:misc")
    return sorted(areas)
