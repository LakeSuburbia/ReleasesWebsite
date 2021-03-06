from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets, permissions
from django.db.models import Sum, Avg
from .serializers import ReleaseSerializer, ScoreSerializer
from rest_framework.decorators import api_view
from django.urls import reverse
from django.db import IntegrityError
from .models import *
import requests


# views API
class ScoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ReleaseScore.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReleaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows releases to be viewed or edited.
    """
    queryset = Release.objects.all().order_by('release_date')
    serializer_class = ReleaseSerializer


def index(request):
    calculateAverageScoreOfSet()
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        releases = Release.objects.all()
        return render(request, "releasesplatform/index.html", {
            "username": request.user.username,
            "firstname": request.user.first_name,
            "lastname": request.user.last_name,
            "releases": releases
        })

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        
        email = request.POST["email"]
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "releasesplatform/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "releasesplatform/register.html", {
                "message": "Email address or username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
       
    else:
        return render(request, "releasesplatform/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "releasesplatform/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "releasesplatform/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def add_release(request):
    if request.method == "POST":
        
        releasedate=request.POST["release_date"]
        artist=request.POST["artist"]
        title=request.POST["title"]

        occurance = Release.objects.filter(release_date=releasedate, artist=artist).count()
        occurance += Release.objects.filter(artist=artist, title=title).count() 
        occurance += Release.objects.filter(title=title, release_date=releasedate).count()

        if occurance > 0:
            return render(request, "releasesplatform/add_release.html", ({
                "message": "This release exists already"
            }))

        data = {
            "release_date": releasedate,
            "artist": artist,
            "title": title
        }
        

        requests.post('http://127.0.0.1:8000/restapi/releasesplatform/', data, auth=('ADMIN', 'ADMIN'))
        return HttpResponseRedirect(reverse("releases"))
    else:
        return render(request, "releasesplatform/add_release.html")


def release_view(request, releaseid):
    if request.user.is_authenticated:
        release = Release.objects.get(id=releaseid)

        if request.method == "POST":
            vote(request, releaseid)

        elif not release:
            return render(request, "releasesplatform/releases.html")

        return render_release(request, release)

        

def edit_release(request, releaseid):
    release = Release.objects.get(id=releaseid)
    if request.method == "POST":
        release.release_date = request.POST["release_date"]
        release.artist = request.POST["artist"]
        release.title = request.POST["title"]
        release.save()

        return HttpResponseRedirect(reverse("releases"))
    else:
        return render(request, "releasesplatform/edit_release.html", {
            "id": releaseid,
            "title": release.title,
            "artist": release.artist,
            "release_date": release.release_date
        })


def vote(request, releaseid):
    release = Release.objects.get(id=releaseid)
    user = request.user
    score = request.POST["score"]
    releasescore = ReleaseScore.objects.filter(user=user).filter(release=release)

    if (releasescore):
        vote = ReleaseScore.objects.filter(user=user).get(release=release)
        vote.score = score
        vote.save()
    else:
        vote = ReleaseScore.objects.create(user=user, release=release, score=score)
        vote.save()



def calculateAverageScoreOfSet():
    releases = Release.objects.all()
    for release in releases:
        calculateAverageScore(release)
    
def calculateAverageScore(release):
    totaalaantal = ReleaseScore.objects.filter(release=release).count()
    if totaalaantal > 0:
        release.averagescore = ReleaseScore.objects.filter(release=release).aggregate(Avg('score'))['score__avg']
        release.hottestvalue = totaalaantal
    else:
        release.averagescore = -1
        release.hottestvalue = -1
    release.save()


def getCurrentScore(user, release):
    if ReleaseScore.objects.filter(user = user).filter(release = release).exists():
        return ReleaseScore.objects.filter(user = user).get(release = release).score
    else:
        return ""

    

def delete_vote(request, releaseid):
    user = request.user
    release = Release.objects.get(id=releaseid)
    if ReleaseScore.objects.filter(user = user).filter(release = release).exists():
        ReleaseScore.objects.filter(user = user).get(release = release).delete()
    return render_release(request, release)


def render_release(request, release):
    calculateAverageScore(release)
    score = getCurrentScore(request.user, release)
    return render(request, "releasesplatform/release.html",{
                "id": release.id,
                "title": release.title,
                "artist": release.artist,
                "release_date": release.release_date,
                "score": score,
                "averagescore": release.averagescore
                })


def profile_view(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username__iexact=username)
        userscores = ReleaseScore.objects.filter(user__username__iexact=username)
        return render(request, "releasesplatform/profile.html",
                        {
                            "user": user,
                            "scores": userscores,
                            "ownAccount": request.user.username == username
                        })