from chalice import Chalice, BadRequestError, IAMAuthorizer, CognitoUserPoolAuthorizer
import os
from chalicelib.s3_service import list_buckets as list_s3_buckets, upload_file
from chalicelib.sqs_service import create_queue, send_message, get_messages

app = Chalice(app_name='my-app')


BUCKET = 'chalice-demo2'


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/getFullName/{key}', methods=['GET'])
def getFullCountryName(key):
    req = app.current_request
    print(req.query_params)
    print(req.uri_params)
    if len(key) < 2:
        raise BadRequestError("Invalid request")
    countries = {'IND': 'India', 'CHN': 'China'}
    return {'full_name': countries[key]}


@app.route('/postCountries', methods=['POST'])
def handlePost():
    countries = app.current_request.json_body['countries']
    return {'countries': countries}


@app.route('/read_env_variable')
def read_env():
    return {"db_url": os.environ['db_url']}


@app.route("/list_buckets")
def list_buckets():
    return list_s3_buckets(app)


@app.route('/upload_file_s3/{filename}', methods=['PUT'], content_types=['application/octet-stream'])
def upload(filename):
    return upload_file(app, filename)


@app.route('/create_queue', methods=['POST'])
def create_sqs_queue():
    return create_queue()


@app.route('/send_message', methods=['POST'])
def send_sqs_message():
    json = app.current_request.json_body
    return send_message(str(json))


@app.on_s3_event(bucket=BUCKET, events=["s3:ObjectCreated:*"])
def handle_s3_event(event):
    print(event.bucket, event.key)
    send_message(event.key)


@app.route('/get_messages', methods=['GET'])
def get_messages_from_sqs():
    return get_messages()


authorizer = CognitoUserPoolAuthorizer(
    'us-east-2_MshHcL28D', provider_arns=['arn:aws:cognito-idp:us-east-2:470181881791:userpool/us-east-2_MshHcL28D'])

iam_authorizer = IAMAuthorizer()


@app.route('/user-pools', methods=['GET'], authorizer=authorizer)
def authenticated():
    return {"success-user-pools": True}


@app.route('/iam-role', methods=['GET'], authorizer=iam_authorizer)
def authenticated_iam():
    return {"success-iam-role": True }


@app.route('/secured_endpoint', methods=['GET'], authorizer=iam_authorizer)
def test_secure_app():
    return { 'accessed_secured': True }

