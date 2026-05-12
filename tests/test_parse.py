from datetime import date

import pytest

from nldate import parse


class TestAbsoluteDates:
    def test_full_month_name(self) -> None:
        assert parse("December 1st, 2025") == date(2025, 12, 1)

    def test_abbreviated_month(self) -> None:
        assert parse("Dec 1, 2025") == date(2025, 12, 1)

    def test_no_comma(self) -> None:
        assert parse("January 15 2024") == date(2024, 1, 15)

    def test_numeric_date(self) -> None:
        assert parse("3/14/2024") == date(2024, 3, 14)

    def test_iso_date(self) -> None:
        assert parse("2024-12-25") == date(2024, 12, 25)


class TestRelativeDates:
    def test_today(self) -> None:
        assert parse("today", date(2025, 6, 15)) == date(2025, 6, 15)

    def test_yesterday(self) -> None:
        assert parse("yesterday", date(2025, 6, 15)) == date(2025, 6, 14)

    def test_tomorrow(self) -> None:
        assert parse("tomorrow", date(2025, 6, 15)) == date(2025, 6, 16)

    def test_in_days(self) -> None:
        assert parse("in 3 days", date(2025, 6, 15)) == date(2025, 6, 18)

    def test_in_weeks(self) -> None:
        assert parse("in 2 weeks", date(2025, 6, 15)) == date(2025, 6, 29)

    def test_in_months(self) -> None:
        assert parse("in 3 months", date(2025, 6, 15)) == date(2025, 9, 15)

    def test_in_years(self) -> None:
        assert parse("in 1 year", date(2025, 6, 15)) == date(2026, 6, 15)


class TestWeekdayReferences:
    def test_next_tuesday(self) -> None:
        # June 15, 2025 is a Sunday -> next Tuesday is June 17
        assert parse("next Tuesday", date(2025, 6, 15)) == date(2025, 6, 17)

    def test_next_monday_from_sunday(self) -> None:
        # June 15, 2025 is a Sunday -> next Monday is June 16
        assert parse("next Monday", date(2025, 6, 15)) == date(2025, 6, 16)

    def test_last_friday(self) -> None:
        # June 17, 2025 is a Tuesday -> last Friday is June 13
        assert parse("last Friday", date(2025, 6, 17)) == date(2025, 6, 13)

    def test_this_wednesday(self) -> None:
        # June 17, 2025 is a Tuesday -> this Wednesday is June 18
        assert parse("this Wednesday", date(2025, 6, 17)) == date(2025, 6, 18)

    def test_same_day_next(self) -> None:
        # June 16, 2025 is Monday -> next Monday should be June 23 (not today)
        assert parse("next Monday", date(2025, 6, 16)) == date(2025, 6, 23)


class TestOffsetExpressions:
    def test_days_before_absolute(self) -> None:
        assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)

    def test_days_after_absolute(self) -> None:
        assert parse("3 days after January 1, 2025") == date(2025, 1, 4)

    def test_weeks_before(self) -> None:
        assert parse("2 weeks before March 15, 2025") == date(2025, 3, 1)

    def test_months_before(self) -> None:
        assert parse("2 months before December 1st, 2025") == date(2025, 10, 1)

    def test_years_after(self) -> None:
        assert parse("1 year after January 1, 2025") == date(2026, 1, 1)

    def test_compound_offset(self) -> None:
        # 1 year and 2 months after June 1, 2025 = August 1, 2026
        assert parse(
            "1 year and 2 months after June 1, 2025",
        ) == date(2026, 8, 1)

    def test_compound_offset_reversed(self) -> None:
        assert parse(
            "2 months and 1 year after June 1, 2025",
        ) == date(2026, 8, 1)

    def test_days_before_relative(self) -> None:
        # 5 days before yesterday from June 15 -> June 9
        assert parse(
            "5 days before yesterday",
            date(2025, 6, 15),
        ) == date(2025, 6, 9)

    def test_days_after_relative(self) -> None:
        # 3 days after tomorrow from June 15 -> June 19
        assert parse(
            "3 days after tomorrow",
            date(2025, 6, 15),
        ) == date(2025, 6, 19)

    def test_compound_after_yesterday(self) -> None:
        # 1 year and 2 months after yesterday from June 15, 2025
        # yesterday = June 14, 2025
        # + 1 year = June 14, 2026
        # + 2 months = August 14, 2026
        assert parse(
            "1 year and 2 months after yesterday",
            date(2025, 6, 15),
        ) == date(2026, 8, 14)


class TestEdgeCases:
    def test_default_today(self) -> None:
        result = parse("today")
        assert result == date.today()

    def test_next_tuesday_no_today(self) -> None:
        result = parse("next Tuesday")
        assert isinstance(result, date)

    def test_month_end_clamping(self) -> None:
        # Jan 31 + 1 month -> Feb 28 (2024 is leap year -> Feb 29)
        assert parse(
            "in 1 month",
            date(2024, 1, 31),
        ) == date(2024, 2, 29)

    def test_month_end_clamping_year(self) -> None:
        # Jan 31 + 1 month (non-leap) -> Feb 28
        assert parse(
            "in 1 month",
            date(2025, 1, 31),
        ) == date(2025, 2, 28)

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError, match="Unable to parse date"):
            parse("not a date at all")

    def test_ordinal_dates(self) -> None:
        assert parse("March 3rd, 2024") == date(2024, 3, 3)
        assert parse("June 2nd, 2024") == date(2024, 6, 2)
        assert parse("January 21st, 2024") == date(2024, 1, 21)
        assert parse("April 4th, 2024") == date(2024, 4, 4)
