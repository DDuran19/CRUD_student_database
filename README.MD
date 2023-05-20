# Student Database

## <strong style="color:lightblue">Overview</strong>:

This project aims to create a relational database management system using `SQLite3` and implement a user-friendly graphical user interface (GUI) using `customtkinter`. The application will consist of four distinct tables: `users`, `advisers`, `courses`, and `year`. The use of a database will ensure efficient data storage and retrieval by avoiding repetition of strings.


## <strong style="color:lightblue">Features</strong>:

<strong style = "color:orange">Relational Database</strong>: The project utilizes SQLite3 to set up and manage the database. The tables include users, advisers, courses, and year, ensuring efficient data organization and retrieval.

<strong style = "color:orange">customtkinter</strong>: The graphical user interface is built using customtkinter, providing a user-friendly interface for manipulating the database. The GUI layout consists of a main table on the top section, an info section on the bottom left for data editing/modification, and a button section on the bottom right.

<strong style = "color:orange">Edit/View Mode</strong>: The GUI includes a slider that allows users to switch between edit and view modes, enabling easy modification or viewing of the data.

<strong style = "color:orange">Data Manipulation</strong>: The GUI provides three main buttons for adding, updating/saving, and deleting data. These buttons facilitate seamless data manipulation within the database.

<strong style = "color:orange">Exit Functionality</strong>: An "exit" button is included to provide a convenient way for users to exit the application.


## <strong style="color:lightblue">Usage</strong>:
1. Launch the application by running the main.py file.

2. The main table will be displayed on the top section of the GUI, showcasing the data from the users, advisers, courses, or year table.

3. Use the slider to switch between edit and view modes. In edit mode, the info section on the bottom left becomes active, allowing users to modify or edit the selected data.

4. Use the buttons in the button section on the bottom right to perform various operations:

    - <strong style = "color:orange">Add</strong>: Add new data to the database.
    - <strong style = "color:orange">Update/Save</strong>: Update or save the modified data.
    - <strong style = "color:orange">Delete</strong>: Delete selected data from the database.
    - <strong style = "color:orange">To exit</strong> the application, click the "exit" button.

## <strong style="color:lightblue">Database Schema</strong> (sqlite3):

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
## <strong style="color:lightblue">AUTHOR</strong>
Denver James Duran
- [Facebook](https://www.facebook.com/denver02.james14/)
- [Github](https://github.com/DDuran19)

You can find this repository [here](https://github.com/DDuran19/CRUD_student_database.git).
