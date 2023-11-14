from django.shortcuts import render,redirect
from home.models import *
from django.db.models import Q 

def dashboard(request):
    if request.user.is_superuser:
        vote = Vote.objects.filter(Q(status= "Pending") | Q(status="Voating"))
        vote_done = Vote.objects.filter(status = "Done")
        candidate_request = CandidateQueue.objects.filter(is_valid = False)
        position = Position.objects.all()
        user = User.objects.filter(is_superuser = False)
        return render(request,'dashboard.html',{"user":user,"vote":vote,"vote_done":vote_done,"position":position,"candidate":candidate_request})
    else:
        return redirect('/')


def candidate(request):

    if request.user.is_superuser:

        candidate = CandidateQueue.objects.all()
        return render(request,'dashboard-candidate.html',{"candidate":candidate})
    

def dashboard_vote(request):

    if request.user.is_superuser:

        vote = Vote.objects.filter(Q(status= "Pending") | Q(status="Voting"))

        return render(request,'dashboard_vote.html',{"vote":vote})

def make_start_vote(request,pk):

    if request.user.is_superuser:

        vote = Vote.objects.get(id=pk)
        vote.status="Voting"
        vote.save()
        return redirect('/dashboard/vote')
    

def make_vote_done(request,pk):

    if request.user.is_superuser:

        vote = Vote.objects.get(id=pk)
        vote.status = "Done"
        vote.save()

        position = Position.objects.filter(vote = vote)
        for i in position:
            try:
                win = Candidate.objects.filter(position = i).order_by('-number_of_vote').first()
                if win is None:
                    continue
                i.win = win.user
                i.save()
            except:
                continue

                
            
        return redirect('/dashboard/vote')
    
def make_vote_delete(request,pk):

    if request.user.is_superuser:
        vote = Vote.objects.get(id=pk)
        vote.delete()
        return redirect('/dashboard/vote')
    
def make_candidate_delete(request,pk):

    if request.user.is_superuser:
        candidate = CandidateQueue.objects.get(id=pk)
        candidate.delete()
        return redirect('/dashboard/candidate')

def make_candidate_accept(request,pk):

    if request.user.is_superuser:
        candidate = CandidateQueue.objects.get(id=pk)
        accept = Candidate.objects.create(user = candidate.user,vote=candidate.vote,position = candidate.position)
        accept.save()
        candidate.delete()
        return redirect('/dashboard/vote')
    


def show_result(request):

    if request.user.is_superuser:

        votes = Vote.objects.filter(status="Done")

        return render(request,'show_result.html',{"votes":votes})
    
    else:
        return redirect('/')