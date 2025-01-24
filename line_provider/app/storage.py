from pydantic import UUID4

from line_provider.app.core.models import Event

events: dict[UUID4, Event] = {}
