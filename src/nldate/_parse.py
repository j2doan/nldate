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
    "sept": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

_WEEK_UNITS = ("week", "weeks", "day", "days", "month", "months", "year", "years")

_WORD_NUM: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}

_WORD_PAT = "(?:" + "|".join(_WORD_NUM) + ")"


def _to_int(s: str) -> int:
    s = s.strip().lower()
    if s in _WORD_NUM:
        return _WORD_NUM[s]
    if s == "a":
        return 1
    return int(s)


def _add_months(d: date, months: int) -> date:
    total = d.month - 1 + months
    y = d.year + total // 12
    m = total % 12 + 1
    max_day = calendar.monthrange(y, m)[1]
    return date(y, m, min(d.day, max_day))


def _apply_offset(d: date, n: int, unit: str, direction: str) -> date:
    if direction == "before":
        if unit == "day":
            return d - timedelta(days=n)
        if unit == "week":
            return d - timedelta(weeks=n)
        if unit == "month":
            return _add_months(d, -n)
        if unit == "year":
            return _add_months(d, -n * 12)
    else:
        if unit == "day":
            return d + timedelta(days=n)
        if unit == "week":
            return d + timedelta(weeks=n)
        if unit == "month":
            return _add_months(d, n)
        if unit == "year":
            return _add_months(d, n * 12)
    return d


def _parse_absolute(s: str) -> date | None:
    s = s.strip()

    # "December 1st, 2025" / "Dec. 1, 2025"
    m = re.match(
        r"([a-zA-Z]+)\.?\s*(\d{1,2})(?:st|nd|rd|th)?\s*,?\s*(\d{4})",
        s,
    )
    if m:
        month_name = m.group(1).lower()
        if month_name in _MONTHS:
            return date(int(m.group(3)), _MONTHS[month_name], int(m.group(2)))

    # "the 1st of December, 2025"
    m = re.match(
        r"the\s+(\d{1,2})(?:st|nd|rd|th)?\s+of\s+([a-zA-Z]+)\.?\s*,?\s*(\d{4})",
        s,
        re.IGNORECASE,
    )
    if m:
        month_name = m.group(2).lower()
        if month_name in _MONTHS:
            return date(int(m.group(3)), _MONTHS[month_name], int(m.group(1)))

    # "1 December 2025" / "1st December 2025" / "1 of December 2025"
    m = re.match(
        r"(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-zA-Z]+)\.?\s*,?\s*(\d{4})",
        s,
    )
    if m:
        month_name = m.group(2).lower()
        if month_name in _MONTHS:
            return date(int(m.group(3)), _MONTHS[month_name], int(m.group(1)))

    # "2025/12/04" / "2025/12/3"
    m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    # "3/14/2024"
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(1)), int(m.group(2)))

    # "2024-12-25"
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))

    return None


def _parse_relative(s: str, today: date) -> date | None:
    s = s.strip().lower()

    # Exact phrases
    if s == "today":
        return today
    if s == "yesterday":
        return today - timedelta(days=1)
    if s == "tomorrow":
        return today + timedelta(days=1)
    if s in ("the day after tomorrow", "day after tomorrow"):
        return today + timedelta(days=2)
    if s in ("the day before yesterday", "day before yesterday"):
        return today - timedelta(days=2)

    # "next Tuesday" / "last Friday" / "this Wednesday"
    m = re.match(
        r"(next|last|this)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
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

    # "this coming Tuesday" / "this past Friday"
    m = re.match(
        r"this\s+(?:coming\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
        s,
    )
    if m:
        target = _WEEKDAYS[m.group(1)]
        current = today.weekday()
        days_ahead = target - current
        if days_ahead < 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)

    m = re.match(
        r"this\s+past\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", s
    )
    if m:
        target = _WEEKDAYS[m.group(1)]
        current = today.weekday()
        days_behind = current - target
        if days_behind <= 0:
            days_behind += 7
        return today - timedelta(days=days_behind)

    # "next week" / "next month" / "next year" / "last week" / etc.
    m = re.match(r"(next|last)\s+(week|month|year)", s)
    if m:
        modifier = m.group(1)
        unit = m.group(2)
        if modifier == "next":
            if unit == "week":
                return today + timedelta(weeks=1)
            if unit == "month":
                return _add_months(today, 1)
            if unit == "year":
                return _add_months(today, 12)
        else:
            if unit == "week":
                return today - timedelta(weeks=1)
            if unit == "month":
                return _add_months(today, -1)
            if unit == "year":
                return _add_months(today, -12)

    # "in a day" / "in a week" / "in a month" / "in a year"
    m = re.match(r"in\s+a\s+(day|week|month|year)", s)
    if m:
        unit = m.group(1)
        if unit == "day":
            return today + timedelta(days=1)
        if unit == "week":
            return today + timedelta(weeks=1)
        if unit == "month":
            return _add_months(today, 1)
        if unit == "year":
            return _add_months(today, 12)

    # "in 3 days" / "in 2 weeks" / "in one month"
    m = re.match(
        rf"in\s+({_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)", s
    )
    if m:
        n = _to_int(m.group(1))
        unit = m.group(2).rstrip("s")
        return _apply_offset(today, n, unit, "after")

    # "a week from now" / "a week from today"
    m = re.match(r"a\s+(day|week|month|year)\s+from\s+(now|today)", s)
    if m:
        unit = m.group(1)
        return _apply_offset(today, 1, unit, "after")

    # "3 days from now" / "two weeks from today"
    m = re.match(
        rf"({_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+from\s+(now|today)",
        s,
    )
    if m:
        n = _to_int(m.group(1))
        unit = m.group(2).rstrip("s")
        return _apply_offset(today, n, unit, "after")

    # "a day ago" / "an hour ago" (only date units for "a")
    m = re.match(r"a\s+(day|week|month|year)\s+ago", s)
    if m:
        unit = m.group(1)
        return _apply_offset(today, 1, unit, "before")

    # "3 days ago" / "two weeks ago" / "1 month ago"
    m = re.match(
        rf"({_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+ago", s
    )
    if m:
        n = _to_int(m.group(1))
        unit = m.group(2).rstrip("s")
        return _apply_offset(today, n, unit, "before")

    # "a day earlier" / "a month later"
    m = re.match(r"a\s+(day|week|month|year)\s+(earlier|later)", s)
    if m:
        unit = m.group(1)
        direction = "before" if m.group(2) == "earlier" else "after"
        return _apply_offset(today, 1, unit, direction)

    # "3 days earlier" / "two weeks later"
    m = re.match(
        rf"({_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+(earlier|later)",
        s,
    )
    if m:
        n = _to_int(m.group(1))
        unit = m.group(2).rstrip("s")
        direction = "before" if m.group(3) == "earlier" else "after"
        return _apply_offset(today, n, unit, direction)

    # "a day back" / "three days back"
    m = re.match(
        rf"(a|{_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)\s+back",
        s,
    )
    if m:
        n = _to_int(m.group(1))
        unit = m.group(2).rstrip("s")
        return _apply_offset(today, n, unit, "before")

    return None


def _resolve_date(s: str, today: date) -> date:
    s = s.strip()

    result = _parse_absolute(s)
    if result is not None:
        return result

    result = _parse_relative(s, today)
    if result is not None:
        return result

    # "5 days before December 1st, 2025" / "a day before yesterday"
    m = re.match(r"(.+?)\s+(before|after)\s+(.+)", s, re.IGNORECASE)
    if m:
        offset_text = m.group(1).strip()
        direction = m.group(2).lower()
        ref_text = m.group(3).strip()

        components = re.findall(
            rf"(a|{_WORD_PAT}|\d+)\s+(day|days|week|weeks|month|months|year|years)",
            offset_text,
            re.IGNORECASE,
        )
        if components:
            ref = _resolve_date(ref_text, today)
            for n_str, unit in components:
                n = _to_int(n_str)
                unit_s = unit.rstrip("s")
                ref = _apply_offset(ref, n, unit_s, direction)
            return ref

    raise ValueError(f"Unable to parse date: {s!r}")


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()
    return _resolve_date(s, today)
