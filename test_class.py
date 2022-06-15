from pickle import NONE
import requests
import json
import os
from requests.auth import HTTPBasicAuth
import urllib3


class asa:

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.token = None
    

    def auth_open(self):
        """
        Base Auth and return device token
        """
        url = 'https://{}/api/tokenservices'.format(self.ip)
        headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
        try:
            resp = requests.post(url = url, headers = headers, auth = HTTPBasicAuth(self.username, self.password), verify = False)
            self.token = resp.headers['X-Auth-Token']
            return self.token
        except(ConnectionError): # Not good
            print('Failed to connect and authenticate to device. Check reachability, DNS, and/or username and password.\n')
            raise SystemExit
            

    def auth_close(self):
        """
        Destroy Token, return 0 if unsuccessful
        """
        url = 'https://{}/api/tokenservices/{}'.format(self.ip, self.token)
        headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent'}
        try:
            resp = requests.delete(url = url, headers = headers, auth=HTTPBasicAuth(self.username, self.password), verify = False)
            return resp
        except(ConnectionError): # Not good
            print('Failed to destroy auth token. Was it created by auth_open() function?\n')
            raise SystemExit 
        

    def _get_s(self, api_uri):
        """
        Universal GET function. api 'tale' must be supplied - /api/...
        Return response content as json-formatted data
        """
        url = 'https://{}{}'.format(self.ip, api_uri)
        headers = {'Content-type': 'application/json', 'User-Agent': 'REST API Agent', 'X-Auth-Token': self.token} 
        try:
            resp = requests.get(url = url, headers = headers, verify = False)
            return resp.content
        except(ConnectionError): # Not good
            print('Failed to GET from device.\n')
            raise SystemExit


    def get_int_info(self,int_name):
        """
        Get interface monitoring info. Correct interface name like 'inside' must be supplied
        Call _get_s() function, return interface info as json-formatted data
        """
        try:
            return self._get_s('/api/monitoring/device/interfaces/{}'.format(int_name))
        except(ConnectionError): # Not good
            print('Failed to GET Interface info from Device. Check interface name.\n')
            raise SystemExit



def main():
 
    urllib3.disable_warnings() # Disable 'untrusted certificate' warnings
    my_dev = asa(ip ='192.168.0.229', username='student', password='Cisco123') # Create object type 'asa'
    my_dev.auth_open() # Init auth to Device, get token
    mon_data = my_dev.get_int_info('inside') # Get 'inside' interface Info
    mon_dict = json.loads(mon_data) # Convert json to dictionary
    print('Input Byte Count: ', mon_dict['inputByteCount'])
    print('Output Byte Count: ', mon_dict['outputByteCount'])
    my_dev.auth_close() # Destroy auth token, taken by auth_open() above


if __name__ == '__main__':
    main()
