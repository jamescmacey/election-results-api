from django.shortcuts import render
from django.conf import settings
from django.views import View
from election_results.utils import get_db_handle
from django.http import HttpResponseServerError, JsonResponse
from election_results import TAURANGA_MONGO_CLIENT as MONGO_CLIENT

# Create your views here.
def statics(request):
    response = {
        "candidates": [],
        "electorates": [],
        "parties": [],
        "voting_places": [],
        "statistics": None,
        "config": settings.TAURANGA_ELECTION_CONFIG
    }

    db = MONGO_CLIENT

    try:
        response["candidates"] = list(db.candidates.find({}))
        response["electorates"] = list(db.electorates.find({}))
        response["parties"] = list(db.parties.find({}))
        response["statistics"] = list(db.statistics.find({}))[0]
        response["voting_places"] = list(db.voting_places.find({}))
    except:
        raise HttpResponseServerError

    return JsonResponse(response)

def isalive(request):
    db = MONGO_CLIENT

    try:
        _ = list(db.election.find({}))[0]
        response = {"is_alive": True}
    except:
        response = {"is_alive": False}

    return JsonResponse(response)

def results(request):
    response = {
        "election": None,
        "results": []
    }

    db = MONGO_CLIENT

    try:
        response["election"] = list(db.election.find({}))[0]
        response["results"] = list(db.electorate_results.find({}))

    except:
        raise HttpResponseServerError

    return JsonResponse(response)