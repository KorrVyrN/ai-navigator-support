"""SQLite persistence unit tests."""
from datetime import datetime, timezone
from app.services.incident_detection import TicketInput
from app.services.ticket_store import TicketStore

def test_store_persists_and_updates(tmp_path):
    path = tmp_path / "tickets.sqlite"
    store = TicketStore(path)
    ticket = TicketInput(id="123", timestamp=datetime(2026, 11, 2, tzinfo=timezone.utc),
                         description="POS offline", region="Lipetsk", equipment="POS")
    store.save(ticket)
    assert TicketStore(path).list_tickets()[0].description == "POS offline"
    updated = ticket.model_copy(update={"description": "POS restored"})
    store.save(updated)
    rows = TicketStore(path).list_tickets()
    assert len(rows) == 1
    assert rows[0].description == "POS restored"
