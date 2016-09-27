# stackexchange_notify

A small python script that watches a StackExchange sub-site (optionally filtered by one tag) for new posts and displays them.

Starts with showing the posts from the last ~15mins

Currently it supports GTK (with lib-notify) and MacOS (with pync).

```
usage: se_notify.py [-h] [-s SITE] [-t TAG] [-d DELAY] [-n {pync,GTK}]
                    [-i ICON]

StackExchange notifications


optional arguments:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  Sub-site to watch (default: CodeReview)
  -t TAG, --tag TAG     Tag to use as filter (default: None)
  -d DELAY, --delay DELAY
                        Delay (in seconds) between subsequent requests
                        (default: 30)
  -n {pync,GTK}, --notifier {pync,GTK}
                        Which notifier to use (default: GTK)
  -i ICON, --icon ICON  Icon (GTK only), either short name or absolute path
```

## Requirements

Uses the StackExchange API [Py-StackExchange](https://github.com/lucjon/Py-StackExchange)

```bash
easy_install Py-StackExchange
```

### Linux (GTK)

To allow displaying the notification

```bash
sudo apt install lib-notify lib-notify-dev
```

### Mac OS

To allow displaying the notification

```bash
pip install pync
```
