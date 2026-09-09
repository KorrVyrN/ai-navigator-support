import pytest
from app.services.anonymizer import PIIAnonymizer


class TestPIIAnonymizer:
    """Tests for PIIAnonymizer class"""

    @pytest.fixture
    def anonymizer(self):
        """Create anonymizer instance for each test"""
        return PIIAnonymizer()

    def test_mask_phone_russian_format(self, anonymizer):
        """Test masking Russian phone numbers with +7 prefix"""
        text = "Call me at +7 (495) 123-45-67"
        result = anonymizer.anonymize(text)
        assert "[PHONE]" in result
        assert "495" not in result

    def test_mask_phone_8_prefix(self, anonymizer):
        """Test masking Russian phone numbers with 8 prefix"""
        text = "My phone: 8 (999) 888-77-66"
        result = anonymizer.anonymize(text)
        assert "[PHONE]" in result
        assert "999" not in result

    def test_mask_email(self, anonymizer):
        """Test masking email addresses"""
        text = "Contact us at support@example.com or info@company.ru"
        result = anonymizer.anonymize(text)
        assert result.count("[EMAIL]") == 2
        assert "support@example.com" not in result
        assert "info@company.ru" not in result

    def test_mask_inn_10_digits(self, anonymizer):
        """Test masking INN with 10 digits"""
        text = "Company INN: 7724569874"
        result = anonymizer.anonymize(text)
        assert "[INN]" in result
        assert "7724569874" not in result

    def test_mask_inn_12_digits(self, anonymizer):
        """Test masking INN with 12 digits"""
        text = "INN: 770011223344"
        result = anonymizer.anonymize(text)
        assert "[INN]" in result
        assert "770011223344" not in result

    def test_mask_snils(self, anonymizer):
        """Test masking SNILS (pension number)"""
        text = "SNILS: 123-456-789 01"
        result = anonymizer.anonymize(text)
        assert "[SNILS]" in result
        assert "123-456-789" not in result

    def test_mask_ip_address(self, anonymizer):
        """Test masking IP addresses"""
        text = "Server IP: 192.168.1.100 and backup 10.0.0.1"
        result = anonymizer.anonymize(text)
        assert result.count("[IP]") == 2
        assert "192.168.1.100" not in result
        assert "10.0.0.1" not in result

    def test_mask_card_number(self, anonymizer):
        """Test masking card numbers"""
        text = "Card: 4532-1111-2222-3333"
        result = anonymizer.anonymize(text)
        assert "[CARD]" in result
        assert "4532" not in result

    def test_multiple_sensitive_data(self, anonymizer):
        """Test masking multiple types of sensitive data in one text"""
        text = (
            "Client: ООО Company, INN 7724569874. "
            "Contact: +7 (495) 123-45-67 or admin@company.ru. "
            "Location: г. Москва, ул. Садовая д. 15. "
            "Server IP: 192.168.1.100"
        )
        result = anonymizer.anonymize(text)
        assert "[PHONE]" in result
        assert "[EMAIL]" in result
        assert "[INN]" in result
        assert "[IP]" in result
        assert "7724569874" not in result
        assert "admin@company.ru" not in result

    def test_empty_string(self, anonymizer):
        """Test handling of empty string"""
        result = anonymizer.anonymize("")
        assert result == ""

    def test_none_input(self, anonymizer):
        """Test handling of None input"""
        result = anonymizer.anonymize(None)
        assert result is None

    def test_text_without_sensitive_data(self, anonymizer):
        """Test text without sensitive data remains unchanged"""
        text = "This is a normal text without any sensitive information"
        result = anonymizer.anonymize(text)
        assert result == text

    def test_multiple_phones_in_text(self, anonymizer):
        """Test masking multiple phone numbers"""
        text = "Call +7 (495) 111-11-11 or +7 (812) 222-22-22"
        result = anonymizer.anonymize(text)
        assert result.count("[PHONE]") == 2
        assert "495" not in result
        assert "812" not in result
