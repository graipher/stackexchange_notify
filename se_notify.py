# @Author: Andreas Weiden <andreas.weiden@gmail.com>
# @Date:   2016-09-27 15:32:31
# @Last modified by:   andreas
# @Last modified time: 2016-09-27 16:43:01


import stackexchange
import time
import argparse


def pync_notify(question, icon):
    from pync import Notifier
    Notifier.notify('Votes: {0.score} | Answers: {1} | Views: {0.view_count}'.format(
        question, len(question.answers)),
        title='CodeReview: {.title}'.format(question),
        subtitle='Tags: {}'.format(', '.join(question.tags)),
        sound='default', open=question.url)


def gtk_notify(question, icon):
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    if not icon:
        icon = 'dialog-information'
    Notify.init('stackexchange')
    notification = Notify.Notification.new(
        '{.title}'.format(question),
        'Tags: {0}\nVotes: {1.score} | Answers: {2} | Views: {1.view_count}'.format(
            ', '.join(question.tags), question, len(question.answers)),
        icon)
    notification.show()


def now():
    """Return the current timestamp"""
    return int(time.time())


def get_questions(site, query_delay, tag):
    """Fetch recent questions from the Stack Exchange network

    This function uses the SE API and yield each
    new question that is asked on the given site.
    """

    se = stackexchange.Site(site, 'ynrQ))36pm7Pyx92S4eK2A((')
    last_query = now() - 10000
    kwargs = {}
    if tag is not None:
        kwargs['tagged'] = tag

    while True:
        fromdate, last_query = last_query, now()

        questions = se.questions(
            fromdate=fromdate, sort='creation', **kwargs)
        for question in questions:
            yield question
        time.sleep(query_delay)


def main():
    notifiers = {"GTK": gtk_notify, "pync": pync_notify}
    sites = [s for s in dir(stackexchange.sites) if not s.startswith('__')]
    icons = {"CodeReview": "icons/codereview.png"}

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
    args = parser.parse_args()

    notifier = notifiers[args.notifier]
    if not args.icon and args.site in icons:
        args.icon = icons[args.site]
    for question in get_questions(args.site, args.delay, args.tag):
        notifier(question, args.icon)

if __name__ == '__main__':
    main()
