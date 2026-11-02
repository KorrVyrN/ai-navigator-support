"""Offline incident detection behavior and API contract."""
from datetime import datetime, timedelta, timezone
from app.services.incident_detection import TicketInput, group_incidents

def test_group_three_nearby_tickets():
    base = datetime(2026, 11, 2, tzinfo=timezone.utc)
    tickets = [TicketInput(id=str(i), timestamp=base + timedelta(minutes=i * 10),
                           description="POS offline", region="Lipetsk", equipment="POS") for i in range(3)]
    result = group_incidents(tickets)
    assert len(result) == 1
    assert result[0].count == 3
    assert result[0].ticket_ids == ["0", "1", "2"]

def test_no_group_when_regions_differ():
    base = datetime(2026, 11, 2, tzinfo=timezone.utc)
    tickets = [TicketInput(id=str(i), timestamp=base, description="offline",
                           region=str(i), equipment="POS") for i in range(3)]
    assert group_incidents(tickets) == []

def test_no_group_when_outside_window():
    base = datetime(2026, 11, 2, tzinfo=timezone.utc)
    tickets = [TicketInput(id=str(i), timestamp=base + timedelta(hours=i),
                           description="offline", region="Lipetsk", equipment="POS") for i in range(3)]
    assert group_incidents(tickets, window_minutes=30) == []
