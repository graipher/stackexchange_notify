#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
# @Author: Andreas Weiden <andreas.weiden@gmail.com>
# @Date:   2016-09-27 15:32:31
# @Last modified by:   andreas
# @Last modified time: 2016-10-10 11:59:15


import stackexchange
import time
import argcomplete
import argparse
from notifiers import *


sites = [s for s in dir(stackexchange.sites) if not s.startswith('__')]

parser = argparse.ArgumentParser(description="StackExchange notifications")
parser.add_argument('-s', '--site', metavar="SITE", default='CodeReview', choices=sites,
                    help="Sub-site to watch (default: CodeReview)")
parser.add_argument('-t', '--tag', default=None,
                    help="Tag to use as filter (default: None)")
parser.add_argument('-d', '--delay', type=int, default=30,
                    help="Delay (in seconds) between subsequent requests (default: 30)")
parser.add_argument('-n', '--notifier', default="GTK",
                    choices=notifiers, help="Which notifier to use (default: GTK)")
parser.add_argument('-i', '--icon', default=None,
                    help="Icon (GTK only), either short name or absolute path")
parser.add_argument('--start-time', type=int, default=1000,
                    help="How far back to start displaying in seconds (default: 1000)")
parser.add_argument('--verbose', '-v', action='store_true',
                    help="Turn on printing of new questions")
argcomplete.autocomplete(parser)


def now():
    """Return the current timestamp"""
    return int(time.time())


def get_questions(site, query_delay, tag, start_time, max_questions=20):
    """Fetch recent questions from the Stack Exchange network

    This function uses the SE API and yield each
    new question that is asked on the given site.
    """

    se = stackexchange.Site(site, 'ynrQ))36pm7Pyx92S4eK2A((')
    last_query = now() - start_time
    kwargs = {}
    if tag is not None:
        kwargs['tagged'] = tag

    while True:
        fromdate, last_query = last_query, now()

        questions = se.questions(
            fromdate=fromdate, sort='creation', **kwargs)
        for question in questions[:max_questions]:
            yield question
        time.sleep(query_delay)


def get_icon(site):
    import os
    path = "{}/icons/{}.png".format(os.getcwd(), site.lower())
    if os.path.isfile(path):
        return path
    return "dialog-information"


def main():
    args = parser.parse_args()

    notifier = notifiers[args.notifier]
    if not args.icon:
        args.icon = get_icon(args.site)
    for question in get_questions(args.site, args.delay, args.tag, args.start_time):
        notifier(question, args.icon)
        if args.verbose:
            print_notify(question)

if __name__ == '__main__':
    main()
