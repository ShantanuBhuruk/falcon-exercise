import pytest
import falcon
from falcon.testing.helpers import create_environ

from StudentDbOperator import StudentDBOperator


@pytest.fixture()
def setup():
    return StudentDBOperator()


@pytest.fixture()
def setup():
    return StudentDBOperator()


def get_request(body, query_string=''):
    env = create_environ(
        path='/student',
        host="localhost",
        port="8000",
        headers={'Content-Type': 'application/json'},
        query_string=query_string,
        body=body,
        method='POST',
    )
    req = falcon.Request(env)
    return req


def get_response():
    return falcon.Response()


def test_json_validation(setup):
    body = '''{
            "name": "Chandan",
            "branch": "Dev",
            "roll_no": 28,
            "section": "A",
            "age": 28
        }'''
    req = get_request(body)
    student_db_operator = setup
    validated1 = student_db_operator.validate_json(req)
    incorrect_req = get_request("")
    validated2 = student_db_operator.validate_json(incorrect_req)
    assert validated1 == True
    assert validated2 == False


def test_create_and_close_connection(setup):
    student_db_operator = setup
    con = student_db_operator.create_connection()
    assert con.is_connected()
    student_db_operator.close_connection()
    assert not con.is_connected()


def test_create_cursor(setup):
    student_db_operator = setup
    student_db_operator.create_connection()
    cur = student_db_operator.create_cursor()
    assert cur
    cur.close()
    student_db_operator.close_connection()


def test_insert(setup):
    body = '''{
                "name": "Vinayak",
                "branch": "Dev",
                "roll_no": 30,
                "section": "A",
                "age": 28
            }'''
    req = get_request(body)
    resp = get_response()
    student_db_operator = setup
    student_db_operator.on_post(req, resp)
    print(resp.media)
    assert "Record Inserted" in resp.media["msg"]


def test_update(setup):
    body = '''{
                "name": "Vinayak",
                "branch": "Dev",
                "roll_no": 30,
                "section": "A",
                "age": 28
            }'''
    req = get_request(body)
    resp = get_response()
    student_db_operator = setup
    student_db_operator.on_put(req, resp)
    print(resp.media)
    assert "Record Updated" in resp.media["msg"]


def test_delete(setup):
    body = '{"roll_no": 30}'
    req = get_request(body)
    resp = get_response()
    student_db_operator = setup
    student_db_operator.on_delete(req, resp)
    print(resp.media)
    assert "has been deleted" in resp.media["msg"]


def test_select(setup):
    req = get_request("")
    resp = get_response()
    student_db_operator = setup
    student_db_operator.on_get(req, resp)
    print(resp.media)
    assert resp.media["students"]


def test_select_by_name(setup):
    req = get_request("", 'name=shantanu')
    resp = get_response()
    student_db_operator = setup
    student_db_operator.on_get(req, resp)
    print(resp.media)
    assert "Shantanu" == resp.media["students"][0]["Name"]








