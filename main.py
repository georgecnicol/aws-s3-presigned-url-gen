#!/usr/bin/python3

import argparse
import boto3

parser = argparse.ArgumentParser()
parser.add_argument('-b', dest = 'bucket', nargs = 1, required = True, help = "Bucket name, eg: my-s3-bucket")
parser.add_argument('-k', dest = 'key', nargs = 1, required = True, help = "Key name, eg: prefix/filename.file")
parser.add_argument('-t', dest = 'time', nargs = '?', type = int, help = "Number of seconds before expiration")
parser.set_defaults(time=3600)
group = parser.add_mutually_exclusive_group(required = True)
group.add_argument('g', dest = 'get', action = 'store_true', help = "Either get (-g) or put (-p) but not both.")
group.add_argument('p', dest = 'get', action = 'store_false', help = "Make sure you have appropriate policies")

args = parser.parse_args()

action = 'get_object' if args.get else 'put_object'
s3 = boto3.client('s3')
url = s3.generate_presigned_url(ClientMethod = action, Params = {'Bucket' : args.bucket[0], 'Key' : args.key[0]}, ExpiresIn = args.time)
if action == 'put_object':
  print(f'For upload:')
  print(f'curl --upload-file /path/to/file \'pre-signed-url\'')

print(f'pre-signed url:\n{url}')
