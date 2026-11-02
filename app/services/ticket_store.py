"""Persistent SQLite ticket storage for standalone development.

This module is not enabled by default; enterprise storage requires a separate review.
"""
import sqlite3
from pathlib import Path

class TicketStore:
    def __init__(self, database_path: Path):
        self.database_path = database_path
        self.initialize()

    def connect(self):
        return sqlite3.connect(str(self.database_path))

    def initialize(self):
        with self.connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS tickets "
                "(id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, "
                "description TEXT NOT NULL, region TEXT NOT NULL, equipment TEXT NOT NULL)"
            )

    def save(self, ticket):
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO tickets(id,timestamp,description,region,equipment) VALUES(?,?,?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET timestamp=excluded.timestamp, "
                "description=excluded.description, region=excluded.region, equipment=excluded.equipment",
                (ticket.id, ticket.timestamp.isoformat(), ticket.description, ticket.region, ticket.equipment),
            )

    def list_tickets(self):
        from app.services.incident_detection import TicketInput
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT id,timestamp,description,region,equipment FROM tickets ORDER BY timestamp DESC"
            ).fetchall()
        return [TicketInput(id=row[0], timestamp=row[1], description=row[2],
                            region=row[3], equipment=row[4]) for row in rows]
