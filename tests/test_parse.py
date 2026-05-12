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

    def test_yyyy_slash_date(self) -> None:
        assert parse("2025/12/04") == date(2025, 12, 4)

    def test_yyyy_slash_no_pad(self) -> None:
        assert parse("2025/12/3") == date(2025, 12, 3)

    def test_day_before_month(self) -> None:
        assert parse("1 December 2025") == date(2025, 12, 1)

    def test_ordinal_day_before_month(self) -> None:
        assert parse("1st December 2025") == date(2025, 12, 1)

    def test_day_of_month(self) -> None:
        assert parse("1 of December 2025") == date(2025, 12, 1)

    def test_the_day_of_month(self) -> None:
        assert parse("the 1st of December, 2025") == date(2025, 12, 1)

    def test_the_day_of_month_no_ordinal(self) -> None:
        assert parse("the 5 of June 2024") == date(2024, 6, 5)

    def test_period_after_month(self) -> None:
        assert parse("Dec. 1, 2025") == date(2025, 12, 1)

    def test_period_no_space(self) -> None:
        assert parse("Dec.1, 2025") == date(2025, 12, 1)

    def test_sept_abbreviation(self) -> None:
        assert parse("Sept. 5, 2024") == date(2024, 9, 5)


class TestRelativeDates:
    def test_today(self) -> None:
        assert parse("today", date(2025, 6, 15)) == date(2025, 6, 15)

    def test_yesterday(self) -> None:
        assert parse("yesterday", date(2025, 6, 15)) == date(2025, 6, 14)

    def test_tomorrow(self) -> None:
        assert parse("tomorrow", date(2025, 6, 15)) == date(2025, 6, 16)

    def test_day_after_tomorrow(self) -> None:
        assert parse("the day after tomorrow", date(2025, 6, 15)) == date(2025, 6, 17)

    def test_day_before_yesterday(self) -> None:
        assert parse("the day before yesterday", date(2025, 6, 15)) == date(2025, 6, 13)

    def test_in_days(self) -> None:
        assert parse("in 3 days", date(2025, 6, 15)) == date(2025, 6, 18)

    def test_in_weeks(self) -> None:
        assert parse("in 2 weeks", date(2025, 6, 15)) == date(2025, 6, 29)

    def test_in_months(self) -> None:
        assert parse("in 3 months", date(2025, 6, 15)) == date(2025, 9, 15)

    def test_in_years(self) -> None:
        assert parse("in 1 year", date(2025, 6, 15)) == date(2026, 6, 15)

    def test_in_a_day(self) -> None:
        assert parse("in a day", date(2025, 6, 15)) == date(2025, 6, 16)

    def test_in_a_week(self) -> None:
        assert parse("in a week", date(2025, 6, 15)) == date(2025, 6, 22)

    def test_in_a_month(self) -> None:
        assert parse("in a month", date(2025, 6, 15)) == date(2025, 7, 15)

    def test_in_a_year(self) -> None:
        assert parse("in a year", date(2025, 6, 15)) == date(2026, 6, 15)

    def test_days_from_now(self) -> None:
        assert parse("3 days from now", date(2025, 6, 15)) == date(2025, 6, 18)

    def test_weeks_from_today(self) -> None:
        assert parse("2 weeks from today", date(2025, 6, 15)) == date(2025, 6, 29)

    def test_a_week_from_now(self) -> None:
        assert parse("a week from now", date(2025, 6, 15)) == date(2025, 6, 22)

    def test_a_month_from_today(self) -> None:
        assert parse("a month from today", date(2025, 6, 15)) == date(2025, 7, 15)

    def test_next_week(self) -> None:
        assert parse("next week", date(2025, 6, 15)) == date(2025, 6, 22)

    def test_last_week(self) -> None:
        assert parse("last week", date(2025, 6, 15)) == date(2025, 6, 8)

    def test_next_month(self) -> None:
        assert parse("next month", date(2025, 6, 15)) == date(2025, 7, 15)

    def test_last_month(self) -> None:
        assert parse("last month", date(2025, 6, 15)) == date(2025, 5, 15)

    def test_next_year(self) -> None:
        assert parse("next year", date(2025, 6, 15)) == date(2026, 6, 15)

    def test_last_year(self) -> None:
        assert parse("last year", date(2025, 6, 15)) == date(2024, 6, 15)

    def test_days_ago(self) -> None:
        assert parse("3 days ago", date(2025, 6, 15)) == date(2025, 6, 12)

    def test_weeks_ago(self) -> None:
        assert parse("2 weeks ago", date(2025, 6, 15)) == date(2025, 6, 1)

    def test_months_ago(self) -> None:
        assert parse("1 month ago", date(2025, 6, 15)) == date(2025, 5, 15)

    def test_years_ago(self) -> None:
        assert parse("1 year ago", date(2025, 6, 15)) == date(2024, 6, 15)

    def test_a_day_ago(self) -> None:
        assert parse("a day ago", date(2025, 6, 15)) == date(2025, 6, 14)

    def test_days_earlier(self) -> None:
        assert parse("3 days earlier", date(2025, 6, 15)) == date(2025, 6, 12)

    def test_weeks_later(self) -> None:
        assert parse("2 weeks later", date(2025, 6, 15)) == date(2025, 6, 29)

    def test_a_day_earlier(self) -> None:
        assert parse("a day earlier", date(2025, 6, 15)) == date(2025, 6, 14)

    def test_a_month_later(self) -> None:
        assert parse("a month later", date(2025, 6, 15)) == date(2025, 7, 15)

    def test_days_back(self) -> None:
        assert parse("3 days back", date(2025, 6, 15)) == date(2025, 6, 12)

    def test_a_week_back(self) -> None:
        assert parse("a week back", date(2025, 6, 15)) == date(2025, 6, 8)

    def test_word_days_ago(self) -> None:
        assert parse("two weeks ago", date(2025, 6, 15)) == date(2025, 6, 1)

    def test_word_in_days(self) -> None:
        assert parse("in five days", date(2025, 6, 15)) == date(2025, 6, 20)

    def test_word_from_now(self) -> None:
        assert parse("ten days from now", date(2025, 6, 15)) == date(2025, 6, 25)

    def test_word_days_back(self) -> None:
        assert parse("four days back", date(2025, 6, 15)) == date(2025, 6, 11)

    def test_word_day_earlier(self) -> None:
        assert parse("one month later", date(2025, 6, 15)) == date(2025, 7, 15)

    def test_word_in_one_month(self) -> None:
        assert parse("in one month", date(2025, 6, 15)) == date(2025, 7, 15)


class TestWeekdayReferences:
    def test_next_tuesday(self) -> None:
        assert parse("next Tuesday", date(2025, 6, 15)) == date(2025, 6, 17)

    def test_next_monday_from_sunday(self) -> None:
        assert parse("next Monday", date(2025, 6, 15)) == date(2025, 6, 16)

    def test_last_friday(self) -> None:
        assert parse("last Friday", date(2025, 6, 17)) == date(2025, 6, 13)

    def test_this_wednesday(self) -> None:
        assert parse("this Wednesday", date(2025, 6, 17)) == date(2025, 6, 18)

    def test_same_day_next(self) -> None:
        assert parse("next Monday", date(2025, 6, 16)) == date(2025, 6, 23)

    def test_this_coming_tuesday(self) -> None:
        assert parse("this coming Tuesday", date(2025, 6, 15)) == date(2025, 6, 17)

    def test_this_past_friday(self) -> None:
        assert parse("this past Friday", date(2025, 6, 17)) == date(2025, 6, 13)


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
        assert parse("1 year and 2 months after June 1, 2025") == date(2026, 8, 1)

    def test_compound_offset_reversed(self) -> None:
        assert parse("2 months and 1 year after June 1, 2025") == date(2026, 8, 1)

    def test_days_before_yesterday(self) -> None:
        assert parse("5 days before yesterday", date(2025, 6, 15)) == date(2025, 6, 9)

    def test_days_after_tomorrow(self) -> None:
        assert parse("3 days after tomorrow", date(2025, 6, 15)) == date(2025, 6, 19)

    def test_compound_after_yesterday(self) -> None:
        assert parse("1 year and 2 months after yesterday", date(2025, 6, 15)) == date(
            2026, 8, 14
        )

    def test_a_day_before_yesterday(self) -> None:
        assert parse("a day before yesterday", date(2025, 6, 15)) == date(2025, 6, 13)

    def test_days_before_day_after_tomorrow(self) -> None:
        assert parse("2 days before the day after tomorrow", date(2025, 6, 15)) == date(
            2025, 6, 15
        )

    def test_word_offset_before(self) -> None:
        assert parse("three days before December 1st, 2025") == date(2025, 11, 28)

    def test_word_compound_offset(self) -> None:
        assert parse(
            "one year and two months after yesterday", date(2025, 6, 15)
        ) == date(2026, 8, 14)


class TestEdgeCases:
    def test_default_today(self) -> None:
        result = parse("today")
        assert result == date.today()

    def test_next_tuesday_no_today(self) -> None:
        result = parse("next Tuesday")
        assert isinstance(result, date)

    def test_month_end_clamping(self) -> None:
        assert parse("in 1 month", date(2024, 1, 31)) == date(2024, 2, 29)

    def test_month_end_clamping_nonleap(self) -> None:
        assert parse("in 1 month", date(2025, 1, 31)) == date(2025, 2, 28)

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError, match="Unable to parse date"):
            parse("not a date at all")

    def test_ordinal_dates(self) -> None:
        assert parse("March 3rd, 2024") == date(2024, 3, 3)
        assert parse("June 2nd, 2024") == date(2024, 6, 2)
        assert parse("January 21st, 2024") == date(2024, 1, 21)
        assert parse("April 4th, 2024") == date(2024, 4, 4)
