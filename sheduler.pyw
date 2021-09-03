import datetime
import sys
from time import sleep
from calendar import monthrange

from config_parser import ConfigParser


def calc_time(minute, hour, h_in_d=1, mp=1, days_till_event=0 ):
    d = datetime.datetime.today()
    time_to_wait = (minute*60 + hour*60*60) - (d.second + d.minute*60 + d.hour*60*60)
    time_to_wait += days_till_event*h_in_d*60*60
    if time_to_wait >= 0: time_to_wait = min(time_to_wait, 60*60*h_in_d*mp)
    else: time_to_wait += 60*60*h_in_d*mp
    return time_to_wait

def main():
    d = datetime.datetime.today()
    c = ConfigParser(
        filename = "sheduler_config.txt",
        config_header = "Sheduler_config",
        configs_list = ['period', 'skript_name_py']
    )
    config = c.get_configs()

    period_type = config['period'].split(', ')[0]
    period_mark = config['period'].split(', ')[1]
    try:
        period_mark_2 = config['period'].split(', ')[2]
    except IndexError:
        pass
    period_list = ['hourly', 'daily', 'weekly', 'monthly']
    days_otw = dict(enumerate(["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]))
    days_otw_rev = dict(zip(days_otw.values(), days_otw.keys()))
    
    d = datetime.datetime.today()
    if period_type == period_list[0]:
        # hourly, mm
        time_to_wait = calc_time(int(period_mark), d.hour)

    elif period_type == period_list[1]:
        # daily, hh:mm
        time_to_wait = calc_time(int(period_mark.split(':')[1]), 
                                int(period_mark.split(':')[0]), 
                                24)

    elif period_type == period_list[2]:
        # weekly, Mo
        temp = days_otw_rev[period_mark] - d.weekday()
        days_till_event = temp if temp >= 0 else temp + 7 
        time_to_wait = calc_time(int(period_mark_2.split(':')[1]), 
                                int(period_mark_2.split(':')[0]), 
                                24, 
                                7, 
                                days_till_event)

    elif period_type == period_list[3]:
        # monthly, 1-31(28)
        mth_max_days = monthrange(d.year, d.month)[1]
        dotm = min(int(period_mark), mth_max_days)
        temp = dotm - d.day
        days_till_event = temp if temp >= 0 else temp + mth_max_days 
        time_to_wait = calc_time(int(period_mark_2.split(':')[1]), 
                                int(period_mark_2.split(':')[0]), 
                                24, 
                                mth_max_days, 
                                days_till_event)


    print(f'Time to sleep: {time_to_wait}')
    try:
        if sys.argv[1] == 'time': pass
    except IndexError:
        sleep(time_to_wait)
        # run script with __name__ == __main__
        exec(open(config['skript_name_py']).read())


# sourcery skip: remove-redundant-if
if __name__ == '__main__':
    # try:
    #     if sys.argv[1] == 'time': print(f'Time to sleep: {time_to_wait}')
    # except IndexError: main()
    main()
    try:
        if sys.argv[1] == 'time': pass
    except IndexError:
        # loop this script
        try:
            exec(open(__file__).read())
        except RecursionError as f:
            print(str(f) + '. Please reload this script')
