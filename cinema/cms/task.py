from cinema.celery import app
from django.core.mail import send_mail


@app.task(bind=True)
def send_mailing(self, list_users, template):
    for i in range(len(list_users)):
        send_mail('Email Kino',
                  'Kino',
                  None,
                  [list_users[i]],
                  fail_silently=False,
                  html_message=template)
        self.update_state(state='PROGRESS',
                          meta={'current': i + 1, 'total': len(list_users)})
    print('Task completed')
    return {'current': 100, 'total': 100}
