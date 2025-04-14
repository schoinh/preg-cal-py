import datetime
import click

from preg_cal import create_ical


@click.command()
@click.option("--year", prompt="In what year are you due? Ex) 2025")
@click.option("--month", prompt="In which month? Ex) 8")
@click.option("--date", prompt="On which date? Ex) 27")
@click.option("--use-days", is_flag=True, help="Generate daily events instead of weekly events")
def preg_call(year, month, date, use_days):
    click.confirm(f"Sounds like your due date is {month}/{date}/{year}?")
    due_date = datetime.date(int(year), int(month), int(date))
    create_ical(due_date, use_days)


if __name__ == "__main__":
    preg_call()
