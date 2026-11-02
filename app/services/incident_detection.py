"""Deterministic, offline incident grouping for synthetic support tickets."""
from collections import defaultdict
from datetime import datetime, timezone
from pydantic import BaseModel, Field

class TicketInput(BaseModel):
    id: str
    timestamp: datetime
    description: str = Field(min_length=1, max_length=20000)
    region: str = "unknown"
    equipment: str = "unknown"

class IncidentGroup(BaseModel):
    region: str
    equipment: str
    ticket_ids: list[str]
    count: int
    first_seen: datetime
    last_seen: datetime

def group_incidents(tickets: list[TicketInput], threshold: int = 3, window_minutes: int = 60) -> list[IncidentGroup]:
    """Group nearby tickets by region and equipment within a rolling time window."""
    buckets = defaultdict(list)
    seen_ids = set()
    for ticket in tickets:
        if ticket.id in seen_ids:
            continue
        seen_ids.add(ticket.id)
        stamp = ticket.timestamp
        if stamp.tzinfo is None:
            stamp = stamp.replace(tzinfo=timezone.utc)
        buckets[(ticket.region.casefold().strip(), ticket.equipment.casefold().strip())].append((stamp, ticket))
    groups = []
    for (region, equipment), entries in buckets.items():
        entries.sort(key=lambda pair: pair[0])
        cluster = []
        for stamp, ticket in entries:
            if cluster and (stamp - cluster[0][0]).total_seconds() > window_minutes * 60:
                if len(cluster) >= threshold:
                    groups.append(IncidentGroup(region=region, equipment=equipment, ticket_ids=[t.id for _, t in cluster], count=len(cluster), first_seen=cluster[0][0], last_seen=cluster[-1][0]))
                cluster = []
            cluster.append((stamp, ticket))
        if len(cluster) >= threshold:
            groups.append(IncidentGroup(region=region, equipment=equipment, ticket_ids=[t.id for _, t in cluster], count=len(cluster), first_seen=cluster[0][0], last_seen=cluster[-1][0]))
    return sorted(groups, key=lambda g: (-g.count, g.region, g.equipment))
