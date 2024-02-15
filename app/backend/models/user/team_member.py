#from django.db import models
#from django.db.utils import IntegrityError
#from .user import User
#from .team import Team

#class TeamMember(models.Model):
#    team_member_id = models.BigAutoField(primary_key=True)
#    username = models.ForeignKey(User, on_delete=models.CASCADE)
#    team_name = models.ForeignKey(Team, on_delete=models.CASCADE)

#    class Meta:
#        constraints = [
#        models.UniqueConstraint(fields=["username", "team_name"], name="prevent multiple memberships of one person in one team constraint")
#        ]
#        verbose_name = "Teammitglied"
#        verbose_name_plural = "Teammitglieder"

#    def __str__(self):
#        return str(self.team_name) + " " + str(self.username)

    # overwrite save methods with caution!
    # this is meant to prevent db crash if one person is added to the same team more than once from addtestdata.py
    # this may occur, when addtestdata.py is run multiple times for development/testing reasons
    # for now, only unique fields are problematic since primary key duplicates just wont be inserted (as expected) without crashing the db
    # exception handling in the admin panel is not affected
#    def save(self, *args, **kwargs):
#        try:
#            super(TeamMember, self).save(*args, **kwargs)
#        except IntegrityError:
#            print("Person ist bereits in diesem Team")
#            pass
