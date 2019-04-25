## Overview
This project provide a sytem structure to stop AWS RDS resources continuously.

Currently(As of 2019-04-25), you can stop DB instances / clusters that are RDS resources, but they will be started automatically after 7 days.

* [Official Document: Stopping an Amazon RDS DB Instance Temporarily](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_StopInstance.html)

In order to stop the DB instance / cluster continuously under this restriction, it is realized using the following AWS services.

* [Lambda](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
* [CloudWatch Events](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html)


Lambda is used to execute a function to stop a resource that has been tagged to indicate the stop target. And CloudWatch Events is used to invoke this function daily at a.m. 0 (default) in UTC time zone.

The above configuration is built using [Serverless Framework](https://serverless.com/).

## Project directory structure

```
rds_stopper
├── README.md
├── lambda      … Lambda function scripts.
│   └── main.py
└── serverless  … Serverless Framework settings.
    ├── events  … CloudWatch Events settings.
    │   └── main.yml
    └── serverless.yml

3 directories, 4 files
```

## Runtime environment

verificated runtime envirnment as following.

### Serverless Framework

```
$ sls --version
1.36.3
```

### Lambda

* Python version: 3.7.2 (default, Mar 1 2019, 11:28:42)
* boto3 version: 1.9.42

## Usage

### 1. Deployment of AWS Environment

First time, you have to execute deploy command.

```
$ cd /path/to/rds_stopper/serverless
$ sls deploy
```

If you ware changed only lambda function, you will be able to deploy function command.

```
$ sls deploy function -f main
```

### 2. Setting for RDS Resource to stop

Using AWS console / AWS CLI, Add the following tag(Key/Value) to the resource which you want to stop.

* Key
  * LAMBDA_RDS_STOPPER_TARGET (default)
* Value
  * True (A string representing 'true', for example True/true/1...)

If you would like to change Key name, you can change ```TARGET_TAG``` in ```serverless.yml```.

```
$ cat serverless.yml
…
TARGET_TAG: LAMBDA_RDS_STOPPER_TARGET
…
```

If the RDS resource is a cluster, you have to tag the cluster. Even if you tag individual instances belonging to a cluster, you can not stop them alone.

### FAQ
#### How to invoke lambda function with manual?

basic invokation is as following.

```
$ sls invoke -f main
```

If you would like to change the log level, you can set "log_level" in Lambda event data.

```
$ sls invoke -f main -d '{ "log_level": "DEBUG" }'
```

valid "log_level" string are as following.

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL
