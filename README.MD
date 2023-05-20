## Student Database

<strong style="color:lightblue">Overview</strong>:
    Simple application that allows a user to Create, Read, Updated and Delete data on a database.

<strong style="color:lightblue">Database Schema</strong> (sqlite3):

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        Student_name CHAR(50),
        Organization_id INTEGER,
        Enrollment_status_id INTEGER,
        Adviser_id INTEGER,
        Course_id INTEGER,
        Year_id INTEGER
    );

    CREATE TABLE IF NOT EXISTS advisers (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        adviser_name CHAR(50)
    );
    
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        course_name CHAR(20)
    );

    CREATE TABLE IF NOT EXISTS year (
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        year_level CHAR(9)
    );
    
    CREATE TABLE IF NOT EXISTS enrollment_status(
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        enrollment_status CHAR(20)
    );

    CREATE TABLE IF NOT EXISTS organization(
        id INTEGER PRIMARY KEY UNIQUE NOT NULL,
        organization CHAR(20)
    );
    
    

<strong style="color:lightblue">Planning</strong>:

* We are going to setup our relational database by creating four distinct tables: `users`, `advisers`, `courses`, `year`. This is going to ensure that we do NOT repeat strings therefore increasing our app's efficiency. To keep things simple,
we are going to use SQLite3 for this project.
* Using customtkinter, we will create a GUI for manipulating data