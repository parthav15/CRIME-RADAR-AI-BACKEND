from django.db import models

class CrimeData(models.Model):
    state = models.CharField(max_length=100)
    year = models.IntegerField()
    
    murder = models.IntegerField()
    attempt_to_murder = models.IntegerField()
    culpable_homicide = models.IntegerField()
    rape = models.IntegerField()
    custodial_rape = models.IntegerField()
    other_rape = models.IntegerField()
    kidnapping_abduction = models.IntegerField()
    kidnapping_women_girls = models.IntegerField()
    kidnapping_others = models.IntegerField()
    dacoity = models.IntegerField()
    assembly_dacoity = models.IntegerField()
    robbery = models.IntegerField()
    burglary = models.IntegerField()
    theft = models.IntegerField()
    auto_theft = models.IntegerField()
    other_theft = models.IntegerField()
    riots = models.IntegerField()
    criminal_breach_of_trust = models.IntegerField()
    cheating = models.IntegerField()
    counterfeiting = models.IntegerField()
    arson = models.IntegerField()
    hurt_grievous_hurt = models.IntegerField()
    dowry_deaths = models.IntegerField()
    assault_women_modesty = models.IntegerField()
    insult_modesty_women = models.IntegerField()
    cruelty_by_husband = models.IntegerField()
    importation_girls = models.IntegerField()
    causing_death_negligence = models.IntegerField()
    other_ipc_crimes = models.IntegerField()
    total_ipc_crimes = models.IntegerField()

    def __str__(self):
        return f"{self.state} - {self.year}"