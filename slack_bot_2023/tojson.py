import datetime
import time

today_date_time = datetime.datetime.now()
print("first day Date:", today_date_time.day - today_date_time.day + 1)

latest_date_time = time.mktime(today_date_time.timetuple())
print("latest UNIX timestamp:", latest_date_time)

oldest_date_time = datetime.datetime(year=today_date_time.year, month=today_date_time.month,
                                     day=today_date_time.day - today_date_time.day + 1, hour=0, minute=0, second=0)
print("oldest UNIX timestamp:", time.mktime(oldest_date_time.timetuple()))
