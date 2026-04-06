"""PDF form field reading and filling."""

import json
from pypdf import PdfReader, PdfWriter


def read_fields(path: str) -> list[dict]:
    """Read all form fields from a PDF, returning field names, types, and values."""
    reader = PdfReader(path)
    fields = []
    if reader.get_fields():
        for name, field in reader.get_fields().items():
            fields.append({
                "name": name,
                "type": field.get("/FT", "unknown"),
                "value": field.get("/V", ""),
                "default": field.get("/DV", ""),
                "options": field.get("/Opt", []),
            })
    return fields


def fill_form(path: str, data: dict, output_path: str, flatten: bool = False) -> str:
    """Fill form fields in a PDF.

    Args:
        path: Input PDF with form fields
        data: Dict mapping field names to values
        output_path: Where to save the filled PDF
        flatten: If True, flatten the form (makes fields non-editable)
    """
    reader = PdfReader(path)
    writer = PdfWriter()
    writer.append(reader)

    for page_num in range(len(writer.pages)):
        writer.update_page_form_field_values(writer.pages[page_num], data)

    if flatten:
        for page in writer.pages:
            for annot in page.get("/Annots", []):
                annot_obj = annot.get_object()
                if annot_obj.get("/Subtype") == "/Widget":
                    annot_obj.update({"/Ff": 1})

    with open(output_path, "wb") as f:
        writer.write(f)
    return output_path
