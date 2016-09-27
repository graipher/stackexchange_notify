import stackexchange
import time
import datetime


def pync_notify(question):
    from pync import Notifier
    Notifier.notify('Votes: {0.score} | Answers: {1} | Views: {0.view_count}'.format(
        question, len(question.answers)),
        title='CodeReview: {.title}'.format(question),
        subtitle='Tags: {}'.format(', '.join(question.tags)),
        sound='default', open=question.url)


def gtk_notify(question):
    from gi.repository import Notify
    from pprint import pprint
    Notify.init('stackexchange')
    pprint(vars(question))
    notification = Notify.Notification.new(
        '{.title}'.format(question),
        'Tags: {0}\nVotes: {1.score} | Answers: {2} | Views: {1.view_count}'.format(
            ', '.join(question.tags), question, len(question.answers)),
        '/home/andreas/Bilder/codereview.png')
    notification.show()


def get_questions2(tags={'python'}):
    """Fetch recent questions from CodeReview

    This function uses the SE API and yield each
    new question that is asked on CR.
    """

    cr = stackexchange.Site(stackexchange.CodeReview)

    old = set()
    while True:
        questions = cr.recent_questions(tagged='python', filter='_b')
        for question in questions[:3]:
            if question.title not in old and len(set(question.tags) | tags):
                old.add(question.title)
                yield question
                time.sleep(10)
        time.sleep(30)


def now():
    """Return the current timestamp"""
    return int(time.time())


def get_questions(site=stackexchange.CodeReview, query_delay=2):
    """Fetch recent questions from the Stack Exchange network

    This function uses the SE API and yield each
    new question that is asked on the given site.
    """

    se = stackexchange.Site(stackexchange.CodeReview)
    last_query = now()

    while True:
        fromdate, last_query = last_query, now()
        questions = se.questions(
            fromdate=fromdate, sort='creation', tagged='python')
        for question in questions:
            yield question
        time.sleep(query_delay)


if __name__ == '__main__':
    for question in get_questions(query_delay=30):
        gtk_notify(question)
