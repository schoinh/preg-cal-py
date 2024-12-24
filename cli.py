import datetime
import click

from preg_cal import format_date, get_week_bounds, get_week_events, create_event


@click.command()
@click.option("--year", prompt="In what year are you due? Ex) 2025")
@click.option("--month", prompt="In which month? Ex) 8")
@click.option("--date", prompt="On which date? Ex) 27")
def preg_call(year, month, date):
    click.confirm(f"Sounds like your due date is {month}/{date}/{year}?")
    due_date = datetime.date(int(year), int(month), int(date))
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

    with open("preg-cal.ics", "w") as file:
        file.write(header + week_events + due_date_event + footer)


if __name__ == "__main__":
    preg_call()
