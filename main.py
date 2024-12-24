from fasthtml.common import *
from starlette.responses import FileResponse
import datetime

# Import your existing logic
from preg_cal import format_date, get_week_bounds, get_week_events, create_event

app, rt = fast_app()


@rt("/")
def get():
    return Titled(
        "Pregnancy Calendar Generator",
        Container(
            P(
                "Select your due date to generate a calendar with pregnancy week markers."
            ),
            Div(
                Form(
                    Group(
                        Input(
                            type="date",
                            id="due_date",
                            name="due_date",
                            min="2024-01-01",
                            max="2030-12-31",
                            required=True,
                            cls="form-control",
                        ),
                        Button(
                            "Generate",
                            type="submit",
                            cls="primary",
                        ),
                    ),
                    method="post",
                    action="/generate",
                ),
                cls="grid",
                style="max-width: 480px;",
            ),
        ),
    )


@dataclass
class DueDate:
    due_date: str  # Will receive date in YYYY-MM-DD format


@rt("/generate")
def post(due: DueDate):
    year, month, day = map(int, due.due_date.split("-"))

    due_date = datetime.date(year, month, day)

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
