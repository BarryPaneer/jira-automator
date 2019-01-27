from jira import JIRA
from ..jw_log import get_logger


log = get_logger(__package__)


class Transition2Backlog:
    def __init__(self, jira_session, issue_):
        self.__jira_session = jira_session
        self.__issue_ = issue_

    def __call__(self):
        action_table = ['reopen issue', 'start progress',
                        'stop progress', 'fail testing', 'revert']

        self.__transition_in_workflow(action_table)

    def __transition_in_workflow(self, action_table):
        transitions_json = self.__jira_session.transitions(self.__issue_)

        for transition in transitions_json:
            next_step_name = transition['name'].lower()

            for action in action_table:

                if action in next_step_name:
                    self.__jira_session.transition_issue(self.__issue_,
                                                         transition=action)
                    action_table.remove(action)
                    log.info('[JIRA] Transition :{0} --> {1}'.format(
                                            self.__issue_.key, action))
                    self.__transition_in_workflow(action_table)
                    break


class TicketsScanner:
    def __init__(self, server, login_name, login_password,
                 filter_cond, notice_for_assignee, notice_for_reporter):
        self.__options = {'server': server, 'validate': True}
        self.__login_account = (login_name, login_password)
        self.__filter_cond = filter_cond
        self.__notice_for_assignee = notice_for_assignee
        self.__notice_for_reporter = notice_for_reporter
        log.info('[JIRA] mission activated...')

    def __login(self):
        log.info('[JIRA] [{0}] sign in, please wait...'.format(
                    self.__login_account[0]
            )
        )
        jira_session = JIRA(
                            basic_auth=self.__login_account,
                            options=self.__options
                            )
        log.info('[JIRA] ok!')

        return jira_session

    def scan(self):
        try:
            reset_count = 0
            jira_session = self.__login()

            log.info('[JIRA] scanning miss time issue...')
            misstime_issues = jira_session.search_issues(self.__filter_cond)
            log.info('[JIRA] issue count: {0}'.format(len(misstime_issues)))

            if 0 == len(misstime_issues):
                return True

            for issue_ in misstime_issues:
                try:
                    self.__reset_misstime_issue(jira_session, issue_)
                    reset_count += 1
                except Exception as e:
                    log.error('[EXCEPTION] {0}'.format(str(e)))

            log.info('[JIRA] mission complete !')

            if reset_count > 0:
                return True
            else:
                log.warn('[JIRA] [WARNING] retry later...')

        except Exception as e:
            log.error('[EXCEPTION] scan() :: {0}'.format(str(e)))

        return False

    def __reset_misstime_issue(self, jira_session, issue_):
        log.info('[JIRA] Issue\'s KEY[{0}] current status: "{1}"'.format(
                issue_.key, issue_.fields.status.name
                )
        )

        # exit when timespent has a value
        if issue_.fields.timespent:
            log.warn('[JIRA] issue.timespend is not null/zero, skip...')
            return

        # setback
        Transition2Backlog(jira_session, issue_)()

        if issue_.fields.assignee:
            msg_to_assignee = '[~{0}] {1}'.format(
                    issue_.fields.assignee.name,
                    self.__notice_for_assignee
            )

            jira_session.add_comment(issue_, msg_to_assignee)
            log.info('[OK] notify assignee[{0}]'.format(
                    issue_.fields.assignee.name
                    )
            )
        else:
            msg_to_reporter = '[~{0}] {1}'.format(
                    issue_.fields.reporter.name,
                    self.__notice_for_reporter
            )

            jira_session.add_comment(issue_, msg_to_reporter)
            log.info('[OK] notify reporter[{0}]'.format(
                    issue_.fields.reporter.name
                    )
            )
