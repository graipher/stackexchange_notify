def pync_notify(question, icon=None):
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
    Notify.init('stackexchange')
    notification = Notify.Notification.new(
        '{.title}'.format(question),
        'Tags: {0}\nVotes: {1.score} | Answers: {2} | Views: {1.view_count}'.format(
            ', '.join(question.tags), question, len(question.answers)),
        icon)
    notification.show()


def print_notify(question, icon=None):
    print """
    {0.title}
    Tags: {1}
    Votes: {0.score} | Answers: {2} | Views: {0.view_count}""".format(
        question, ', '.join(question.tags), len(question.answers))

notifiers = {"GTK": gtk_notify, "pync": pync_notify, "terminal": print_notify}
