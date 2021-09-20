from chalicelib import db
from chalicelib import SqlQueries
from chalice import Chalice, Response
from chalice import BadRequestError


def select_all():
    return db.PostgresqlDB().query(SqlQueries.DEPARTMENT_SELECT_ALL, "")


def create_db():
    try:
        db.PostgresqlDB().update(SqlQueries.DB_CREATE,
                                 ('create db'))
        return {"status_code": '200',
        "description": 'department table is created successfully '
        }
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}


def process_select(departments_id):
    try:
        db.PostgresqlDB().update(SqlQueries.DEPARTMENT_SELECT,
                                 (departments_id))
        return {"departments": select_all()}
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}





def process_insert(app, user_id):
    try:
        departments_list = app.current_request.json_body['departments']
        for department in departments_list:
            db.PostgresqlDB().update(SqlQueries.DEPARTMENT_INSERT,
                                     (department['department_name'], user_id, user_id))
        return {"departments": select_all()}
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}

def process_update(app, user_id):
    try:
        departments_list = app.current_request.json_body['departments']
        for department in departments_list:
            db.PostgresqlDB().update(SqlQueries.DEPARTMENT_UPDATE,
                                     (department['department_name'], user_id, department['department_id']))
        return {"departments": select_all()}
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}

def process_delete(department_id):
    try:
        
        db.PostgresqlDB().update(SqlQueries.DEPARTMENT_DELETE,(department_id))
        return {"departments": select_all()}
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}


def process_cleanup():
    try:
        
        db.PostgresqlDB().update(SqlQueries.DROP_TABLE,"")
        return {"departments": select_all()}
        # return {"Success ":"Record inserted successfully","status_code":200}
    except Exception as err:
        return {"Error ": str(err), "status_code": 400}