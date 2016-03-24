from django.db import models


class Execution(models.Model):
    objects = models.Manager()

    def __init__(self, id, app_name, exec_name, submit_date, sched_date, fin_date, status):
        self.id = id
        self.app_name = app_name
        self.exec_name = exec_name
        self.submit_date = submit_date
        self.sched_date = sched_date
        self.fin_date = fin_date
        self.status = status
