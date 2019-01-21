from jira import JIRA


class TicketsScanner:
    def __init__(self, server, login_name, login_password, filter_cond):
        self.__options = {'server': server, 'validate': True}
        self.__login_account = (login_name, login_password)
        self.__filter_cond = filter_cond

    def __login(self):
        print('[JIRA] sign in, please wait...')
        jira_session = JIRA(
                            basic_auth=self.__login_account
                            , options=self.__options
                            )
        print('[JIRA] ok!')

        return jira_session

    def scan(self):
        jira_session = self.__login()

        print('[JIRA] scanning...')
        all_issues = jira_session.search_issues(self.__filter_cond)
        print('[JIRA] issue count: {0}'.format(len(all_issues)))


