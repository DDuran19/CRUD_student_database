import sqlite3

from utils import table_name,limit

DATABASE_PATH="student_database.sqlite3"
COMMA=','

def create(table_name: table_name, **kwargs) ->bool:
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        columns = ''
        question_marks=''
        values = []
        counter = 0
        for key, value in kwargs.items():
            counter+=1
            columns+=key
            question_marks+='?'
            values.append(value)
            if not counter == len(kwargs):
                question_marks+=COMMA
                columns+=COMMA



        query_string = f"INSERT INTO {table_name} ({columns}) \
            VALUES({question_marks})"
        values = tuple(values)
        try:
            cur.execute(query_string,values)
            db.commit()
        except Exception as error:
            print(error)
            return False
        
        return True

def read(table_name: table_name,id: int, limit:limit=limit.One) -> sqlite3.Cursor:
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        query=''
        table_name=table_name.value
        if table_name =="students":
            query +="SELECT students.id, students.Student_name, courses.course_name, year.year_level,\
                enrollment_status.enrollment_status,advisers.adviser_name, \
                organization.Organization\
                FROM students    \
                JOIN advisers ON students.Adviser_id = advisers.id    \
                JOIN courses ON students.Course_id = courses.id    \
                JOIN organization ON students.Organization_id = organization.id    \
                JOIN year ON students.Year_id = year.id\
                JOIN enrollment_status ON students.Enrollment_status_id = enrollment_status.id\
                    \
                WHERE students.id = ?"
            
        elif table_name=="advisers":
            query+="SELECT adviser_name FROM advisers where id = ?"

        elif table_name=="courses":
            query+="SELECT course_name FROM courses where id = ?"

        elif table_name=="year":
            query+="SELECT year_level FROM year where id = ?"

        elif table_name=="enrollment_status":
            query+="SELECT enrollment_status FROM enrollment_status where id = ?"

        elif table_name=="organization":
            query+="SELECT organization FROM organization where id = ?"
      
        rows=cur.execute(query,(id,))
        print(query)
        print(id)
        if limit: rows = cur.fetchone()
        else: rows = cur.fetchall()

        return rows
 
def update(table_name: table_name,id: int,**kwargs) -> bool:
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        columns=[]
        query_string = f'UPDATE {table_name} SET '
        for key, value in kwargs.items():
            columns.append(f'{key} = "{value}"')
        query_string+=f'{", ".join(columns)} WHERE id = ?'
        
        try:
            cur.execute(query_string,(id,))
            db.commit()
        except Exception as error:
            print(error)
            return False
        
        return True

def delete(table_name: table_name,id: int):
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        try:
            cur.execute(f'DELETE * FROM {table_name} WHERE id = ?', (id,))
            db.commit()
        except Exception as error:
            print(error)
            return False
        
        return True
    
def get_all_students():
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT students.id, students.Student_name, courses.course_name, year.year_level,\
                enrollment_status.enrollment_status,advisers.adviser_name, \
                organization.Organization\
                FROM students    \
                JOIN advisers ON students.Adviser_id = advisers.id    \
                JOIN courses ON students.Course_id = courses.id    \
                JOIN organization ON students.Organization_id = organization.id    \
                JOIN year ON students.Year_id = year.id\
                JOIN enrollment_status ON students.Enrollment_status_id = enrollment_status.id")
        return cur.fetchall()
def get_data_for_dropdown(data: str):
    """
    Get data for a dropdown list.

    Args:
        data: The name of the table to query.

    Returns:
        A list of strings containing the data for the dropdown list.

    **Allowed values for data:**
        advisers, year, courses, enrollment_status, organization
    """
    with sqlite3.connect(DATABASE_PATH) as db:
        cur = db.cursor()
        column=''
        
        match data:
            case "advisers":
                column = "adviser_name"
            case "year":
                column = "year_level"
            case "courses":
                column = "course_name"
            case "enrollment_status":
                column = data
            case "organization":
                column = data

        cur.execute(f"SELECT {column} FROM {data}")
        rows = cur.fetchall()
        advisers=[]
        for row in rows:
            advisers.append(row[0])
        return advisers



if __name__=="__main__":
    #create(table_name.advisers,adviser_name="Sample Adviser")
    #create(table_name.courses,course_name="Physics")
    update(table_name.advisers,1,adviser_name="Sample Adviser")
    
    print(read(table_name.advisers,1))
    print(read(table_name.courses,1))
    