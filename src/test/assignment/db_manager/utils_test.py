from datetime import date
from main.assignment.db_manager.utils import _get_previous_month
from main.assignment.db_manager.utils import _get_next_month


def _get_previous_month_january_test():
    current_date = date(2021, 1, 1)

    actual_date = _get_previous_month(current_date)
    expect_date = date(2020, 12, 1)

    assert actual_date == expect_date


def _get_previous_month_february_test():
    current_date = date(2021, 2, 1)

    actual_date = _get_previous_month(current_date)
    expect_date = date(2021, 1, 1)

    assert actual_date == expect_date


def _get_previous_month_december_test():
    current_date = date(2021, 12, 1)

    actual_date = _get_previous_month(current_date)
    expect_date = date(2021, 11, 1)

    assert actual_date == expect_date


def __get_next_month_january_test():
    current_date = date(2021, 1, 1)

    actual_date = _get_next_month(current_date)
    expect_date = date(2021, 2, 1)

    assert actual_date == expect_date


def _get_next_month_february_test():
    current_date = date(2021, 2, 1)

    actual_date = _get_next_month(current_date)
    expect_date = date(2021, 3, 1)

    assert actual_date == expect_date


def _get_next_month_december_test():
    current_date = date(2021, 12, 1)

    actual_date = _get_next_month(current_date)
    expect_date = date(2022, 1, 1)

    assert actual_date == expect_date
