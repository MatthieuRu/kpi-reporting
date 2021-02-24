from datetime import date
from datetime import timedelta
from random import randrange


def _get_previous_month(
    current_month: date
) -> date:
    """Get the previous month from a date

    Args:
        current_month (date): current month

    Returns:
        date: previous month
    """
    # Get previous month
    if current_month.month == 1:
        previous_month = date(
            current_month.year - 1,
            12,
            1
        )
        return previous_month
    else:
        previous_month = date(
            current_month.year,
            current_month.month - 1,
            1
        )
    return previous_month


def _get_next_month(
    current_month: date
) -> date:
    """Get the next month from a date

    Args:
        current_month (date): next month

    Returns:
        date: next month
    """
    # Get previous month
    if current_month.month == 12:
        next_month = date(
            current_month.year + 1,
            1,
            1
        )
        return next_month
    else:
        next_month = date(
            current_month.year,
            current_month.month + 1,
            1
        )
        return next_month


def _random_date(
    start: date,
    end: date
) -> date:
    """Get random date between two dates

    Args:
        start (date):  start date
        end (date): end date

    Returns:
        date: random date bewteen start and end date
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
