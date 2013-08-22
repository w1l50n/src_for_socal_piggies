from celery import task
import logging
import random

from django.core.exceptions import ObjectDoesNotExist
from rapidsms.router import send, lookup_connections
from sms_raffle.models import RaffleEntry, RafflePrize, RaffleWinner


logger = logging.getLogger(__name__)


@task
def choose_winners():
    raffle_winners = RaffleWinner.objects.count()
    if raffle_winners > 0:
        return
    else:
        raffle_entries = RaffleEntry.objects.all()
        raffle_prizes = RafflePrize.objects.all()

        raffle_entry_indexes = range(raffle_entries.count())
        random.shuffle(raffle_entry_indexes)

        prize = raffle_prizes.get(prize='rpi')
        rpi_winner = raffle_entries[raffle_entry_indexes[0]]
        RaffleWinner.objects.create(winner=rpi_winner, prize=prize)

        prize = raffle_prizes.get(prize='tshirt')
        k = min(prize.quantity, len(raffle_entry_indexes[1:]))
        tshirt_winner_indexes = random.sample(raffle_entry_indexes[1:], k)
        for index in tshirt_winner_indexes:
            RaffleWinner.objects.create(winner=raffle_entries[index], prize=prize)

    notify_winners()


@task
def rechoose_rpi():
    raffle_winners = RaffleWinner.objects.all()
    try:
        raffle_winners.get(prize__prize='rpi').delete()
    except ObjectDoesNotExist:
        pass
    except Exception as ex:
        logger.warn(ex)
        return

    phone_numbers = [data[0] for data in raffle_winners.values_list('winner__phone_number')]
    raffle_entries = RaffleEntry.objects.exclude(phone_number__in=phone_numbers)
    raffle_prizes = RafflePrize.objects.get(prize='rpi')

    raffle_entry_indexes = range(raffle_entries.count())
    random.shuffle(raffle_entry_indexes)

    rpi_winner = raffle_entries[raffle_entry_indexes[0]]
    RaffleWinner.objects.create(winner=rpi_winner, prize=raffle_prizes)

    notify_winners(prize='rpi')


@task
def reset_winner():
    raffle_winners = RaffleWinner.objects.all().delete()


@task
def notify_winners(prize=None):
    if prize:
        raffle_winners = RaffleWinner.objects.select_related().filter(prize__prize=prize)
    else:
        raffle_winners = RaffleWinner.objects.select_related().all()
    for winner in raffle_winners:
        try:
            connections = lookup_connections(backend="kannel-gsm-modem",
                                             identities=[winner.winner.phone_number])
            text = "You have won a {0}".format(winner.prize.get_prize_display())
            logger.info((text, winner.winner.phone_number))
            #send(text, connections=connections)
        except Exception as ex:
            logger.warn(ex)

