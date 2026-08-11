import json
import os
from anonymizer import PIIAnonymizer

def run_pipeline():
    print("=== [AI-Штурман] Запуск пайплайна обработки заявок ===")
    anonymizer = PIIAnonymizer()
    
    data_path = os.path.join("data", "synthetic_tickets.json")
    if not os.path.exists(data_path):
        print(f"Ошибка: файл {data_path} не найден.")
        return
    
    with open(data_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)
    
    print(f"Загружено заявок для анализа: {len(tickets)}")
    print("-" * 60)
    
    for ticket in tickets:
        raw_desc = ticket.get("description", "")
        clean_desc = anonymizer.mask_text(raw_desc)
        print(f"[ID: {ticket['id']}] ФЗ-152 Маскирование -> {clean_desc}")

    print("-" * 60)
    print("Имитация векторного анализа через EmbeddingsGigaR и GigaChat-2-Max...")
    print("🔥 [АНОМАЛИЯ ОБНАРУЖЕНА]: Кластер сбоев провайдера связи в районе ул. Тверская.")
    print("✅ [Human-in-the-Loop]: Карточка массового инцидента сформирована за 15 минут и передана в ДЦ.")

if __name__ == "__main__":
    run_pipeline()
