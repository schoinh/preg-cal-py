import datetime
import click

from preg_cal import create_ical


@click.command()
@click.option("--year", prompt="In what year are you due? Ex) 2025")
@click.option("--month", prompt="In which month? Ex) 8")
@click.option("--date", prompt="On which date? Ex) 27")
def preg_call(year, month, date):
    click.confirm(f"Sounds like your due date is {month}/{date}/{year}?")
    due_date = datetime.date(int(year), int(month), int(date))
    create_ical(due_date)


if __name__ == "__main__":
    preg_call()
