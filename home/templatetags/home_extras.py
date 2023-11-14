from django import template
from home.models import *
register = template.Library()

def is_voted(value,arg):


    if Collected_vote.objects.filter(position=value,user=arg).exists():
        return True

    return False


def is_possible_to_be_candidate(value,arg):


    if CandidateQueue.objects.filter(vote=value.vote,user=arg).exists():
        return False
    if value.vote.status != "Pending":
        return False
    if Candidate.objects.filter(vote=value.vote,user=arg).exists():
        return False
    return True


def is_vote_start_or_not(value,arg):


    if value.status == "Voting":
        return True

    return False

def which_one_is_win(value):

    win = Position.objects.get(id = value.position.id)
    if value.user == win.win:
        return True
    else:
        return False


register.filter('is_voted',is_voted)
register.filter('which_one_is_win',which_one_is_win)
register.filter('is_vote_start_or_not',is_vote_start_or_not)
register.filter('is_possible_to_be_candidate',is_possible_to_be_candidate)