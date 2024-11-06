# coding=utf-8
"""
@author: John Mark Mayhall
email: jmm0111@uah.edu
Last Edit: 11/06/2024
Code for downloading NEXRAD data from AWS.
"""
import os

import boto3
from botocore import UNSIGNED
from botocore.client import Config


def downloader(data_bucket: str, data_prefix: str, local_path: str, time_start=None, time_limit=None):
    """
    Function for downloading data for AWS based on a data bucket and the bucket's prefix. The function then saves the
    data to a given path. A time start and limit can also be provided to only download files in a certain timeframe.
    :param data_bucket: The AWS bucket you want to download from.
    :param data_prefix: The year, month, and day you want to download data from.
    :param local_path: The path you want to save files to.
    :param time_start: Optional, files from before this integer will be skipped
    :param time_limit: Optional, files from after this integer will be skipped.
    """
    s3client = boto3.client('s3', config=Config(signature_version=UNSIGNED))  # Initializes the sign-in key for AWS
    for obj in s3client.list_objects(Bucket=data_bucket, Prefix=data_prefix)['Contents']:  # Grabs all files
        try:  # Accounts for naming differences.
            filename = obj['Key'].rsplit('/', 1)[1]
        except IndexError:
            filename = obj['Key']
        if 'MDM' in filename or int(filename[13: 15]) < time_start:  # Allows files to be skipped
            print('skipping')
            continue
        if 'MDM' in filename or int(filename[13: 15]) > time_limit:  # Allows files to be skipped
            print('skipping')
            continue

        print('saving')
        localfilename = os.path.join(local_path,
                                     filename)  # The local directory must exist.
        s3client.download_file(data_bucket, obj['Key'], localfilename)  # Downloads the files.


if __name__ == "__main__":
    downloader(data_bucket='noaa-nexrad-level2', data_prefix='2024/09/27/KTLH',
               local_path='C:/Users/jmayhall/Downloads/ktlh_data/lv2-sept27/', time_limit=9)
