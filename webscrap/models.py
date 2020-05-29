
from django.db import models


# Create your models here.
class Coronacases(models.Model):
    Index = models.CharField(max_length=128)
    Country_Name = models.CharField(max_length=128)
    Total_Cases = models.CharField(max_length=128)
    New_Cases = models.CharField(max_length=128)
    Deaths_Per_Country = models.CharField(max_length=128)
    New_Death = models.CharField(max_length=128)
    Total_Recovered = models.CharField(max_length=128)
    Active_Cases = models.CharField(max_length=128)
    Serious_and_Critical = models.CharField(max_length=128)
    Cases_Per_Million = models.CharField(max_length=128)
    Death_Per_Millions = models.CharField(max_length=128)
    Total_Tests = models.CharField(max_length=128)
    Tests_Per_Millions = models.CharField(max_length=128)
    Total_Population = models.CharField(max_length=128)

    # Total_Cases = models.CharField(max_length=128)
    # Death = models.CharField(max_length=128)
    # Total_Recovered = models.CharField(max_length=128)
    # Currently_Infected = models.CharField(max_length=128)
    # Mild_Condition = models.CharField(max_length=128)
    # Serious_Condition = models.CharField(max_length=128)
    # Case_With_Outcome = models.CharField(max_length=128)
    # Recovered = models.CharField(max_length=128)
    # Total_Deaths = models.CharField(max_length=128)

    def __str__(self):

        return "%s - %s" % (self.Country_Name, self.Index)



