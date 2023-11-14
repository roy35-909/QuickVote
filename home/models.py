from django.db import models
from authentication.models import User


class Vote(models.Model):


    name  = models.CharField(max_length=300)
    start = models.DateField()
    status = models.CharField(max_length=100,default="Pending")

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE,null=True,blank=True)
    win = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    win_by = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=300)
    
    def __str__(self) -> str:
        return self.name
    

class CandidateQueue(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)

    is_valid = models.BooleanField(default=False)

class Candidate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    number_of_vote = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.user.first_name
    
class Collected_vote(models.Model):

    vote = models.ForeignKey(Vote,on_delete=models.CASCADE)
    position = models.ForeignKey(Position,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
