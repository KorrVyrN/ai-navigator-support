"""Demo ticket repository tests."""
from pathlib import Path
from app.services.demo_repository import DemoTicketRepository

def test_demo_repository_loads_synthetic_tickets():
    path = Path(__file__).resolve().parents[1] / "data" / "synthetic_tickets.json"
    tickets = DemoTicketRepository(path).list_tickets()
    assert tickets
    assert all(ticket.id and ticket.description for ticket in tickets)
    assert all(ticket.timestamp is not None for ticket in tickets)
