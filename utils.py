import datetime

def valid_year(year):
  if year and year.isdigit():
    year = int(year)
    if year >=1900 and year <=2020:
      return year

def valid_month(month):
    return month

def is_current_year(year):
    currentYear = int(datetime.datetime.now().year)
    if year and year.isdigit():
        year = int(year)
        if year == currentYear:
            return year