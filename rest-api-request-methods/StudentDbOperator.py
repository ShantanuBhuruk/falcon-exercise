"""
Basic Database CRUD Operations using MySql with Python
Written by Shantanu Bhuruk
"""
import json
import falcon
import mysql.connector

"""
Student Database Operations Class
"""


class StudentDBOperator:
    con = None
    cur = None

    __json_content = {}

    """
    Create a database connection
    """

    def __init__(self):
        pass

    def __validate_json(self, req):
        try:
            self.__json_content = json.loads(req.stream.read())
            print("Valid Input JSON")
            return True
        except ValueError as e:
            self.__json_content = {}
            print("Invalid Input JSON")
            return False

    def create_connection(self):
        self.con = mysql.connector.connect(host="localhost", user="root", passwd="")
        print(f"Connected to Database Server {self.con.server_host}:{self.con.server_port}")
        return self.con

    """
    Close Database Connection
    """

    def close_connection(self):
        self.con.close()

    """
    Create a cursor
    """

    def create_cursor(self):
        self.cur = self.con.cursor()
        self.cur.execute("Use Test")
        print("Using Database Test...!!!")
        return self.cur

    """
    Insert Student into the Database
    """

    def on_post(self, req, resp):
        self.create_connection()
        self.create_cursor()
        resp.status = falcon.HTTP_200
        validated = self.__validate_json(req)
        output = {}
        if validated:
            insert_sql = "INSERT INTO STUDENT (NAME, BRANCH, ROLL, SECTION, AGE) VALUES (%s, %s, %s, %s, %s)"
            req_params = self.__json_content
            values = (req_params["name"], req_params["branch"], req_params["roll_no"], req_params["section"], req_params["age"])
            self.cur.execute(insert_sql, values)
            self.con.commit()
            print(f"Record Inserted: {values}")
            output = {
                "msg": "Record Inserted {}".format(values)
            }
        else:
            output = {
                "msg": "Invalid Json Input"
            }
        self.close_connection()
        resp.body = json.dumps(output)

    """
    Update Student
    """

    def on_put(self, req, resp):
        self.create_connection()
        self.create_cursor()
        resp.status = falcon.HTTP_200
        update_sql = "UPDATE STUDENT SET NAME = %s, BRANCH = %s, SECTION = %s, AGE = %s WHERE ROLL = %s"
        req_params = json.loads(req.stream.read())
        values = (req_params["name"], req_params["branch"], req_params["section"], req_params["age"], req_params["roll_no"])
        self.cur.execute(update_sql, values)
        self.con.commit()
        print(f"Record Updated: {values}")
        output = {
            "msg": "Record Updated {}".format(values)
        }
        self.close_connection()
        resp.body = json.dumps(output)

    """
    Delete Student
    """

    def on_delete(self, req, resp):
        self.create_connection()
        self.create_cursor()
        resp.status = falcon.HTTP_200
        delete_sql = "DELETE FROM STUDENT WHERE ROLL = %(a)s"
        req_params = json.loads(req.stream.read());
        self.cur.execute(delete_sql, {"a": req_params["roll_no"]})
        self.con.commit()
        print(f"Record with Roll No: {req_params['roll_no']} has been deleted")
        output = {
            "msg": "Record with Roll No: {} has been deleted".format(req_params['roll_no'])
        }
        self.close_connection()
        resp.body = json.dumps(output)

    """
    Select all Students from Database
    """

    def on_get(self, req, resp):
        self.create_connection()
        self.create_cursor()
        resp.status = falcon.HTTP_200
        params = req.params
        if params:
            self.cur.execute("SELECT * FROM STUDENT WHERE NAME = %(a)s", {"a": params["name"]})
        else:
            self.cur.execute("SELECT * FROM STUDENT")
        records = self.cur.fetchall()

        print("Fetched data from Student : ")
        students = []
        for record in records:
            print(record)
            student = dict()
            student["Name"] = record[0]
            student["Branch"] = record[1]
            student["Roll No"] = record[2]
            student["Section"] = record[3]
            student["Age"] = record[4]
            students.append(student)

        output = {
            "students": students
        }
        self.close_connection()
        resp.body = json.dumps(output)


def main():
    student_db_operator = StudentDBOperator()
    student_db_operator.create_connection()
    student_db_operator.create_cursor()


if __name__ == "__main__": main()
