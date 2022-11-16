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

## Usage

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
```

