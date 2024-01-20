from django.db import models

class EventType(models.TextChoices):
    CINEMA = "CI", ("Kino")
    CONCERT = "CO", _("Konzert")
    PLAY = "P", _("Theater")
    FESTIVAL = "F", _("Festival")
    OTHER = "O", _("Sonstiges")


class Event(models.Model):
    event_name = models.CharField(max_length=50, primary_key=true))
    event_type = models.CharField(
        max_length=2,
        choices=EventType.choices
        default=EventType.OTHER)
    event_description = models.TextField()
    #maybe use blob here instead
    event_press = models.TextField()
    event_fee = models.DecimalField(max_digits=4, decimal_places=2)
    #TODO: "requires pillow library"
    event_image = models.ImageField()

    class Meta:
        verbose_name = "Veranstaltung"
        verbose_name_plural = "Veranstaltungen"

    def __str__(self):
        return self.event_name

class EventDay(models.Model):
    event_day_id = models.BigAutoField(primary_key=true)
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.DateTimeField()
    duration = models.DurationField() #TODO: test how this works
    admission_time = models.DateTimeField()

    class Meta:
        verbose_name = "Veranstaltungstag"
        verbose_name_plural = "Veranstaltungstage"

    def __str__(self):
        return self.event_name + date

class Act(models.Model):
    act_name = models.CharField(max_length=40, primary_key=true)
    person_count = models.PositiveIntegerField()
    #TODO: "requires pillow library"
    act_image = models.ImageField()
    #TODO: test options
    music_sample = models.FileField()
    diet = models.CharField(max_length=100)
    act_email = models.EmailField, max_length=100)
    act_phone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Band"

    def __str__(self):
        return self.act_name

class EventAct(models.Model):
    event_act_id = models.BigAutoField(primary_key=true)
    event_day = models.ForeignKey(EventDay, on_delete=models.cascade)
    act_name = models.ForeignKey(Act, on_delete=models.cascade)

    class Meta:
        verbose_name = "Auftritt"
        verbose_name_plural = "Auftritte"

    def __str__(self):
        return self.event_name + act_name
