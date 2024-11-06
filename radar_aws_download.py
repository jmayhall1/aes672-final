import os

import boto3
from botocore import UNSIGNED
from botocore.client import Config


s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))

for obj in s3client.list_objects(Bucket='noaa-nexrad-level2', Prefix='2024/09/27/KTLH')['Contents']:
    try:
        filename = obj['Key'].rsplit('/', 1)[1]
    except IndexError:
        filename = obj['Key']

    if 'MDM' in filename or int(filename[13: 15]) > 9:
        print('skipping')
        continue

    print('saving')
    localfilename = os.path.join('C:/Users/jmayhall/Downloads/ktlh_data/lv2-sept27/', filename)  # The local directory must exist.
    s3client.download_file('noaa-nexrad-level2', obj['Key'], localfilename)