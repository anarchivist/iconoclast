"""
iconoclast.py
"""

import logging
import optparse
import sys
import os
import boto
from iiif.static import IIIFStatic

s3 = boto.client('s3')
destbucket = 'iconoclast-test'
#todo: add some config

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        inbound = '/tmp/inbound/%s' % key
        outbound = '/tmp/outbound/%s' % key
        s3_client.download_file(bucket, key, inbound)

        # TODO: Add prefix
        sg = IIIFStatic(dst=outbound, tilesize=512, api_version='2.0')
        sg.generate(inbound)
        for dirpath, dirnames, files in os.walk(outbound):
            for f in files:
                s3_client.upload_file(os.path.join(dirpath, f), destbucket, f)