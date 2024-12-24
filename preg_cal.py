import datetime
import random


def format_date(date_object: datetime.date) -> str:
    return date_object.strftime("%Y%m%d")


def get_week_bounds(due_date: datetime.date):
    week_bounds = []
    week_num = 4
    week_start = due_date - datetime.timedelta(days=(7 * 36))
    week_end = week_start + datetime.timedelta(days=7)

    while week_num <= 42:
        week = (week_num, format_date(week_start), format_date(week_end))
        week_bounds.append(week)

        week_num += 1
        week_start += datetime.timedelta(days=7)
        week_end += datetime.timedelta(days=7)

    return week_bounds


def get_week_events(week_bounds):
    week_events = ""

    for week_num, week_start, week_end in week_bounds:
        week_events += create_event(f"{week_num}W", week_start, week_end)

    return week_events


def create_event(name, start, end):
    hex = "".join([random.choice("0123456789abcdef") for i in range(6)])
    return (
        "BEGIN:VEVENT\n"
        "CREATED:20241222T231056Z\n"
        f"DTEND;VALUE=DATE:{end}\n"
        "DTSTAMP:20241222T231407Z\n"
        f"DTSTART;VALUE=DATE:{start}\n"
        "LAST-MODIFIED:20241222T231124Z\n"
        "SEQUENCE:1\n"
        f"SUMMARY:{name}\n"
        "TRANSP:TRANSPARENT\n"
        f"UID:PREG-CAL-{name}-{hex}\n"
        "BEGIN:VALARM\n"
        "ACTION:NONE\n"
        "TRIGGER;VALUE=DATE-TIME:19760401T005545Z\n"
        "END:VALARM\n"
        "END:VEVENT\n"
    )
