from jira import JIRA
from ..jw_log import get_logger


log = get_logger(__package__)


class TicketsScanner:
    def __init__(self, server, login_name, login_password, filter_cond):
        self.__options = {'server': server, 'validate': True}
        self.__login_account = (login_name, login_password)
        self.__filter_cond = filter_cond
        log.info('[JIRA] mission activated...')

    def __login(self):
        try:
            log.info('[JIRA] [{0}] sign in, please wait...'.format(
                        self.__login_account[0]
                )
            )
            jira_session = JIRA(
                                basic_auth=self.__login_account,
                                options=self.__options
                                )
            log.info('[JIRA] ok!')
        except Exception as e:
            log.error('[EXCEPTION] {0}'.format(str(e)))
            raise

        return jira_session

    def scan(self):
        jira_session = self.__login()

        log.info('[JIRA] scanning miss time issue...')
        misstime_issues = jira_session.search_issues(self.__filter_cond)
        log.info('[JIRA] issue count: {0}'.format(len(misstime_issues)))

        for issue_ in misstime_issues:
            try:
                self.__reset_misstime_issue(jira_session, issue_)
            except Exception as e:
                log.error('[EXCEPTION] {0}'.format(str(e)))

        log.info('[JIRA] mission complete !')

    def __reset_misstime_issue(self, jira_session, issue_):
        log.info('[JIRA] Issue\'s KEY[{0}] current status: "{1}"'.format(
                issue_.key, issue_.fields.status.name
                )
        )

        jira_session.transition_issue(issue_, transition='In Progress')

        if issue_.fields.assignee:
            msg_to_assignee = '[~{0}] {1}'.format(
                    issue_.fields.assignee.name,
                    'hey guy, log time, pls...'
            )

            jira_session.add_comment(issue_, msg_to_assignee)
            log.info('[OK] notify assignee[{0}] ->"In Progress"'.format(
                    issue_.fields.assignee.name
                    )
            )
        else:
            msg_to_reporter = '[~{0}] {1}'.format(
                    issue_.fields.reporter.name,
                    'hey guy, the issue is expired...'
            )

            jira_session.add_comment(issue_, msg_to_reporter)
            log.info('[OK] notify reporter[{0}] ->"In Progress"'.format(
                    issue_.fields.reporter.name
                    )
            )
