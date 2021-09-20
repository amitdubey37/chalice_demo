from chalice import Chalice
from chalicelib import department_service
app = Chalice(app_name='my-app')

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/setup' ,methods=['GET'])
def setup_app():
    return department_service.create_db()


@app.route('/cleanup' ,methods=['GET'])
def cleanup():
    return department_service.process_cleanup()


@app.route('/department' ,methods=['GET'])
def select_all():
    return department_service.select_all()

@app.route('/department/insert' ,methods=['POST'])
def process_insert():
    return department_service.process_insert(app,"1234") 

@app.route('/department/update' ,methods=['POST'])
def process_update():
    return department_service.process_update(app,"1234") 

@app.route('/department/{department_id}' ,methods=['GET'])
def process_select(department_id):
    return department_service.process_select(department_id) 

@app.route('/department/delete/{department_id}' ,methods=['GET'])
def process_delete(department_id):
    return department_service.process_delete(department_id) 



