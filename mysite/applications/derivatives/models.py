from django.db import models

# Create your models here.
class EconomicIndicatorStandard(models.Model):
    date = models.DateField()
    dbcode = models.CharField(max_length=100)
    indicator = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    freq = models.CharField(max_length=10)
    value = models.FloatField(null=False, blank=False, default=None)
    update_date = models.DateField(null=True)
    flow = models.CharField(max_length=1)

    class Meta:
        unique_together = (("date", "dbcode", "freq"),)

    def __str__(self):
        return self.dbcode + '_' + self.indicator + '_' + self.country

class EconomicIndicatorCounterparty(models.Model):
    date = models.DateField()
    dbcode = models.CharField(max_length=100)
    indicator = models.CharField(max_length=200)
    country = models.CharField(max_length=20)
    counter_party = models.CharField(max_length=20)
    freq = models.CharField(max_length=10)
    value = models.FloatField(null=False, blank=False, default=None)
    update_date = models.DateField(null=True)

    class Meta:
        unique_together = (("date", "dbcode", "freq", "counter_party"),)
    def __str__(self):
        return self.dbcode + '_' + self.indicator + '_' + self.country
