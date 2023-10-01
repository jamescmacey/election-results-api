from django.shortcuts import render
from django.conf import settings
from django.views import View
from django.http import HttpResponseServerError, JsonResponse, Http404, HttpResponse
from election_results import MONGO_CLIENT
from datetime import datetime
import zoneinfo
import json
from bson import ObjectId
import zlib
import base64

# Create your views here.

def index(request):
    db = MONGO_CLIENT
    now = datetime.now(zoneinfo.ZoneInfo("Pacific/Auckland")).timestamp()
    MINUTES = 60
    threshold = now - (60 * MINUTES)
    heartbeats = list(db.heartbeat.find({"datetime_timestamp": {"$gt": threshold}}))
    context = {}
    for heartbeat in heartbeats:
        if heartbeat.get("worker_id") not in context.keys():
            context[heartbeat.get("worker_id")] = heartbeat
        if heartbeat.get("datetime_timestamp") > context[heartbeat.get("worker_id")].get("datetime_timestamp"):
            context[heartbeat.get("worker_id")] = heartbeat

        context[heartbeat.get("worker_id")]["datetime"] = context[heartbeat.get("worker_id")]["datetime"].replace(tzinfo=zoneinfo.ZoneInfo("UTC"))

    return render(request, "api/index.html", context = {"heartbeats": context.values()})

class EventList(View):
    def get(self, request, *args, **kwargs):
        db = MONGO_CLIENT
        try:
            response = list(db.events.find({"event_type": "actual"}))
        except:
            raise HttpResponseServerError
        return JsonResponse({"events":response})
    
class Event(View):
    def get(self, request, *args, **kwargs):
        db = MONGO_CLIENT
        event_id = self.kwargs['event_id']
        response = None
        try:
            response = db.events.find_one({"_id": event_id})
        except:
            raise HttpResponseServerError
        if not response:
            raise Http404
        return JsonResponse(response)
    
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

    
class ResultsList(View):
    def get(self, request, *args, **kwargs):
        db = MONGO_CLIENT
        event_id = self.kwargs['event_id']
        encoder = JSONEncoder()

        format = self.request.GET.get('format')
        if format not in ["json", "compressed"]:
            format = "compressed"

        newer_than = 0
        try:
            newer_than = float(self.request.GET.get('newer_than', 0))
        except ValueError:
            newer_than = 0

        try:
            response = list(db.results.find({"event_id": event_id, "updated_timestamp": {"$gt": newer_than}}))
            response = encoder.encode({"results":response})

            if format == "compressed":
                response = base64.b64encode(zlib.compress(bytes(response, "utf-8"))).decode("ascii")
                return JsonResponse({"compressed": response})
            elif format == "json":
                return HttpResponse(response, content_type="application/json")
        except:
            raise HttpResponseServerError
        