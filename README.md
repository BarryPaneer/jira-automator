# Jira Automator Tool

## Requirements
* Python >=2.7 <3
* jira == 2.0.0

## How to install

1. Install `ve` if you don't have it yet:
    ```
    # curl -kL "https://raw.githubusercontent.com/erning/ve/master/ve" -o "/usr/local/bin/ve"
    ```

    Next, change permission for ve:
    ```
    # chmod +x /usr/local/bin/ve
    ```

2. Do the following steps:
    ```
    $ git clone git@github.com:juwai/jira-automator.git
    $ cd xml
    $ virtualenv .virtualenv
    $ ve pip install -r requirements.txt
    ```

    Next:
    ```
    $ ve python setup.py develop --no-deps
    ```

3. Finally, configure your `settings.cfg` under `src/jw/` properly, based on `settings.cfg.sample`


### Start services

```bash
$ ve scheduler-start your/other/folder/settings.cfg
$ ve rpc-start --help # more info
```

### Run as a command
```bash
$ ve scheduler-start src/jw/settings.cfg -x
```

### Example of configuration
```
[JIRA_MISS_TIME]

jira_url = http://jira.juwai.com

login_name = IamCaesar

login_password = MyPassword

filter = project in ("Consumer Products", "Industry Products", "Platform Products", XML, Salesforce, LOC) AND status in (Closed, Done, "PM Testing", Testing) AND type not in (Epic, subTaskIssueTypes()) AND (timespent is EMPTY OR timespent = 0) AND fixVersion is EMPTY AND updated >= 2017-11-01 ORDER BY Status DESC, updated DESC

notice_for_assignee = [SYSTEM NOTICE] Log time, please !

notice_for_reporter = [SYSTEM NOTICE] The issue has not been assigned !

```

you can find this configuration in folder (python2.7/site-packages/jira_scheduler-0.0.1.dev0-py2.7.egg/jw/settings.cfg) 
