from tickets_scanner import TicketsScanner


filter_condition = 'project in ("Consumer Products", "Industry Products", "Platform Products", XML, Salesforce, LOC) AND status in (Closed, Done, "PM Testing", Testing) AND type not in (Epic, subTaskIssueTypes()) AND (timespent is EMPTY OR timespent = 0) AND fixVersion is EMPTY AND updated >= 2017-11-01 ORDER BY Status DESC, updated DESC '


def __main():
    scanner = TicketsScanner('http://jira.juwai.com', 'barry.bao', 'wsjkdwyqwj@2019', filter_condition)
    scanner.scan()


if __name__ == '__main__':
    __main()
