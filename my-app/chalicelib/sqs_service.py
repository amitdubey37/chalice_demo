from chalice import Chalice, Response
import boto3

sqs = boto3.client('sqs')


QUEUE_NAME = 'chalice-demo-queue'


def create_queue():
    try:
        queue = sqs.create_queue(QueueName=QUEUE_NAME, Attributes={"DelaySeconds": "5"})
        print(queue)
        return {'success': True, 'message': f'queue with name {QUEUE_NAME} created', 'status': 200}

    except Exception as e:
        print(e)
        return {'status_code': 400}


def send_message(message_body):
    try:
        queue_res = sqs.get_queue_url(QueueName=QUEUE_NAME)
        print(queue_res)
        queue_url = queue_res['QueueUrl']
        response = sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=message_body)
        return {'status': 200, 'message': 'Message sent {}'.format(response['MessageId'])}
    except Exception as e:
        print(e)
        return {'status': 400, 'message': "unable to send sqs message"}


def get_messages():
    try:
        queue_response = sqs.get_queue_url(QueueName=QUEUE_NAME)
        queue_url = queue_response['QueueUrl']
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=20,
            WaitTimeSeconds=20
        )

        messages = response['Messages']

        return messages

    except Exception as e:
        print(str(e))
        # app.log.error('error occurred during creating queue')
        return {"Error": 'error occurred during sending message queue' + str(e), "status_code": 400}
