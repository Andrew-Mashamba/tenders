"""CLI entry point for document tools."""

import argparse
import json
import sys
from pathlib import Path


def parse_pages(pages_str: str) -> list[int]:
    """Parse page specification like '1-3,5,8-10' into a list of ints."""
    pages = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            pages.extend(range(int(start), int(end) + 1))
        else:
            pages.append(int(part))
    return pages


def parse_page_ranges(pages_str: str) -> list[tuple[int, int]]:
    """Parse page ranges like '1-3,5-5,8-10' into list of (start, end) tuples."""
    ranges = []
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            ranges.append((int(start), int(end)))
        else:
            n = int(part)
            ranges.append((n, n))
    return ranges


def cmd_pdf_read(args):
    from tools.pdf.reader import extract_text, extract_tables, get_metadata
    if args.metadata:
        from tools.utils import print_json
        print_json(get_metadata(args.file))
    elif args.tables:
        from tools.utils import print_json
        pages = parse_pages(args.pages) if args.pages else None
        print_json(extract_tables(args.file, pages))
    else:
        pages = parse_pages(args.pages) if args.pages else None
        print(extract_text(args.file, pages))


def cmd_pdf_merge(args):
    from tools.pdf.merger import merge
    result = merge(args.files, args.output)
    print(f"Merged {len(args.files)} files → {result}")


def cmd_pdf_split(args):
    from tools.pdf.merger import split, extract_pages
    if args.pages:
        pages = parse_pages(args.pages)
        result = extract_pages(args.file, pages, args.output)
    else:
        ranges = parse_page_ranges(args.ranges)
        result = split(args.file, ranges, args.output)
    print(f"Split → {result}")


def cmd_pdf_forms_read(args):
    from tools.pdf.forms import read_fields
    from tools.utils import print_json
    print_json(read_fields(args.file))


def cmd_pdf_forms_fill(args):
    from tools.pdf.forms import fill_form
    with open(args.data) as f:
        data = json.load(f)
    result = fill_form(args.file, data, args.output, flatten=args.flatten)
    print(f"Filled form → {result}")


def cmd_pdf_create(args):
    if args.type == "proposal":
        from tools.pdf.creator import create_proposal
        with open(args.data) as f:
            data = json.load(f)
        result = create_proposal(data, args.output)
    elif args.type == "letter":
        from tools.pdf.creator import create_cover_letter
        with open(args.data) as f:
            data = json.load(f)
        result = create_cover_letter(data, args.output)
    elif args.type == "table":
        from tools.pdf.creator import create_table_pdf
        with open(args.data) as f:
            data = json.load(f)
        result = create_table_pdf(data["headers"], data["rows"], args.output,
                                  title=data.get("title", ""))
    else:
        from tools.pdf.creator import create_from_text
        text = sys.stdin.read() if args.data == "-" else Path(args.data).read_text()
        result = create_from_text(text, args.output, title=args.title or "")
    print(f"Created → {result}")


def cmd_docx_read(args):
    if args.format == "json":
        from tools.docx.reader import extract_structure
        from tools.utils import print_json
        print_json(extract_structure(args.file))
    elif args.tables:
        from tools.docx.reader import extract_tables
        from tools.utils import print_json
        print_json(extract_tables(args.file))
    else:
        from tools.docx.reader import extract_text
        print(extract_text(args.file))


def cmd_docx_create(args):
    with open(args.data) as f:
        data = json.load(f)
    if args.template:
        from tools.docx.creator import create_from_template
        result = create_from_template(args.template, data, args.output)
    elif args.type == "letter":
        from tools.docx.creator import create_cover_letter
        result = create_cover_letter(data, args.output)
    else:
        from tools.docx.creator import create_proposal
        result = create_proposal(data, args.output)
    print(f"Created → {result}")


def cmd_docx_edit(args):
    from tools.docx.editor import find_replace
    replacements = json.loads(args.replace)
    result = find_replace(args.file, replacements, args.output)
    print(f"Edited → {result}")


def cmd_docx_to_pdf(args):
    from tools.docx.converter import to_pdf
    result = to_pdf(args.file, args.output)
    print(f"Converted → {result}")


def cmd_xlsx_read(args):
    if args.format == "json":
        from tools.xlsx.reader import extract_data
        from tools.utils import print_json
        print_json(extract_data(args.file, args.sheet))
    else:
        from tools.xlsx.reader import extract_text
        print(extract_text(args.file, args.sheet))


def cmd_xlsx_create(args):
    with open(args.data) as f:
        data = json.load(f)
    from tools.xlsx.creator import create_from_data
    result = create_from_data(data, args.output)
    print(f"Created → {result}")


def cmd_xlsx_edit(args):
    if args.cell and args.value:
        from tools.xlsx.editor import update_cell
        result = update_cell(args.file, args.sheet or "Sheet1", args.cell, args.value, args.output)
    elif args.data:
        from tools.xlsx.editor import update_cells
        with open(args.data) as f:
            updates = json.load(f)
        result = update_cells(args.file, args.sheet or "Sheet1", updates, args.output)
    elif args.append:
        from tools.xlsx.editor import append_row
        values = json.loads(args.append)
        result = append_row(args.file, args.sheet or "Sheet1", values, args.output)
    else:
        print("Error: Specify --cell/--value, --data, or --append", file=sys.stderr)
        sys.exit(1)
    print(f"Edited → {result}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tools", description="TENDERS document tools")
    sub = parser.add_subparsers(dest="command", required=True)

    # === PDF ===
    pdf = sub.add_parser("pdf", help="PDF operations")
    pdf_sub = pdf.add_subparsers(dest="subcmd", required=True)

    # pdf read
    pr = pdf_sub.add_parser("read", help="Extract text/tables/metadata from PDF")
    pr.add_argument("file", help="PDF file path")
    pr.add_argument("--pages", help="Page range: 1-3,5,8-10")
    pr.add_argument("--tables", action="store_true", help="Extract tables as JSON")
    pr.add_argument("--metadata", action="store_true", help="Show PDF metadata")
    pr.set_defaults(func=cmd_pdf_read)

    # pdf merge
    pm = pdf_sub.add_parser("merge", help="Merge PDFs")
    pm.add_argument("files", nargs="+", help="PDF files to merge")
    pm.add_argument("-o", "--output", required=True, help="Output file")
    pm.set_defaults(func=cmd_pdf_merge)

    # pdf split
    ps = pdf_sub.add_parser("split", help="Split/extract pages from PDF")
    ps.add_argument("file", help="Input PDF")
    ps.add_argument("--pages", help="Pages to extract: 1,3,5")
    ps.add_argument("--ranges", help="Page ranges: 1-3,8-10")
    ps.add_argument("-o", "--output", required=True, help="Output file")
    ps.set_defaults(func=cmd_pdf_split)

    # pdf forms
    pf_read = pdf_sub.add_parser("forms-read", help="Read PDF form fields")
    pf_read.add_argument("file", help="PDF file with forms")
    pf_read.set_defaults(func=cmd_pdf_forms_read)

    pf_fill = pdf_sub.add_parser("forms-fill", help="Fill PDF form fields")
    pf_fill.add_argument("file", help="PDF file with forms")
    pf_fill.add_argument("--data", required=True, help="JSON file with field values")
    pf_fill.add_argument("-o", "--output", required=True, help="Output file")
    pf_fill.add_argument("--flatten", action="store_true", help="Flatten form after filling")
    pf_fill.set_defaults(func=cmd_pdf_forms_fill)

    # pdf create
    pc = pdf_sub.add_parser("create", help="Create a PDF")
    pc.add_argument("--type", choices=["text", "proposal", "letter", "table"], default="text")
    pc.add_argument("--data", required=True, help="JSON data file or - for stdin (text type)")
    pc.add_argument("--title", help="Title (for text type)")
    pc.add_argument("-o", "--output", required=True, help="Output file")
    pc.set_defaults(func=cmd_pdf_create)

    # === DOCX ===
    docx = sub.add_parser("docx", help="DOCX operations")
    docx_sub = docx.add_subparsers(dest="subcmd", required=True)

    # docx read
    dr = docx_sub.add_parser("read", help="Extract text from DOCX")
    dr.add_argument("file", help="DOCX file path")
    dr.add_argument("--format", choices=["text", "json"], default="text")
    dr.add_argument("--tables", action="store_true", help="Extract tables only")
    dr.set_defaults(func=cmd_docx_read)

    # docx create
    dc = docx_sub.add_parser("create", help="Create a DOCX")
    dc.add_argument("--type", choices=["proposal", "letter"], default="proposal")
    dc.add_argument("--template", help="DOCX template file for placeholder replacement")
    dc.add_argument("--data", required=True, help="JSON data file")
    dc.add_argument("-o", "--output", required=True, help="Output file")
    dc.set_defaults(func=cmd_docx_create)

    # docx edit
    de = docx_sub.add_parser("edit", help="Find/replace in DOCX")
    de.add_argument("file", help="DOCX file")
    de.add_argument("--replace", required=True, help='JSON: {"old": "new"}')
    de.add_argument("-o", "--output", required=True, help="Output file")
    de.set_defaults(func=cmd_docx_edit)

    # docx to-pdf
    dp = docx_sub.add_parser("to-pdf", help="Convert DOCX to PDF")
    dp.add_argument("file", help="DOCX file")
    dp.add_argument("-o", "--output", required=True, help="Output PDF file")
    dp.set_defaults(func=cmd_docx_to_pdf)

    # === XLSX ===
    xlsx = sub.add_parser("xlsx", help="XLSX operations")
    xlsx_sub = xlsx.add_subparsers(dest="subcmd", required=True)

    # xlsx read
    xr = xlsx_sub.add_parser("read", help="Read XLSX data")
    xr.add_argument("file", help="XLSX file path")
    xr.add_argument("--sheet", help="Specific sheet name")
    xr.add_argument("--format", choices=["text", "json"], default="text")
    xr.set_defaults(func=cmd_xlsx_read)

    # xlsx create
    xc = xlsx_sub.add_parser("create", help="Create XLSX from JSON data")
    xc.add_argument("--data", required=True, help="JSON data file")
    xc.add_argument("-o", "--output", required=True, help="Output file")
    xc.set_defaults(func=cmd_xlsx_create)

    # xlsx edit
    xe = xlsx_sub.add_parser("edit", help="Edit XLSX cells")
    xe.add_argument("file", help="XLSX file")
    xe.add_argument("--sheet", help="Sheet name")
    xe.add_argument("--cell", help="Cell reference (e.g., A1)")
    xe.add_argument("--value", help="New value")
    xe.add_argument("--data", help="JSON file with {cell: value} updates")
    xe.add_argument("--append", help="JSON array of values to append as new row")
    xe.add_argument("-o", "--output", required=True, help="Output file")
    xe.set_defaults(func=cmd_xlsx_edit)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
