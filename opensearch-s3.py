#!/usr/bin/env python
import requests, json, argparse, os
from requests.exceptions import HTTPError
from colorama import Style,Fore

if os.name == 'nt':
	os.system('cls')
else:
	os.system('clear')

def start():
	print('''

 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )

		''')

parser = argparse.ArgumentParser(description='Script Creating and Restoring OpenSearch Snapshots on AWS S3 for Backup.')

parser.add_argument('--host',
                            help = 'Opensearch Host',
                            type = str,
                            required=True)

parser.add_argument('--testcon',
                            help = 'To test connection to Opensearch RestAPI',
                            action = 'store_true')

parser.add_argument('--indice',
                            help = 'Name of indice to be backedup',
                            type = str)

parser.add_argument('--s3repo',
                            help = 'S3 Snapshot Repository Name',
                            type = str)

parser.add_argument('--snap',
                            help = 'Name of snapshot you want to create',
                            type = str)

parser.add_argument('--action',
                            help = 'List of actions register repo, take snapshot, get snapshot status, restore',
                            choices = ('registerrepo', 'takesnap', 'status', 'restore'))


args = parser.parse_args()

host = args.host
s3repo = args.s3repo
indice = args.indice
snapname = args.snap

# Get environment variables
authtoken = os.environ.get('authtoken')

# Global variables
url = 'https://'+host+':9200/_snapshot/'
headers = {'content-type': 'application/json', 'Authorization': 'Basic '+authtoken}

def testconn(_host_):
    '''
    Simple Function to check if the Opensearch host is live and accessable.

    Args:
        _host_ (string): IP or hostname of the server.
    '''
    try:
        url = url = 'https://'+host+':9200/'
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
    except Exception as err:
        print(f'Other error: {err}')
    else:
        print(Fore.GREEN + 'Connection to Opensearch Successful!!')
        json_object = json.loads(response.content)
        print('Name: ' +json_object['name'])
        print('Cluster Name: ' +json_object['cluster_name'])
        print('Version: ' +json_object['version']['number']+Style.RESET_ALL)

def registerrepo(_reponame_):
	'''Register S3 Repo for snapshots using the Opensearch RestAPI

	Args:
		_reponame_ (string): Name of the snapshot repo this should be same as S3 bucket name for easier managment.
	
	Returns:
		If the snapshot repo does not exist it will create the repo.
	'''

	print ('[+] {}'.format('Register Snapshot Repository: '+_reponame_))
	# Register Snapshot Repository
	payload = {'type':'s3','settings':{'bucket':_reponame_}}
	try:
		response = requests.put(url+_reponame_, data=json.dumps(payload), headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		if json_object['acknowledged']:
			print(Fore.GREEN +'Snapshot Registered Successfully: '+_reponame_+Style.RESET_ALL)

def takesnapshot(_reponame_,_snapname_,_indicename_):
	'''Taking snapshot and storing it to S3 repo for backup

	Args:
		_reponame_ (string): Name of the snapshot repo this should be same as S3 bucket name for easier managment.
        _snapname_ (string): Name of the snapshot that is going to be created in the S3 repo.
	Returns:
		If the S3 snapshot repo exist it will create new snapshot in the S3 repo.
	'''

	print ('[+] {}'.format('Name of Snapshot to be created: '+_snapname_))

	# Name of indices that need to be backedup.
	payload = {'indices':''+_indicename_+'','ignore_unavailable':'true','include_global_state':'false','partial':'false'}
	try:
		response = requests.put(url+_reponame_+'/'+_snapname_, data=json.dumps(payload), headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(json.dumps(json_object, indent = 1))
  
def status(_reponame_,_snapname_):
	'''Check the status of Snapshot if its complete of in progress or if there is any error

	Args:
		_reponame_ (string): Name of the snapshot repo this should be same as S3 bucket name for easier managment.
        _snapname_ (string): Name of the snapshot that is going to be created in the S3 repo.
	'''

	print ('[+] {}'.format('Check the status of: '+_snapname_))

	try:
		response = requests.get(url+_reponame_+'/'+_snapname_, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(json.dumps(json_object, indent = 1))

def main():
    start()
    
    if args.testcon:
        testconn(host)
    elif args.action == 'registerrepo':
        registerrepo(s3repo)
    elif args.action == 'takesnap':
        takesnapshot(s3repo, snapname, indice)
    elif args.action == 'status':
        status(s3repo, snapname)
        
if __name__ == '__main__':
	main()
    