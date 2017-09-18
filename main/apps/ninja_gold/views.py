from django.shortcuts import render, redirect
import random
from time import localtime, strftime
from datetime import datetime

# Create your views here.

def index(request):
    try:
        request.session["gold"]
    except KeyError:
        request.session["gold"] = 0
    if "logbook" not in request.session:
        request.session["logbook"] = []
    if "color" not in request.session:
        request.session["color"] = []
    return render(request, "ninja_gold/index.html")

def process_money(request, building_type):
    if request.method == "POST":
        earned_gold = 0
        color = "found"
        if building_type == "farm":
            earned_gold = random.randrange(10, 21)
        if building_type == "cave":
            earned_gold = random.randrange(5, 11)
        if building_type == "house":
            earned_gold = random.randrange(2, 6)
        if building_type == "casino":
            earned_gold = random.randrange(-50, 51)
            if earned_gold < 0:
                color = "lost"
        timestamp = datetime.now().strftime("%Y/%m/%d %-I:%M%p")
        logbook = {
            "class": color,
            "message": "You {} {} golds from the {} ({})".format(color, abs(earned_gold), building_type, timestamp)
        }
        try:
            logbook_list = request.session["logs"]
        except KeyError:
            logbook_list = []

        request.session["gold"] += earned_gold

        logbook_list.append(logbook)
        request.session["logs"] = logbook_list

    return redirect('/')

def reset(request):
    request.session["gold"] = 0
    request.session["logs"] = []
    return redirect ("/")