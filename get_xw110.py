# Copyright (c) 2018 Leeman Geophysical LLC.
# Distributed under the terms of the MIT License.
"""Send data from XW110 sensor to AWS S3 as a lambda function."""

import boto3
import datetime
import logging
import json
import urllib.request
import xml.etree.ElementTree as ET


URL = 'http://73.130.117.239:1139/state.xml'
BUCKET_NAME = 'scepool'
KEY = 'xw110data.json'


def lambda_handler(event, context):

    logging.info('Requesting XML.')
    data = {}
    with urllib.request.urlopen(URL) as f:
        tree = ET.parse(f)
        root = tree.getroot()

    logging.info('Success.')
    # Fill dictionary with XML data
    tags = ['units', 'sensor1', 'sensor2', 'sensor3', 's1Alrm', 's2Alrm', 's3Alrm',
            'battery', 'batteryVoltage', 'powersource', 'time']
    for child in root:
        if child.tag in tags:
            data[child.tag] = child.text

    # Make timestamp into time string
    data['time'] = datetime.datetime.fromtimestamp(int(data['time']))
    data['time'] = data['time'].strftime('%Y-%m-%d %H:%M:%S')

    json_payload = json.dumps(data)

    logging.info('Sending to S3.')
    # Write file to S3
    # Create an S3 client
    s3 = boto3.client('s3')

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.put_object(Body=json_payload, Bucket=BUCKET_NAME, Key=KEY)
    logging.info('Success.')
