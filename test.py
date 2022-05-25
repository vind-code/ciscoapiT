import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3




def main():

    username = 'student'
    pawd =  'Cisco123'
    url =  'https://192.168.0.229/api/tokenservices'
    headers = {'Connection':  'Close',  'Content-type': 'application/json', 'User-Agent':  'REST API Agent'}
 
    urllib3.disable_warnings()

    response = requests.post(url=url, headers=headers, auth=HTTPBasicAuth(username, pawd), verify=False)

    if response:
        jsonResp = response.json()
        print (jsonResp)
    else:
        print( 'An error has occurred.')


if __name__ == '__main__':
    main()
