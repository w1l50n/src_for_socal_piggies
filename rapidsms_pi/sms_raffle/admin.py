from django.contrib import admin

from sms_raffle.models import RaffleEntry, RafflePrize, RaffleWinner

class RafflePrizeAdmin(admin.ModelAdmin):
    list_display = ('prize', 'quantity')

admin.site.register(RafflePrize, RafflePrizeAdmin)
