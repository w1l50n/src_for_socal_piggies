from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from djappsettings import settings

from sms_raffle.models import RaffleWinner
from sms_raffle.tasks import (choose_winners as choose_winners_task,
                                rechoose_rpi as rechoose_rpi_task,
                                reset_winner as reset_winner_task)


def show_winners(request):
    raffle_winners = RaffleWinner.objects.select_related().order_by('prize__prize')

    data = {
        'raffle_winners' : raffle_winners,
    }

    return render_to_response(
            "show_winners.html",
            data,
            context_instance=RequestContext(request))


def choose_winners(request):
    choose_winners_task.delay()
    return HttpResponse("Accepted", content_type="text/plain", status=202)
    

def rechoose_rpi(request):
    rechoose_rpi_task.delay()
    return HttpResponse("Accepted", content_type="text/plain", status=202)


def reset_winner(reset_winner):
    reset_winner_task.delay()
    return HttpResponse("Accepted", content_type="text/plain", status=202)    