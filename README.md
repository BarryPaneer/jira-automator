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
$ ve scheduler-start ./your/other/folder/settings.cfg
$ ve rpc-start --help # more info
```

### Run as a command
```bash
$ ve scheduler-start src/jw/settings.cfg -x
```
