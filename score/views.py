from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.


def home(request):
    match = Match.objects.first()
    context = {"match": match}
    return render(request, "home.html", context)


def update_score(request):
    match = Match.objects.first()
    context = {"match": match}
    if request.method == "POST":
        match_id = request.POST["match"]
        player_id = request.POST["player"]
        score = request.POST["score"]
        obj, created = Score.objects.get_or_create(match=match_id, player=player_id)
        obj.score = obj.score + int(score)
        obj.save()
        return redirect("update_score")
    return render(request, "update_score.html", context)
