from django.contrib import admin
from .models import *

class PositionInline(admin.TabularInline):
    model = Position
    extra = 0

class VoteAdmin(admin.ModelAdmin):

    inlines = [PositionInline]
    class Meta:
        model = Vote

admin.site.register(Vote,VoteAdmin)
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(CandidateQueue)
admin.site.register(Collected_vote)
