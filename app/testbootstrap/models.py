from django.db import models


class Person(models.Model):
    surname = models.CharField(max_length=40)
    last_name = models.CharField(max_length=30)
    mail_adress = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Event(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    helper = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline


class EventDay(models.Model):
    pub_date = models.DateField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
