from scapy.all import *
from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import socket
from main import send_packet_data


def get_host_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

host_ip = get_host_ip_address()

def send_dns_request(server_ip, domain_name , recursive):
    # Create a DNS request packet
  
    dns_request = IP(dst=server_ip)/UDP()/DNS(rd=recursive, qd=DNSQR(qname=domain_name))
    # Send the packet and receive the response
    response = sr1(dns_request, verbose=0)

    return response


def build_request(host_ip,domain_name,query_type,server_ip, timestamp):
    request = {"host_ip": host_ip,"domain_name": domain_name,"query_type" : query_type,"server_ip": 
    server_ip,"time_stamp": timestamp}
    return request
def build_response(response):
    # Extract the desired data from the DNS response
    res_code = response[DNS].rcode  # Response code
    ttl = response[DNS].an.ttl     # TTL (Time to Live)
    resolved_ip = response[DNS].an.rdata   # Resolved IP address
    timestamp = datetime.now(pytz.timezone('Asia/Jerusalem')).strftime("%d:%m:%Y:%Z")  # Current timestamp
    resp = {"res_code" : res_code , "TTL" : ttl , "resolved_ip" : resolved_ip , "time_stamp" : timestamp}
    return resp

# Example usage
server_ip = "8.8.8.8"  # DNS server IP (e.g., Google DNS)
domain_name = "example.com"

send_packet_data(host_ip , domain_name , 1 , 'request' , build_request(host_ip,domain_name,'reuquest',server_ip,"123:12c"))
send_packet_data(host_ip , domain_name , 1 , 'response' , build_response(send_dns_request(server_ip,domain_name,1)))

#structure of the tuple for request:

#(token_id,host_ip,domain,query_type,server_ip , time_stamp)

#for response:

#(token_id,host_ip, res_code , TTL , resolved_ip, time_stamp)

# Print the response

