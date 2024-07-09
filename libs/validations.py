import re

def isValidYearParam(yearParam):
    MIN_YEAR = 1970
    MAX_YEAR = 2023

    isValidFormat = re.match(r'^\d{4}(\-\d{4})?$', yearParam) is not None
    if not isValidFormat:
        return False

    if len(yearParam) == 9:
        years = yearParam.split("-")
        if int(years[0]) > int(years[1]):
            return False

        if int(years[0]) < MIN_YEAR or int(years[1]) > MAX_YEAR:
            return False
    elif int(yearParam) < MIN_YEAR or int(yearParam) > MAX_YEAR:
        return False

    return True