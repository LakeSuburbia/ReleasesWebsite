from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.db import IntegrityError
from .models import *


# Create your views here.
def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "releases/index.html", {
                "firstname": request.user.first_name,
                "lastname": request.user.last_name,
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
            return render(request, "releases/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "releases/register.html", {
                "message": "Email address or username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "releases/register.html")


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
            return render(request, "releases/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "releases/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def addRelease(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            releasedate = request.POST["releasedate"]
            artist = request.POST["artist"]

            # TODO Add format control.

            # Attempt to create new user
            try:
                user = Release.objects.create(artist = artist, title = title, releasedate = releasedate)
                user.save()

            # TODO Add check doubles
            #except IntegrityError as e:
            #    print(e)
            #    return render(request, "releases/register.html", {
            #        "message": "Release is already added."
            #    })
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "releases/index.html")
