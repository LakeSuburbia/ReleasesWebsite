from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


# Create your models here.
class User(AbstractUser):
    pass


class Release(models.Model):
    release_date = models.DateField()
    title = CharField(max_length=100)
    artist = CharField(max_length=100)

    def __str__(self):
        return self.title


class ReleaseScore(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    release = models.ForeignKey('Release', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])


class ReleasePublicScore:
    release = models.ForeignKey('Release', on_delete=models.CASCADE)
    score = models.ForeignKey('ReleaseScore', on_delete=models.CASCADE)
    # globalaveragescore = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    # globalhottestscore = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
