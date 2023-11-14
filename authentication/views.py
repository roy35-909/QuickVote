from django.shortcuts import render,HttpResponse,redirect
from rest_framework.response import Response
from .models import User

from rest_framework.views import APIView
from .firebase import make_register_sent,make_register_done,change_login_status
is_sensor_connected = True
try:
    from .main import enroll_finger,get_fingerprint_detail

except:
    is_sensor_connected = False
from django.contrib.auth.models import auth
def get_fid():

    for i in range(1,127):

        try:
            user = User.objects.get(f_id = i)
            
        except:
            return i
        

class finger_register(APIView):
    def get(self,request,fid):
        if is_sensor_connected:
            pass
        else:
            return Response({"msg":"FingerPrint Sensor Not Connected ."})
        if enroll_finger(fid):
            return Response({"msg":"Enrolled Finger Successfully"})
        else:
            return Response({"msg" : "Some Error ......"})


def registration(request):

    if request.method == 'GET':
        fid = get_fid()
        if is_sensor_connected:
            make_register_sent(fid)
            
        
        return render(request,'register.html',context={"fid": fid})
    
    elif request.method == 'POST':
        if is_sensor_connected:
            pass
        else:
            return redirect('/')
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        nid = data['nid']
        phone = data['phone']
        alternative_password = data['password']
        fid = data['fid']
        user = User.objects.create(first_name=first_name,last_name=last_name,email = email,nid = nid, phone = phone)

        user.set_password("1234@asdf")
        if alternative_password != None:
            user.alternative_password = alternative_password
        user.f_id = int(fid)
        user.save()
        make_register_done()
        return redirect('/auth/registration')
    

class finger_login(APIView):
    def get(self,request,email):
        if is_sensor_connected:
            pass
        else:
            return Response({"msg":"FingerPrint Sensor Not Connected !"})
        print(email)
        try:
            user = User.objects.get(email=email)

        except:
            return Response({"msg":"Object Not Found"})
        
        for i in range(1,10):

            x,y = get_fingerprint_detail()


            if x:
                break

        if x ==True:
            if user.f_id == int(y):
                return Response({"msg" : "FingerPrint Matched !"})

            else:
                return Response({"msg": "Finger Print Don't match !"})
        else:
            return Response({"msg":"Try Again Please ."})

def login(request):


    if request.method == 'GET':
        # for i in range(1,10):
        #   if get_fingerprint_detail():
        #       break
        change_login_status("Click Scan Button..")
        return render(request,'login.html')
    

    if request.method == 'POST':

        data = request.POST
        print(data['status'])
        if data['status'] == 'FingerPrint Matched!':

            email = data['email']
            user = auth.authenticate(email=email,password = '1234@asdf')

            if user is not None:
                auth.login(request,user)

            return redirect('/')
        else:
            email = data['email']
            userr = User.objects.get(email = email)
            if userr.alternative_password == data['status']:
                user = auth.authenticate(email=email,password = '1234@asdf')
                auth.login(request,user)
                return redirect('/')
                

            return redirect('/')
            
        

def logout(request):


    auth.logout(request)
    return redirect('/auth/login')