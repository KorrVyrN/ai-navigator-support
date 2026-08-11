from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Ticket(BaseModel):
    id: Optional[str] = None
    created_at: datetime
    source: str
    description: str
    category: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    location: Optional[str] = None
    equipment: Optional[str] = None
