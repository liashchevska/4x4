def is_unique(items: list[str]) -> bool:
    """Check if all items in the list are unique (case-insensitive)."""
    casefolded = {item.casefold() for item in items}
    return len(items) == len(casefolded)
