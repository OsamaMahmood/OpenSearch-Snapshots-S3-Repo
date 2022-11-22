#!/usr/bin/env python
import requests, json, argparse, os
from requests.exceptions import HTTPError
from colorama import Style,Fore
from datetime import datetime

# The following line is responsible for suppressing the SSL Cert warning.
requests.packages.urllib3.disable_warnings()

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

parser.add_argument('--indices',
                            help = 'Name of indices to be backedup Ex: indice1,indice2-*,..',
                            type = str)

parser.add_argument('--s3repo',
                            help = 'S3 Snapshot Repository Name',
                            type = str)

parser.add_argument('--snap',
                            help = 'Name of snapshot you want to create',
                            type = str)

parser.add_argument('--auth',
                            help = 'Basic HTTP Auth Token',
                            type = str)

parser.add_argument('--action',
                            help = 'List of actions register repo, take snapshot, get snapshot status, restore them.',
                            choices = ('registerrepo', 'takesnap', 'status', 'restore', 'restoreindice', 'listsnaps', 'listrepos', 'listindices', 'deleterepo', 'deletesnap', 'deleteindice'))

args = parser.parse_args()

host = args.host
s3repo = args.s3repo
indices = args.indices
snapname = args.snap

# Get environment variables
if args.auth:
	authtoken = args.auth
else:	
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
        url = 'https://'+host+':9200/'
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

def listrepos():
	'''
	Function to list all snapshot repositories
	'''

	print ('[+] {}'.format('List of Snapshot Repositories'))
	try:
		response = requests.get(url, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def listsnaps(_s3repo_):
	'''
	Function to list all snapshots in a repositoriey
	'''

	print ('[+] {}'.format('List of Snapshot Repositories'))
	try:
		response = requests.get(url+_s3repo_+'/_all', headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def listindices(_host_):
	'''
	Function to list all opensearch indices
	'''

	print ('[+] {}'.format('List of indices'))
	try:
		url = 'https://'+host+':9200/_cat/indices'
		response = requests.get(url, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		print(Fore.GREEN +response.content.decode('utf-8')+Style.RESET_ALL)

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
			print(Fore.GREEN +'S3 Snapshot Repo Registered Successfully: '+_reponame_+Style.RESET_ALL)

def takesnapshot(_reponame_,_snapname_,_indicename_):
	'''Taking snapshot and storing it to S3 repo for backup

	Args:
		_reponame_ (string): Name of the snapshot repo this should be same as S3 bucket name for easier managment.
        _snapname_ (string): Name of the snapshot that is going to be created in the S3 repo.
		_indicename_ (string): Name of the indices you want to take snapshot of.
	Returns:
		If the S3 snapshot repo exist it will create new snapshot in the S3 repo.
	'''

	print ('[+] {}'.format('Name of Snapshot to be created: '+_snapname_))
	snapnamedate=_snapname_+'-'+str(datetime.date(datetime.now()))
	print(snapnamedate)
	# Name of indices that need to be backedup.
	payload = {'indices':''+_indicename_+'','ignore_unavailable':'true','include_global_state':'false','partial':'false'}
	try:
		response = requests.put(url+_reponame_+'/'+snapnamedate, data=json.dumps(payload), headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'Snapshot with same name already exists: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)
		print(Fore.GREEN +'Snapshot Registered Successfully: '+_reponame_+'/'+_snapname_+Style.RESET_ALL)
  
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
		print(f'Snapshot not found: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		print(Fore.GREEN + 'Snapshot Status!!')
		json_object = json.loads(response.content)
		print(json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def restore(_reponame_,_snapname_):
	'''
	Function to restore complete snapshot to opensearch.

	Args:
		_reponame_ (string): name of the opensearch s3 repo 
		_snapname_ (string): name of the snapshot want to restore
	'''

	print ('[+] {}'.format('Restore Snapshot: '+_snapname_))
	try:
		response = requests.post(url+_reponame_+'/'+_snapname_+'/_restore', headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'Open index with same name already exists delete them inorder to restore: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		print(Fore.GREEN + 'Snapshot Successfully Restored!!')
		json_object = json.loads(response.content)
		print(json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def restoreindice(_reponame_,_snapname_,_indices_):
	'''
	Fucntion to restore specific indices from a snapshot

	Args:
		_reponame_ (string): name of the opensearch s3 repo
		_snapname_ (string): name of snapshot
		_indices_ (string): name of indices you want to restore ex indice1,indice2
	'''

	print ('[+] {}'.format('Restore Specific indices form Snapshot: '+_snapname_+' Indices: '+_indices_))

	payload = {'indices':''+_indices_+'','ignore_unavailable':'true','include_global_state':'false','include_aliases':'false','partial':'false'}
	try:
		response = requests.post(url+_reponame_+'/'+_snapname_+'/_restore', data=json.dumps(payload), headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'Open index with same name already exists delete them inorder to restore: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		print(Fore.GREEN + 'Indices restore Status!!')
		json_object = json.loads(response.content)
		print(json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def deleterepo(_s3repo_):
	'''
	Function to delete repository
	'''

	print ('[+] {}'.format('Delete Snapshot Repository'))
	try:
		response = requests.delete(url+_s3repo_, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def deletesnap(_s3repo_,_snapname_):
	'''
	Function to delete snapshot in repository
	'''

	print ('[+] {}'.format('Delete Snapshot in Repository'))
	try:
		response = requests.delete(url+_s3repo_+'/'+_snapname_, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def deleteindice(_host_,_indice_):
	'''
	Function to delete indices from opensearch
	'''

	print ('[+] {}'.format('Delete indices'))
	url = 'https://'+host+':9200/'
	try:
		response = requests.delete(url+_indice_, headers=headers, verify=False)
		response.raise_for_status()
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Other error: {err}')
	else:
		print(response)
		json_object = json.loads(response.content)
		print(Fore.GREEN +json.dumps(json_object, indent = 1)+Style.RESET_ALL)

def main():
    start()
    
	#If testcon is passed in args following function will be called
    if args.testcon:
        testconn(host)

	#If action arg is set to registerrepo following functiuon will be called to register s3 snapshot repo
    elif args.action == 'registerrepo':
        registerrepo(s3repo)

	#If action arg is set to takesnap following function will be called with the repo name, name of snapshot and the indices that you want to include in the snapshot.
    elif args.action == 'takesnap':
        takesnapshot(s3repo, snapname, indices)

	#if action arg is set to status following function will be called with repo name and the name of snapshot to check the status.
    elif args.action == 'status':
        status(s3repo, snapname)

	#if action arg is set to restore following function will be called with repo name and the name of snapshot to restore to openserarch.
    elif args.action == 'restore':
        restore(s3repo, snapname)

	#if action arg is set to restore following function will be called with repo name and the name of snapshot to restore specific indices to openserarch.
    elif args.action == 'restoreindice':
        restoreindice(s3repo, snapname, indices)

	#if action arg is set to listrepos following function will be called to list all repos that are registered.
    elif args.action == 'listrepos':
        listrepos()

	#if action arg is set to listsnaps following function will be called to list all snapshots in a repo.
    elif args.action == 'listsnaps':
        listsnaps(s3repo)

	#if action arg is set to listindices following function will be called to list all indices in opensearch.
    elif args.action == 'listindices':
        listindices(host)

	#if action arg is set to deleterepo following function will be called with s3repo name to delete the repo.
    elif args.action == 'deleterepo':
        deleterepo(s3repo)

	#if action arg is set to deletesnap following function will be called with repo name and snap name to delete snapshot in repo.
    elif args.action == 'deletesnap':
        deletesnap(s3repo, snapname)

	#if action arg is set to deleteindice following function will be called to delete that indice on opensearch
    elif args.action == 'deleteindice':
        deleteindice(host, indices)


if __name__ == '__main__':
	main()
