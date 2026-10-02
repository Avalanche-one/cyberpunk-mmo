from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import generic

from cyberpunk_mmo.models import Faction


def index(request: HttpRequest) -> HttpResponse:
    num_players = get_user_model().objects.count()
    context = {
        "num_players": num_players
    }
    return render(request,"cyberpunk_mmo/index.html", context=context)


class FactionListView(generic.ListView):
    model = Faction
    paginate_by = 10
