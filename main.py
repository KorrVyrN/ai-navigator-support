"""Offline synthetic-data demonstration. Use uvicorn app.main:app for the API."""
import json
from pathlib import Path

from app.services.anonymizer import PIIAnonymizer


def run_pipeline():
    tickets = json.loads((Path(__file__).parent / 'data/synthetic_tickets.json').read_text(encoding='utf-8'))
    anonymizer = PIIAnonymizer()
    for ticket in tickets:
        print(f"ID: {ticket['id']} | {anonymizer.anonymize(ticket['description'])}")


if __name__ == '__main__':
    run_pipeline()
