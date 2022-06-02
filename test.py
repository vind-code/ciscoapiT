import requests
import json
import os
from requests.auth import HTTPBasicAuth
import urllib3

username = 'student'
pawd = 'Cisco123'

def init_auth(base_url):
    '''
    Base Auth and return device token
    '''
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
    try:
        resp = requests.post(url = base_url + 'tokenservices', headers = headers, auth=HTTPBasicAuth(username, pawd), verify=False)
        return resp.headers['X-Auth-Token']
    except(ConnectionError): # Not good
        print('Failed to connect and authenticate to device. Check reachability, DNS, and/or username and password.\n')
        raise SystemExit

def close_auth(base_url,xToken):
    '''
    Destroy Token, return 0 if unsuccessful
    '''
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
    try:
        resp = requests.delete(url = base_url + 'tokenservices/' + xToken, headers = headers, auth=HTTPBasicAuth(username, pawd), verify=False)
        return resp
    except(ConnectionError): # Not good
        print('Failed to destroy token.\n')
        raise SystemExit

def get_int_counts(base_url,int_name,xToken):
    '''
    Get interface monitoring info
    '''
    headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent', 'X-Auth-Token': xToken}
    try:
        resp = requests.get(url = base_url + 'monitoring/device/interfaces/' + int_name, headers = headers, verify=False)
        return resp.content
    except(ConnectionError): # Not good
        print('Failed to destroy token.\n')
        raise SystemExit

def main():
 

    base_url='https://192.168.0.229/api/'


    urllib3.disable_warnings()


    Auth_Token = init_auth(base_url)
    ### print(Auth_Token)
    mon_data = get_int_counts(base_url,'inside',Auth_Token)
    mon_dict = json.loads(mon_data)
    print(mon_dict['inputByteCount'])
    print(mon_dict['outputByteCount'])
    close_auth(base_url,Auth_Token)

if __name__ == '__main__':
    main()
