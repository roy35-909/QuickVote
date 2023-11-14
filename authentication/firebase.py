import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("./cred.json")
firebase_admin.initialize_app(cred)

db = firestore.client()




# doc = doc_ref.get()

# if doc.exists:
#     extected_id = doc.to_dict()['expected_id']
#     print(extected_id)
# else:
#     print("No such Document!")



# doc_ref.set({"expected_id":4},merge = True)

# print(doc_ref)


def make_register_sent(fid):
    try:
        doc_ref = db.collection('Register').document('register')
        doc_ref.set({"id":fid,"status":"Sent"},merge = True)
        return True
    
    except:
        print("Something worng when send data from firebase.py")
        return False
    

def make_register_done():
    try:
        doc_ref = db.collection('Register').document('register')
        doc_ref.set({"status":"Done"},merge = True)
        return True
    
    except:
        print("Something worng when send data from firebase.py")
        return False
    

def change_register_status(status):
    try:
        doc_ref = db.collection('Register').document('register')
        doc_ref.set({"fingerprint_status" : status},merge = True)
        return True
    
    except:
        print("Something worng when send data from firebase.py")
        return False
    


def change_login_status(status):

    try:
        doc_ref = db.collection('Login').document('login')
        doc_ref.set({"status" : status},merge = True)
        return True
    
    except:
        print("Something worng when send data from firebase.py")
        return False


def change_login_sensor_id(status):

    try:
        doc_ref = db.collection('Login').document('login')
        doc_ref.set({"sensor_id" : status},merge = True)
        return True
    
    except:
        print("Something worng when send data from firebase.py")
        return False
