from fasthtml.common import *
from starlette.responses import FileResponse
import datetime

from preg_cal import format_date, get_week_bounds, get_week_events, create_event

app, rt = fast_app()


@rt("/")
def get():
    return Titled(
        "Pregnancy Calendar Generator",
        Form(
            Group(
                Input(
                    type="number",
                    id="year",
                    name="year",
                    min="2024",
                    max="2030",
                    placeholder="Year (e.g. 2025)",
                ),
                Input(
                    type="number",
                    id="month",
                    name="month",
                    min="1",
                    max="12",
                    placeholder="Month (1-12)",
                ),
                Input(
                    type="number",
                    id="date",
                    name="date",
                    min="1",
                    max="31",
                    placeholder="Date (1-31)",
                ),
                Button("Generate Calendar", type="submit"),
            ),
            method="post",
            action="/generate",
        ),
        P("Enter your due date to generate a calendar with pregnancy week markers."),
    )


@dataclass
class DueDate:
    year: int
    month: int
    date: int


@rt("/generate")
def post(due: DueDate):
    due_date = datetime.date(due.year, due.month, due.date)

    due_date_event = create_event(
        "Due Date",
        format_date(due_date),
        format_date(due_date + datetime.timedelta(days=1)),
    )

    header = (
        "BEGIN:VCALENDAR\n"
        "CALSCALE:GREGORIAN\n"
        "PRODID:-//Apple Inc.//macOS 13.2.1//EN\n"
        "VERSION:2.0\n"
        "X-APPLE-CALENDAR-COLOR:#CC73E1\n"
        "X-WR-CALNAME:Preg Cal\n"
    )
    footer = "END:VCALENDAR"

    week_bounds = get_week_bounds(due_date)
    week_events = get_week_events(week_bounds)

    filename = "preg-cal.ics"
    with open(filename, "w") as file:
        file.write(header + week_events + due_date_event + footer)

    return FileResponse(
        filename,
        media_type="text/calendar",
        filename=filename,
    )


serve()
