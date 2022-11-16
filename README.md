# OpenSearch-Snapshots-S3-Repo
 Simple Python script to create an manage OpenSearch Snapshots.

## Description

Opensearch repository-s3 plugin does not have a UI app as of right now all the configuration has to be done using the Dev Tools (Opensearch RestAPI) this script help you in creating and managing those snapshot and you can setup corn job to schedule snapshots as well.

Feature Supports:

- [x] Test Opensearch RestAPI connection
- [x] Register S3 repository bucket to store snapshots
- [x] Take snapshots and put them in S3 repository
- [x] Check Snapshot status (Success, Failed, errors)
- [x] Restore Complete snapshot to new or same Opensearch instance
- [x] Restore specific indices from snapshot to new or same Opensearch instance

## Setup Instructions

Before using this make sure that you have installed Opensearch repository-s3 plugin and restart your opensearch service.

The installation method:

```shell script
$ git clone https://github.com/OsamaMahmood/OpenSearch-Snapshots-S3-Repo
$ cd OpenSearch-Snapshots-S3-Repo
$ pip3 install -r requirements.txt
```

Alternatively, you can setup a virtual environment and install dependencies:

```shell script
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

Run the tool:

```shell script
$ python3 opensearch-s3.py -h

usage: opensearch-s3.py [-h] --host HOST [--testcon] [--indices INDICES]
                        [--s3repo S3REPO] [--snap SNAP]
                        [--action {registerrepo,takesnap,status,restore,restoreindice}]

Script Creating and Restoring OpenSearch Snapshots on AWS S3 for Backup.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Opensearch Host
  --testcon             To test connection to Opensearch RestAPI
  --indices INDICES     Name of indices to be backedup Ex:
                        indice1,indice2-*,..
  --s3repo S3REPO       S3 Snapshot Repository Name
  --snap SNAP           Name of snapshot you want to create
  --action {registerrepo,takesnap,status,restore,restoreindice}
                        List of actions register repo, take snapshot, get
                        snapshot status, restore them.
```

## Usage

### Test Connection to Opensearch RestAPI


```shell script
$ python3 opensearch-s3.py --host localhost --testcon


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


Connection to Opensearch Successful!!
Name: node-1
Cluster Name: test-cluster
Version: 7.10.2
```
### Register S3 repository bucket to store snapshots


```shell script
$ python3 opensearch-s3.py --host localhost --action registerrepo --s3repo s3bucketname


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Register Snapshot Repository: s3bucketname
<Response [200]>
S3 Snapshot Repo Registered Successfully: s3bucketname
```
### Take snapshots and put them in S3 repository


```shell script
$ python3 opensearch-s3.py --host localhost --action registerrepo --s3repo s3bucketname


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Register Snapshot Repository: s3bucketname
<Response [200]>
S3 Snapshot Repo Registered Successfully: s3bucketname
```
