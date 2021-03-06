from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import CharField


# Create your models here.
class User(AbstractUser):
    pass


class Release(models.Model):
    release_date = models.DateField()
    title = CharField(max_length=100)
    artist = CharField(max_length=100)
    averagescore = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=-1)
    hottestvalue = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)], default=-1)

    def __str__(self):
        return self.title


class ReleaseScore(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    release = models.ForeignKey('Release', on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])

