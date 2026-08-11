import re

class PIIAnonymizer:
    """Модуль маскирования персональных данных по ФЗ-152"""
    
    def __init__(self):
        self.phone_pattern = re.compile(r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}')
        self.inn_pattern = re.compile(r'\b\d{10}\b|\b\d{12}\b')
        self.address_pattern = re.compile(r'(г\.|ул\.|пр-кт|пер\.|д\.)\s?[А-Яа-я0-9\.\s\-]+(?=,|$|\sне\s|working)')

    def mask_text(self, text: str) -> str:
        """Замена чувствительных данных на безопасные плейсхолдеры"""
        masked = self.phone_pattern.sub('[MASKED_PHONE]', text)
        masked = self.inn_pattern.sub('[MASKED_INN]', masked)
        masked = self.address_pattern.sub('[MASKED_ADDRESS]', masked)
        return masked

if __name__ == "__main__":
    anonymizer = PIIAnonymizer()
    sample_text = "Заявка от ООО Ромашка (ИНН 7701234567), г. Москва, ул. Ленина д. 10. Тел: +7 (999) 111-22-33. Не работает POS."
    print("Исходный текст:", sample_text)
    print("Защищенный текст:", anonymizer.mask_text(sample_text))
