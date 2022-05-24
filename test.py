import requests

def main():

name = 'student'

pawd =  'Cisco123'

url =  'https://192.168.0.229/doc'
headers = {'Connection':  'Close',  'User-Agent':  'REST API Agent'}
data = {'msid': phone, 'message': mess, 'naming': name, 'login': user, 'password': pamd5} 

response = requests.post(url=url, data=data, headers=headers)

if response:
    print( 'Success!')
else:
    print( 'An error has occurred.')


if __name__ == '__main__':
    main()
