from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class CausalEvent(BaseModel):
    id: str
    scheme_id: Optional[str] = None
    event_date: datetime
    description: str
    event_type: str = Field(..., pattern="^(portal_update|policy_change|rule_change|budget_release|other)$")
    source_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# In-Memory Registry for now (Phase 2A) - Replace with DB later
class CausalEventStore:
    _events: List[CausalEvent] = []

    @classmethod
    def add_event(cls, event: CausalEvent):
        cls._events.append(event)
        # Keep sorted by date
        cls._events.sort(key=lambda x: x.event_date)

    @classmethod
    def get_events(cls, scheme_id: str = None, start_date: datetime = None, end_date: datetime = None) -> List[CausalEvent]:
        results = cls._events
        
        if scheme_id:
            results = [e for e in results if e.scheme_id == scheme_id]
            
        if start_date:
            results = [e for e in results if e.event_date >= start_date]

        if end_date:
            results = [e for e in results if e.event_date <= end_date]
            
        return results

    @classmethod
    def get_latest_event(cls, scheme_id: str) -> Optional[CausalEvent]:
        # Since list is sorted, take last matching
        matches = [e for e in cls._events if e.scheme_id == scheme_id]
        return matches[-1] if matches else None
