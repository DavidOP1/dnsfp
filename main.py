import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
cred_obj = firebase_admin.credentials.Certificate("ServiceAccountKey.json")
default_app = firebase_admin.initialize_app(cred_obj)
db= firestore.client()

#Build host profile

def send_packet_data(host_ip,domain,index,request_type,data):
    packet_data_json = json.dumps(packet_data)
    ref = db.collection('active-hosts').document(host_ip).collection('queried-domain').document(domain).collection('query1').document(request_type)
    ref.set(data)
