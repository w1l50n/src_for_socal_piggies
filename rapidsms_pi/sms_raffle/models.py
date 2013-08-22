from django.db import models

class RaffleEntry(models.Model):
    phone_number = models.CharField(max_length=16, unique=True, db_index=True)


class RafflePrize(models.Model):
    PRIZES = (
        ('rpi', 'Raspberry PI'),
        ('tshirt', 'T-Shirt'),
    )
    prize = models.CharField(max_length=16, choices=PRIZES)
    quantity = models.IntegerField()


class RaffleWinner(models.Model):
    
    winner = models.ForeignKey(RaffleEntry, unique=True)
    prize = models.ForeignKey(RafflePrize)
