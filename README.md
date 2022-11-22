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
- [x] List all S3 repositories that are registered
- [x] List all snapshots with in a S3 repository
- [x] List all indices present on Opensearch
- [x] Delete S3 repository
- [x] Delete snapshot with in S3 repository
- [x] Delete indice present on Opensearch

## Setup Instructions

Before using this make sure that you have installed Opensearch repository-s3 plugin and restart your opensearch service.

```
$ /usr/share/opensearch/bin/opensearch-plugin install repository-s3 
$ systemctl restart opensearch
```

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

usage: opensearch-s3.py [-h] --host HOST [--testcon] [--indices INDICES] [--s3repo S3REPO] [--snap SNAP] [--auth AUTH]
                        [--action {registerrepo,takesnap,status,restore,restoreindice,listsnaps,listrepos,listindices,deleterepo,deletesnap,deleteindice}]

Script Creating and Restoring OpenSearch Snapshots on AWS S3 for Backup.

options:
  -h, --help            show this help message and exit
  --host HOST           Opensearch Host
  --testcon             To test connection to Opensearch RestAPI
  --indices INDICES     Name of indices to be backedup Ex: indice1,indice2-*,..
  --s3repo S3REPO       S3 Snapshot Repository Name
  --snap SNAP           Name of snapshot you want to create
  --auth AUTH           Basic HTTP Auth Token
  --action {registerrepo,takesnap,status,restore,restoreindice,listsnaps,listrepos,listindices,deleterepo,deletesnap,deleteindice}
                        List of actions register repo, take snapshot, get snapshot status, restore them.
```

## Usage
This script get the authtoken from env variable so you will need to define you Basic Auth token for Opensearch in your env variable.

```
$ export authtoken='basicauthbase64'
```
Also if you don't want to use env variables you can pass the auth token using arguments

```
$ python3 opensearch-s3.py --host localhost --action status --s3repo test --snap test --auth 'YWRtaW46YWRtaW4='
```

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
$ python3 opensearch-s3.py --host localhost --action takesnap --s3repo s3bucketname --snap test --indices test-statistics


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Name of Snapshot to be created: test-<currentdate>
<Response [200]>
{
 "accepted": true
}
Snapshot Registered Successfully: s3bucketname/test-2022-11-18
```

### Check Snapshot status (Success, Failed, errors)


```shell script
$ python3 opensearch-s3.py --host localhost --action status --s3repo s3bucketname --snap test


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Check the status of: test
<Response [200]>
Snapshot Status!!
{
 "snapshots": [
  {
   "snapshot": "test",
   "uuid": "-XgRId07SCGUz-i-h44lqw",
   "version_id": 135238227,
   "version": "1.2.4",
   "indices": [
    "test-statistics"
   ],
   "data_streams": [],
   "include_global_state": false,
   "state": "SUCCESS",
   "start_time": "2022-11-16T12:41:03.258Z",
   "start_time_in_millis": 1668602463258,
   "end_time": "2022-11-16T12:41:04.258Z",
   "end_time_in_millis": 1668602464258,
   "duration_in_millis": 1000,
   "failures": [],
   "shards": {
    "total": 1,
    "failed": 0,
    "successful": 1
   }
  }
 ]
}
```

### Restore Complete snapshot to new or same Opensearch instance


```shell script
$ python3 opensearch-s3.py --host localhost --action restore --s3repo s3bucketname --snap test


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Restore Snapshot: test
<Response [200]>
Snapshot Successfully Restored!!
{
 "accepted": true
}
```

### Restore specific indices from snapshot to new or same Opensearch instance


```shell script
$ python3 opensearch-s3.py --host localhost --action restoreindice --s3repo s3bucketname --snap test --indice sample-index1


 	Creating OpenSearch Snapshots on AWS S3 for Backup.
 	Author: OsamaMahmood - ( https://github.com/OsamaMahmood )


[+] Restore Specific indices form Snapshot: test Indices: sample-index1
<Response [200]>
Indices restore Status!!
{
 "accepted": true
}
```

### List all S3 repositories that are registered


```shell script
$ python3 opensearch-s3.py --host localhost --action listrepos
```

### List all snapshots with in a S3 repository


```shell script
$ python3 opensearch-s3.py --host localhost --action listsnaps --s3repo s3bucketname
```

### List all indices present on Opensearch


```shell script
$ python3 opensearch-s3.py --host localhost --action listindices
```

### Delete S3 repository


```shell script
$ python3 opensearch-s3.py --host localhost --action deleterepo --s3repo s3bucketname
```

### Delete snapshot with in S3 repository


```shell script
$ python3 opensearch-s3.py --host localhost --action deletesnap --s3repo s3bucketname --snap nameofsnapshot
```

### Delete indice present on Opensearch


```shell script
$ python3 opensearch-s3.py --host localhost --action deleteindice --indices indice-name
```
