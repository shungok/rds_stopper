# load modules
from os import environ as env
from distutils.util import strtobool
import sys
import logging
import traceback
# local download modules.
import boto3
from botocore.exceptions import ClientError

# set const vars.
LOG_LEVEL = {
    'DEBUG':    logging.DEBUG,
    'INFO':     logging.INFO,
    'WARNING':  logging.WARNING,
    'ERROR':    logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# set logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Python version: {}'.format(sys.version))
    logger.info('boto3 version: {}'.format(boto3.__version__))
    logger.info('{} : start function with {}'.format(context.function_name, event))

    ############################################################
    # set log lovel.
    ############################################################
    if 'log_level' in event:
        log_level_name = event['log_level']
        if event['log_level'] in LOG_LEVEL:
            log_level = LOG_LEVEL[log_level_name]
            logger.setLevel(log_level)
            logger.info('set loglevel to {}.'.format(log_level_name))
        else:
            raise ValueError('Unkown log level: {}.'.format(log_level_name))

    ############################################################
    # set env vars.
    ############################################################
    TARGET_TAG_NAME = env.get('TARGET_TAG')

    ############################################################
    # prepare rds client.
    ############################################################
    session = boto3.Session()
    rds = session.client('rds')

    ############################################################
    # for RDS DB Instances
    ############################################################
    rds_instances = rds.describe_db_instances()['DBInstances']
    rds_available_instances = [ins for ins in rds_instances if 'DBClusterIdentifier' not in ins and ins['DBInstanceStatus'] == 'available']
    for ins in rds_available_instances:
        tags = rds.list_tags_for_resource(ResourceName=ins['DBInstanceArn'])['TagList']
        for tag in tags:
            if tag['Key'] == TARGET_TAG_NAME and strtobool(str(tag['Value'])) == True:
                logger.info(ins)
                res = rds.stop_db_instance(DBInstanceIdentifier=ins['DBInstanceIdentifier'])
                logger.info(res)

    ############################################################
    # for RDS DB Clusters
    ############################################################
    rds_clusters = rds.describe_db_clusters()['DBClusters']
    rds_available_clusters = [cls for cls in rds_clusters if cls['Status'] == 'available']
    for cls in rds_available_clusters:
        tags = rds.list_tags_for_resource(ResourceName=cls['DBClusterArn'])['TagList']
        for tag in tags:
            if tag['Key'] == TARGET_TAG_NAME and strtobool(str(tag['Value'])) == True:
                logger.info(cls)
                res = rds.stop_db_cluster(DBClusterIdentifier=cls['DBClusterIdentifier'])
                logger.info(res)

    logger.info('{} : end function with {}'.format(context.function_name, event))
    return True
