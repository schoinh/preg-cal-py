from fasthtml.common import *
from starlette.responses import FileResponse
import datetime

from preg_cal import create_ical

app, rt = fast_app()


@rt("/")
def get():
    return Titled(
        "Pregnancy Calendar Generator",
        Container(
            Style("""
                .tooltip-wrapper {
                    position: relative;
                    display: inline-block;
                }
                .tooltip-wrapper::after {
                    content: attr(data-tooltip);
                    position: absolute;
                    bottom: 100%;
                    left: 50%;
                    transform: translateX(-50%);
                    padding: 4px 8px;
                    background: #333;
                    color: white;
                    border-radius: 4px;
                    font-size: 14px;
                    white-space: nowrap;
                    visibility: hidden;
                    opacity: 0;
                    transition: opacity 0.1s;
                }
                .tooltip-wrapper:hover::after {
                    visibility: visible;
                    opacity: 1;
                }
            """),
            P(
                "Enter your estimated due date to generate a calendar (.ics) file containing events from 4 to 42 weeks."
            ),
            P(
                "Import it as a new calendar into your Google Calendar, Apple Calendar, or Outlook, where you can:"
            ),
            Ul(
                Li("View the week numbers alongside all your other life events"),
                Li("Show/hide the calendar as needed"),
                Li("Change the name, color, and events as you would with any other calendar layer"),
            ),
            P(
                "It's your file once you've downloaded it. If your due date changes, you can just delete the calendar and generate a new one here."
            ),
            Hr(),
            Div(
                Form(
                    Label("Estimated Due Date:"),
                    Group(
                        Input(
                            type="date",
                            id="due_date",
                            name="due_date",
                            required=True,
                            cls="form-control",
                        ),
                    ),
                    Div(
                        Button("Week Events", 
                               type="button", 
                               name="event_type", 
                               value="week", 
                               id="week_events", 
                               cls="toggle-button active",
                               title="Shows only the weeks on the calendar."),
                        Button("Day Events", 
                               type="button", 
                               name="event_type", 
                               value="day", 
                               id="day_events", 
                               cls="toggle-button",
                               title="Shows a new event per day of pregnancy on the calendar."),
                        Input(type="hidden", name="event_type", value="week"),
                        cls="toggle-group"
                    ),
                    Group(
                        Button(
                            "Download",
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
            Hr(),
            H3("How to import the .ics file into your calendar app"),
            P("Note: The exact steps can vary and change due to updates to calendar applications. If the directions below seem outdated, a quick web search should help you out."),
            P("Apple Calendar"),
            Ol(
                Li("Simply drag and drop the file onto your Calendar app."),
                Li("When asked for a destination calendar, choose \"New Calendar...\" and give your new calendar a name."),
            ),
            Div(
                Img(src="screenshot.png", width="500px", style="border: 2px solid black; margin-bottom: 2em;"),
                id="screenshot",
            ),
            P("Google Calendar"),
            Ol(
                Li("Go to Settings > Add Calendar to create a new calendar."),
                Li("In Settings > Import & Export > Import, upload the .ics file, select the new calendar you created, and click Import."),
            ),
            P("Outlook Calendar"),
            Ul(
                Li("The steps may vary based on your operating system (Mac vs. PC) and the platform you're using (web vs. desktop app). A web search is recommended for the most up-to-date information."),
            ),
        ),
        Head(
            Link(rel="stylesheet", href="/static/style.css"),
            Script(src="/static/script.js"),
            Title("Pregnancy Calendar Generator"),
        ),
    )


@dataclass
class DueDate:
    due_date: str  # YYYY-MM-DD format
    event_type: str  # 'week' or 'day'


@rt("/generate")
def post(due: DueDate):
    year, month, day = map(int, due.due_date.split("-"))

    due_date = datetime.date(year, month, day)
    filename = create_ical(due_date, event_type=(due.event_type))

    return FileResponse(
        filename,
        media_type="text/calendar",
        filename=filename,
    )


serve()
