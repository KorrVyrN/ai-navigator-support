import re


class PIIAnonymizer:
    """
    Detects and masks common types of potentially sensitive information.
    This is a basic protection layer and should not be treated as
    a complete legal compliance solution.
    """

    def __init__(self):
        self.patterns = {
            "phone": re.compile(
                r"(?<!\d)(?:\+7|8)[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}(?!\d)"
            ),
            "email": re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            ),
            "inn": re.compile(
                r"(?<!\d)\d{10}(?:\d{2})?(?!\d)"
            ),
            "snils": re.compile(
                r"(?<!\d)\d{3}[-\s]?\d{3}[-\s]?\d{3}\s?\d{2}(?!\d)"
            ),
            "ip": re.compile(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ),
            "card": re.compile(
                r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)"
            ),
        }

    def anonymize(self, text: str) -> str:
        """
        Replace detected sensitive information with placeholders.
        """

        if not text:
            return text

        result = text

        result = self.patterns["phone"].sub("[PHONE]", result)
        result = self.patterns["email"].sub("[EMAIL]", result)
        result = self.patterns["inn"].sub("[INN]", result)
        result = self.patterns["snils"].sub("[SNILS]", result)
        result = self.patterns["ip"].sub("[IP]", result)
        result = self.patterns["card"].sub("[CARD]", result)

        return result
