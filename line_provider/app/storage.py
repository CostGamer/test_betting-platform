from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from pydantic import UUID4

from line_provider.app.core.models import Event, EventStatus

# Storage example
events: dict[UUID4, Event] = {
    UUID("547e95a4-0afc-46d2-8c32-c757cc6bb5d9", version=4): Event(
        name="Real Madrid - Barcelona",
        coefficient=Decimal("1.51"),
        deadline=int(datetime.now(timezone.utc).timestamp()) + 100,
        event_id=UUID("547e95a4-0afc-46d2-8c32-c757cc6bb5d9", version=4),
        status=EventStatus.NEW,
    ),
    UUID("6960f10c-361b-46fe-a5bb-7540c0b0a8ba", version=4): Event(
        name="Liverpool - Chelsea",
        coefficient=Decimal("2.15"),
        deadline=int(datetime.now(timezone.utc).timestamp()) + 200,
        event_id=UUID("6960f10c-361b-46fe-a5bb-7540c0b0a8ba", version=4),
        status=EventStatus.NEW,
    ),
    UUID("c9c94acc-4288-4352-a1a1-c5b33c854f30", version=4): Event(
        name="Paris Saint-Germain - Bayern Munich",
        coefficient=Decimal("1.87"),
        deadline=int(datetime.now(timezone.utc).timestamp()) + 300,
        event_id=UUID("c9c94acc-4288-4352-a1a1-c5b33c854f30", version=4),
        status=EventStatus.NEW,
    ),
}
