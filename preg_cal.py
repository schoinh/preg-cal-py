import datetime
from dataclasses import dataclass
from typing import Iterator, Literal
import random
import zoneinfo

EventType = Literal["week", "day"]

@dataclass
class Event:
    week_num: int
    start_date: datetime.date
    end_date: datetime.date
    name: str | None = None
    created_at: datetime.datetime | None = None
    
    def __post_init__(self):
        """Initialize creation time if not provided."""
        if self.created_at is None:
            # Use UTC for all timestamps
            self.created_at = datetime.datetime.now(zoneinfo.ZoneInfo('UTC'))

    def get_name(self) -> str:
        """Get the event name, defaulting to week number if not specified."""
        return self.name or f"{self.week_num}W"

    def format_date(self, date: datetime.date) -> str:
        """Format a date object to calendar string format."""
        return date.strftime("%Y%m%d")
    
    def format_datetime(self, dt: datetime.datetime) -> str:
        """Format a datetime object to iCal format in UTC."""
        return dt.strftime("%Y%m%dT%H%M%SZ")

    def create_uid(self) -> str:
        """Create a unique identifier for the event."""
        hex_id = "".join(random.choices("0123456789abcdef", k=6))
        timestamp = self.format_datetime(self.created_at)
        return f"PREG-CAL-{self.get_name()}-{timestamp}-{hex_id}"

    def to_ical(self) -> str:
        """Convert the event to iCal format."""
        created_str = self.format_datetime(self.created_at)
        
        return (
            "BEGIN:VEVENT\n"
            f"CREATED:{created_str}\n"
            f"DTEND;VALUE=DATE:{self.format_date(self.end_date)}\n"
            f"DTSTAMP:{created_str}\n"
            f"DTSTART;VALUE=DATE:{self.format_date(self.start_date)}\n"
            f"LAST-MODIFIED:{created_str}\n"
            "SEQUENCE:1\n"
            f"SUMMARY:{self.get_name()}\n"
            "TRANSP:TRANSPARENT\n"
            f"UID:{self.create_uid()}\n"
            "BEGIN:VALARM\n"
            "ACTION:NONE\n"
            "TRIGGER;VALUE=DATE-TIME:19760401T005545Z\n"
            "END:VALARM\n"
            "END:VEVENT\n"
        )


def get_pregnancy_start_date(due_date: datetime.date) -> datetime.date:
    """Calculate the start date of pregnancy tracking (36 weeks before due date)."""
    return due_date - datetime.timedelta(days=(7 * 36))


def generate_events(due_date: datetime.date, event_type: EventType) -> Iterator[Event]:
    """Generate pregnancy calendar events based on the specified type."""
    week_num = 4
    current_date = get_pregnancy_start_date(due_date)
    
    # Use the same creation time for all events in a batch
    created_at = datetime.datetime.now(zoneinfo.ZoneInfo('UTC'))
    
    while week_num <= 42:
        if event_type == "week":
            # Generate one event per week
            week_end = current_date + datetime.timedelta(days=7)
            yield Event(week_num, current_date, week_end, created_at=created_at)
            current_date = week_end
            week_num += 1
        else:  # day events
            # Generate an event for each day in the week
            for _ in range(7):
                next_day = current_date + datetime.timedelta(days=1)
                name = f"{week_num}W {next_day.strftime('%b %d')}"
                yield Event(week_num, current_date, next_day, name=name, created_at=created_at)
                current_date = next_day
            week_num += 1


def create_ical(due_date: datetime.date, event_type: EventType = "week") -> str:
    """Create an iCal file with pregnancy events."""
    created_at = datetime.datetime.now(zoneinfo.ZoneInfo('UTC'))
    
    CALENDAR_HEADER = (
        "BEGIN:VCALENDAR\n"
        "CALSCALE:GREGORIAN\n"
        "PRODID:-//Apple Inc.//macOS 13.2.1//EN\n"
        "VERSION:2.0\n"
        "X-APPLE-CALENDAR-COLOR:#CC73E1\n"
        "X-WR-CALNAME:Preg Cal\n"
    )
    CALENDAR_FOOTER = "END:VCALENDAR"

    # Create the due date event
    due_date_event = Event(
        week_num=42,
        start_date=due_date,
        end_date=due_date + datetime.timedelta(days=1),
        name="Due Date",
        created_at=created_at
    )

    # Generate all events including the due date
    events = list(generate_events(due_date, event_type))
    events.append(due_date_event)
    
    # Write to file
    filename = "preg-cal.ics"
    with open(filename, "w") as file:
        file.write(CALENDAR_HEADER)
        for event in events:
            file.write(event.to_ical())
        file.write(CALENDAR_FOOTER)

    return filename
