"""reset miss time tickets and remind"""
import os
import time
import datetime
from argparse import ArgumentParser
from ConfigParser import RawConfigParser
from tickets_scanner import TicketsScanner
from calendar import monthrange


def __get_args_parser():
    arg_parser = ArgumentParser(description=__doc__)

    arg_parser.add_argument('cfg',
                            help='Input Configuration',
                            nargs='*',
                            type=str,
                            default=os.path.abspath(
                                os.path.dirname(
                                    os.path.dirname(__file__)
                                    )
                                ) + '/settings.cfg'
                            )

    arg_parser.add_argument('-x', '--exec-once',
                            action='store_true',
                            help='script will not run in scheduler mode')

    return arg_parser


def __is_last_day_of_month(year, month, day):
    last_days_month = monthrange(year, month)[1]

    return last_days_month == day


def main():
    last_activate_date_ = 19700101
    options = __get_args_parser().parse_args()

    print('configuration path: {0}'.format(options.cfg))

    while True:
        if not options.exec_once:
            time.sleep(30)

        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        today = year * 10000 + month * 100 + day

        if (__is_last_day_of_month(year, month, day) and
                today > last_activate_date_) or options.exec_once:

            if datetime.datetime.now().hour != 9 and not options.exec_once:
                continue  # [ServiceMode] not in working time

            config = RawConfigParser()
            config.read(options.cfg)
            jira_url = config.get('JIRA_MISS_TIME', 'jira_url')
            login_name = config.get('JIRA_MISS_TIME', 'login_name')
            login_password = config.get('JIRA_MISS_TIME', 'login_password')
            filter_condition = config.get('JIRA_MISS_TIME', 'filter')
            notice_for_assignee = config.get('JIRA_MISS_TIME',
                                             'notice_for_assignee')
            notice_for_reporter = config.get('JIRA_MISS_TIME',
                                             'notice_for_reporter')

            scanner = TicketsScanner(
                jira_url,
                login_name,
                login_password,
                filter_condition,
                notice_for_assignee,
                notice_for_reporter
            )

            # if get a failure then retry.
            if scanner.scan():
                last_activate_date_ = today

        if options.exec_once:
            break


if __name__ == '__main__':
    main()
