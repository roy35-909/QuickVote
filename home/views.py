from django.shortcuts import render,redirect
from .models import *
from authentication.models import User
from django.db.models import Q 
def home(request):


    if request.method == 'GET':
        objj = Vote.objects.filter(Q(status= "Pending") | Q(status="Voting"))
        if request.user.is_authenticated:
            return render(request,'home.html',{"current_vote":objj,"user":request.user})
        else:
            return redirect('/auth/login')


def select_vote(request,pk):


    if request.method == 'GET':
        if request.user.is_authenticated:
            objj = Vote.objects.get(id=pk)
            return render(request,'vote.html',{"current_vote":objj,"user":request.user})
        else:
            return redirect('/auth/login')
        


def make_vote(request,pk):

    if request.user.is_authenticated:

        objj = Position.objects.get(id=pk)

        return render(request,'make_vote.html',{"position":objj,"user":request.user})
    
    else:
        return redirect('/auth/login')
    

def give_vote(request,pk):

    if request.user.is_authenticated:

        candidate = Candidate.objects.get(id=pk)
        if Collected_vote.objects.filter(vote = candidate.vote,position = candidate.position,candidate=candidate,user = request.user).exists():
            return redirect('/vote/'+str(candidate.vote.id))
        candidate.number_of_vote+=1
        candidate.save()

        vote = Collected_vote.objects.create(vote = candidate.vote,position = candidate.position,candidate=candidate,user=request.user)
        vote.save()

        return redirect('/vote/'+str(candidate.vote.id))
    

def become_candidate(request,pk):

    if request.user.is_authenticated:
        position = Position.objects.get(id=pk)
        candidate = CandidateQueue.objects.create(user = request.user,vote = position.vote, position = position)
        candidate.save()
        return redirect('/vote/'+str(position.vote.id))