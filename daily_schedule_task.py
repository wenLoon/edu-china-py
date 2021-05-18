import schedule
import time
import datetime
import mysql_insert as myjob

def daily_job():
    print('Job:每天下午00:00执行一次')
    print('Job-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    myjob.my_main_option()
    print('Job-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

def week_job():
    print('Job:周六00:00执行一次')
    print('Job-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    myjob.my_main_option()
    print('Job-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
    # schedule.every().day.at('00:00').do(daily_job)
    schedule.every().saturday.at("00:00").do(week_job) 
    while True:
        schedule.run_pending()
        time.sleep(100)