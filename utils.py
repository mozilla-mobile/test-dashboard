import datetime
from datetime import datetime, timedelta


format_date = "%Y-%m-%d"
format_datetime = '%Y-%m-%dT%H:%M:%S.%fZ'


class Utils:

    def convert_datetime_to_epoch(str_date):
        str_to_dt = datetime.strptime(str_date, format_date)
        t = str_to_dt.timestamp()
        return int(t)

    def convert_epoch_to_datetime(str_epoch_date):
        e = int(str_epoch_date)
        ts = datetime.fromtimestamp(e)
        return ts.strftime(format_date)

    def start_date(num_days, end_date=''):
        """ given an end_date (default: now), calculate a start date num_days
        number of days in the past """

        if not end_date: 
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, format_date)
        d = end_date - timedelta(days=num_days)
        return d.strftime(format_date)
