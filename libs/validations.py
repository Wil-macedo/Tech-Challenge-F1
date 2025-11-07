"""
Validation functions for query parameters.
"""
import re


def is_valid_year_param(year_param):
    """
    Validate year parameter format and range.

    Args:
        year_param: String representing a year (YYYY) or year range (YYYY-YYYY)

    Returns:
        bool: True if valid, False otherwise
    """
    min_year = 1970
    max_year = 2023

    is_valid_format = re.match(r'^\d{4}(\-\d{4})?$', year_param) is not None
    if not is_valid_format:
        return False

    if len(year_param) == 9:
        years = year_param.split("-")
        if int(years[0]) > int(years[1]):
            return False

        if int(years[0]) < min_year or int(years[1]) > max_year:
            return False
    elif int(year_param) < min_year or int(year_param) > max_year:
        return False

    return True
