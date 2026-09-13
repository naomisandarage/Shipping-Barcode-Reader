from .fedex import FedExParser


def parse_barcode(raw_text: str) -> dict:
    """Central router to detect carrier and pick the correct parser."""
    if '[)>' in raw_text or 'FDE' in raw_text or 'FDX' in raw_text:
        parser = FedExParser(raw_text)
        return parser.parse()
    else:
        return {"error": "Unsupported barcode format"}
