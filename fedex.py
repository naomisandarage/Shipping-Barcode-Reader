import re


class FedExParser:
    def __init__(self, raw_data: str):
        self.raw_data = raw_data

    def _clean_text(self, text: str) -> str:
        """Helper to replace visual control character symbols with standard spaces/chars."""
        if not text:
            return ""
        return text.replace('␠', ' ').strip()

    def parse(self) -> dict:
        normalized = (self.raw_data.replace('␝', '\x1d').replace(
            '␞', '\x1e').replace('␜', '\x1c'))

        parsed_data = {"carrier": "FedEx", "recipient": {"name": None, "street": None, "city": None, "province_state": None, "postal_code": None, "phone": None},
                       "package": {"weight": None, "tracking_number": None, "description": None}}

        blocks = normalized.split('\x1e')

        for block in blocks:
            cleaned_block = block.lstrip('[)>')

            if cleaned_block.startswith('01'):
                fields = cleaned_block.split('\x1d')

                if len(fields) > 1:
                    raw_postal = fields[1]
                    parsed_data["recipient"]["postal_code"] = self._clean_text(
                        raw_postal[2:] if raw_postal.startswith('02') else raw_postal)

                if len(fields) > 6:
                    parsed_data["package"]["tracking_number"] = self._clean_text(
                        fields[6])

                if len(fields) > 10:
                    parsed_data["package"]["weight"] = self._clean_text(
                        fields[10])

                if len(fields) > 12:
                    parsed_data["recipient"]["street"] = self._clean_text(
                        fields[12])

                if len(fields) > 13:
                    parsed_data["recipient"]["city"] = self._clean_text(
                        fields[13])

                if len(fields) > 14:
                    parsed_data["recipient"]["province_state"] = self._clean_text(
                        fields[14])

                if len(fields) > 15:
                    raw_name = fields[15].split('\x1e')[0]
                    parsed_data["recipient"]["name"] = self._clean_text(
                        raw_name)

            elif cleaned_block.startswith('06'):
                fields = cleaned_block.split('\x1d')
                for field in fields:
                    if field.startswith('12Z'):
                        parsed_data["recipient"]["phone"] = self._clean_text(
                            field[3:])
                    elif field.startswith('99Z'):
                        sub_fields = field.split('\x1c')
                        if len(sub_fields) > 4:
                            parsed_data["package"]["description"] = self._clean_text(
                                sub_fields[4])
        return parsed_data
