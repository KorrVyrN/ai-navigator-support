"""Repository for local demo tickets; corporate integrations require separate approval."""
import json
from pathlib import Path
from app.services.incident_detection import TicketInput

class DemoTicketRepository:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def list_tickets(self) -> list[TicketInput]:
        records = json.loads(self.file_path.read_text(encoding="utf-8"))
        return [
            TicketInput(
                id=str(item["id"]),
                timestamp=item["timestamp"],
                description=item["description"],
                region=item.get("region") or item.get("location") or "unknown",
                equipment=item.get("equipment") or item.get("type") or "unknown",
            )
            for item in records
        ]
