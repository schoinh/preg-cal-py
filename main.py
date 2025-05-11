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
                Img(src="screenshot-google.png", width="800px", style="border: 1px solid gray; border-radius: 10px; box-shadow: 10px 10px 18px -1px rgba(0,0,0,0.27); margin-bottom: 1em;"),
                id="screenshot-google",
            ),
            Hr(),
            H3("How to import the .ics file into your calendar app"),
            Div(
                H4("Tips"),
                Ul(
                    Li("The exact steps can vary and change due to updates to calendar applications. If the directions below seem outdated, a quick web search should help you out."),
                    Li("Importing the file into a new calendar instead of an existing one will allow you to show and hide just the pregnancy calendar, give it its own color, and easily delete all calendar events for the pregnancy weeks if needed."),
                    Li("If your due date changes, simply delete the calendar and generate a new one here."),
                ),
                style="border: 1px solid gray; border-radius: 10px; margin: 1em 0; padding: 1em;",
            ),
            P(B("Google Calendar")),
            Ol(
                Li("Go to Settings > Add Calendar to create a new calendar."),
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
            Hr(),
            Div(
                P(
                    "Need help? Have feedback? Send an email to ",
                    A("pregcal.help@gmail.com", href="mailto:pregcal.help@gmail.com"),
                    " or file an issue on ",
                    A("GitHub", href="https://github.com/schoinh/preg-cal-py"),
                    "!",
                ),
                P("Made with ❤️ in Seattle"),
                style="font-size: 0.8em; text-align: center;",
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
