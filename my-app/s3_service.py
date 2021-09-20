import boto3

s3 = boto3.client('s3', region_name='us-east-2')

BUCKET = 'chalice-demo2'


def upload_file(app, filename):
    try:
        body = app.current_request.raw_body
        print(filename)
        temp_file = '/tmp/' + filename
        with open(temp_file, 'wb') as f:
            f.write(body)
        s3.upload_file(temp_file, BUCKET, filename)
    except Exception as e:
        app.log.error("Error while uploading file to s3", e)
        return {"error": "Could not upload the file"}


def list_buckets(app):
    try:
        response = s3.list_buckets()
        print(response)
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        return {"bucket_list": buckets}
    except Exception as e:
        app.log.error("Unable to fetch s3 buckets", e)
        return {"error": "Could not fetch s3 buckets"}

