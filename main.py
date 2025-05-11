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
            P(
                "Enter your estimated due date to generate a calendar (.ics) file containing week-long events from 4 to 42 weeks:"
            ),
            Div(
                Form(
                    Group(
                        Input(
                            type="date",
                            id="due_date",
                            name="due_date",
                            required=True,
                            cls="form-control",
                        ),
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
                style="margin-bottom: 20px; max-width: 480px;",
            ),
            P(
                "Import the file as a new calendar into your Google Calendar, Apple Calendar, or Outlook, where you can:"
            ),
            Ul(
                Li("View the week numbers alongside all your other life events"),
                Li("Show/hide the calendar as needed"),
                Li("Change the name, color, and events as you would with any other calendar layer"),
            ),
            Div(
                Img(src="screenshot-google.png", width="800px", style="border: 2px solid black; margin-bottom: 1em;"),
                id="screenshot-google",
            ),
            P(
                "It's your file once you've downloaded it. If your due date changes, you can just delete the calendar and generate a new one here."
            ),
            Hr(),
            H3("How to import the .ics file into your calendar app"),
            P("Note: The exact steps can vary and change due to updates to calendar applications. If the directions below seem outdated, a quick web search should help you out."),
            P(B("Google Calendar")),
            Ol(
                Li("Go to Settings > Add Calendar to create a new calendar. (Importing the file into a new calendar will make it easy for you to delete the calendar if you need to change the due date or just want to remove all the calendar events.)"),
                Li("In Settings > Import & Export > Import, upload the .ics file, select the new calendar you created, and click Import."),
            ),
            P(B("Apple Calendar")),
            Ol(
                Li("Simply drag and drop the file onto your Calendar app."),
                Li("When asked for a destination calendar, choose \"New Calendar...\" and give your new calendar a name."),
            ),
            P(B("Outlook Calendar")),
            Ul(
                Li("The steps may vary based on your operating system (Mac vs. PC) and the platform you're using (web vs. desktop app). A web search is recommended for the most up-to-date information."),
            ),
        ),
    )


@dataclass
class DueDate:
    due_date: str  # YYYY-MM-DD format


@rt("/generate")
def post(due: DueDate):
    year, month, day = map(int, due.due_date.split("-"))

    due_date = datetime.date(year, month, day)
    filename = create_ical(due_date)

    return FileResponse(
        filename,
        media_type="text/calendar",
        filename=filename,
    )


serve()
