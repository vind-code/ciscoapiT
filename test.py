import requests
import json
import os
from requests.auth import HTTPBasicAuth
import urllib3

def init_auth(dic_dev):
    """
    Base Auth and return device token
    """
    url = 'https://{}/api/tokenservices'.format(dic_dev['ip'])
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
    try:
        resp = requests.post(url = url, headers = headers, auth = HTTPBasicAuth(dic_dev['username'], dic_dev['password']), verify = False)
        return resp.headers['X-Auth-Token']
    except(ConnectionError): # Not good
        print('Failed to connect and authenticate to device. Check reachability, DNS, and/or username and password.\n')
        raise SystemExit

def close_auth(dic_dev,xToken):
    """
    Destroy Token, return 0 if unsuccessful
    """
    url = 'https://{}/api/tokenservices/{}'.format(dic_dev['ip'], xToken)
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
    try:
        resp = requests.delete(url = url, headers = headers, auth=HTTPBasicAuth(dic_dev['username'], dic_dev['password']), verify = False)
        return resp
    except(ConnectionError): # Not good
        print('Failed to destroy token.\n')
        raise SystemExit

def get_int_counts(dic_dev,int_name,xToken):
    """
    Get interface monitoring info
    """
    url = 'https://{}/api/monitoring/device/interfaces/{}'.format(dic_dev['ip'], int_name)
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent', 'X-Auth-Token': xToken}
    try:
        resp = requests.get(url = url, headers = headers, verify = False)
        return resp.content
    except(ConnectionError): # Not good
        print('Failed to destroy token.\n')
        raise SystemExit

def main():
 
    urllib3.disable_warnings()
    my_dev = {'username': 'student', 'password': 'Cisco123', 'ip': '192.168.0.229'}

    Auth_Token = init_auth(my_dev)
    ### print(Auth_Token)
    mon_data = get_int_counts(my_dev,'inside',Auth_Token)
    mon_dict = json.loads(mon_data)
    print('Input Byte Count: ', mon_dict['inputByteCount'])
    print('Output Byte Count: ', mon_dict['outputByteCount'])
    close_auth(my_dev,Auth_Token)

if __name__ == '__main__':
    main()
