import calendar
import re
from datetime import date, timedelta

_WEEKDAYS: dict[str, int] = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

_MONTHS: dict[str, int] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def _add_months(d: date, months: int) -> date:
    total = d.month - 1 + months
    y = d.year + total // 12
    m = total % 12 + 1
    max_day = calendar.monthrange(y, m)[1]
    return date(y, m, min(d.day, max_day))


def _parse_absolute(s: str) -> date | None:
    s = s.strip()
    m = re.match(
        r"([a-zA-Z]+)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*(\d{4})",
        s,
    )
    if m:
        month_name = m.group(1).lower()
        day = int(m.group(2))
        year = int(m.group(3))
        if month_name in _MONTHS:
            return date(year, _MONTHS[month_name], day)
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def _parse_relative(s: str, today: date) -> date | None:
    s = s.strip().lower()
    if s == "today":
        return today
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "tomorrow":
        return today + timedelta(days=1)
    m = re.match(
        r"(next|last|this)\s+"
        r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
        s,
    )
    if m:
        modifier = m.group(1)
        target = _WEEKDAYS[m.group(2)]
        current = today.weekday()
        if modifier == "next":
            days_ahead = target - current
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        if modifier == "last":
            days_behind = current - target
            if days_behind <= 0:
                days_behind += 7
            return today - timedelta(days=days_behind)
        if modifier == "this":
            days_ahead = target - current
            if days_ahead < 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
    m = re.match(r"in\s+(\d+)\s+(day|days|week|weeks|month|months|year|years)", s)
    if m:
        n = int(m.group(1))
        unit = m.group(2).rstrip("s")
        if unit == "day":
            return today + timedelta(days=n)
        if unit == "week":
            return today + timedelta(weeks=n)
        if unit == "month":
            return _add_months(today, n)
        if unit == "year":
            return _add_months(today, n * 12)
    return None


def _resolve_date(s: str, today: date) -> date:
    s = s.strip()
    result = _parse_absolute(s)
    if result is not None:
        return result
    result = _parse_relative(s, today)
    if result is not None:
        return result
    m = re.match(
        r"(.+?)\s+(before|after)\s+(.+)",
        s,
        re.IGNORECASE,
    )
    if m:
        offset_text = m.group(1).strip()
        direction = m.group(2).lower()
        ref_text = m.group(3).strip()
        components = re.findall(
            r"(\d+)\s+(day|days|week|weeks|month|months|year|years)",
            offset_text,
            re.IGNORECASE,
        )
        if components:
            ref = _resolve_date(ref_text, today)
            for n_str, unit in components:
                n = int(n_str)
                unit_s = unit.rstrip("s")
                if direction == "before":
                    if unit_s == "day":
                        ref -= timedelta(days=n)
                    elif unit_s == "week":
                        ref -= timedelta(weeks=n)
                    elif unit_s == "month":
                        ref = _add_months(ref, -n)
                    elif unit_s == "year":
                        ref = _add_months(ref, -n * 12)
                else:
                    if unit_s == "day":
                        ref += timedelta(days=n)
                    elif unit_s == "week":
                        ref += timedelta(weeks=n)
                    elif unit_s == "month":
                        ref = _add_months(ref, n)
                    elif unit_s == "year":
                        ref = _add_months(ref, n * 12)
            return ref
    raise ValueError(f"Unable to parse date: {s!r}")


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()
    return _resolve_date(s, today)
