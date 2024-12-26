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
