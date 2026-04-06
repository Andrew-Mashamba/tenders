"""Shared utilities for document tools."""

from pathlib import Path
import json
import sys

PROJECT_DIR = Path("/Volumes/DATA/PROJECTS/TENDERS")
TOOLS_DIR = PROJECT_DIR / "tools"
TEMPLATES_DIR = TOOLS_DIR / "templates"
APPLICATIONS_DIR = PROJECT_DIR / "applications"
INSTITUTIONS_DIR = PROJECT_DIR / "institutions"

VALID_EXTENSIONS = {
    "pdf": [".pdf"],
    "docx": [".docx", ".doc"],
    "xlsx": [".xlsx", ".xls"],
}


def resolve_path(path: str) -> Path:
    """Resolve a path, treating relative paths as relative to PROJECT_DIR."""
    p = Path(path)
    if p.is_absolute():
        return p
    return PROJECT_DIR / p


def validate_file(path: str, expected_type: str | None = None) -> Path:
    """Validate that a file exists and optionally check its extension."""
    p = resolve_path(path)
    if not p.exists():
        print(f"Error: File not found: {p}", file=sys.stderr)
        sys.exit(1)
    if expected_type and p.suffix.lower() not in VALID_EXTENSIONS.get(expected_type, []):
        print(f"Error: Expected {expected_type} file, got {p.suffix}", file=sys.stderr)
        sys.exit(1)
    return p


def safe_output_path(path: str, force: bool = False) -> Path:
    """Resolve output path, warn if file exists."""
    p = resolve_path(path)
    if p.exists() and not force:
        print(f"Warning: Output file exists, will overwrite: {p}", file=sys.stderr)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def print_json(data):
    """Pretty-print data as JSON to stdout."""
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
