import customtkinter as CTk
import tkinter as stk

from tkinter import ttk
from dataclasses import dataclass
from typing import Optional,Union
from random import choice
from time import sleep

from queries import create,read,update,delete,get_all_students,get_data_for_dropdown
from utils import limit,table_name

EMPTY_STRING: str = ''
END: str = 'end'
@dataclass
class main_window:
    window: CTk.CTk | None = None

    TITLE="Student Database Manager"
    WIDTH = 1280
    HEIGHT= 720
    APPEARANCE_MODE = "dark"
    SHOW_PASSWORD = False

    table_style: Optional[ttk.Style] = None
    style: Optional[ttk.Style] = None
    table: Optional[ttk.Treeview] = None
    columns: tuple[str] = ('id','Student_Name','Year','Course', "Organization",
                           'Adviser', 'Enrollment_Status')
    headers: tuple[str] = ('Student ID','Student Name','Year','Course', "Organization",
                           'Adviser', 'Enrollment Status')

    column_label=0
    column_entry=1

    controls_frame: Optional[CTk.CTkFrame] = None
    info_frame: Optional[CTk.CTkFrame] = None
    entry_frame: Optional[CTk.CTkFrame] = None

    student_id: Optional[CTk.CTkEntry] = None
    student_name: Optional[CTk.CTkEntry] = None
    year: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    course: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    organization: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    adviser: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    enrollment_status: Union[CTk.CTkComboBox,CTk.CTkEntry] = None

    buttons_frame: Optional[CTk.CTkFrame] = None
    is_in_View_Mode: bool = True
    is_in_new_mode: bool = False
    view_mode_toggler: Optional[CTk.CTkSwitch] = None

    year_dropdown=get_data_for_dropdown('year')
    course_dropdown=get_data_for_dropdown('courses')
    organization_dropdown=get_data_for_dropdown('organization')
    adviser_dropdown=get_data_for_dropdown('advisers')
    enrollment_status_dropdown=get_data_for_dropdown('enrollment_status')

    name_is_valid=False
    year_is_valid=False
    course_is_valid=False
    organization_is_valid=False
    adviser_is_valid=False
    enrollment_status_is_valid=False

    def __init__(self) -> None:
        self.create_the_window()
        self.set_title()
        self.set_appearance_mode()
        self.create_table()
        self.create_controls_frame()
        self.setup_info_frame()
        self.setup_buttons_frame()
        self.initialize_data_from_database()
        self.bind_functions()
        self.window.mainloop()


    def create_the_window(self):
        self.window = CTk.CTk()
        self.window.geometry(self.get_center_of_screen())
        self.window.columnconfigure(0,weight=1)
        self.window.maxsize(self.WIDTH,self.HEIGHT)   
        self.window.minsize(self.WIDTH*0.7,self.HEIGHT*0.7) 
    def set_title(self):
        self.window.title(self.TITLE)    
    def set_appearance_mode(self):
        CTk.set_appearance_mode(self.APPEARANCE_MODE)
    
    def create_table(self):
        self.table=ttk.Treeview(self.window, columns = self.columns,
            show = 'headings',height=20)
        self.create_heading_for_table()
        self.resize_columns()
        self.create_table_style()
        
            
        self.table.grid(row=0, column=0, padx=20, pady=20, sticky="wens")
    def create_heading_for_table(self):
        counter = 0
        for _ in self.columns:
            self.table.heading(self.columns[counter],text = self.headers[counter])
            counter+=1
    def create_table_style(self):
        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#333333", 
                fieldbackground="#333333",foreground="white")
        self.table_style = ttk.Style()
        self.table_style.configure("Treeview.Heading", background="lightblue", foreground="black")
    def resize_columns(self):
        self.table.column("id",width=80,stretch=False)
        self.table.column("Student_Name",width=300,stretch=False)
        self.table.column("Year",width=120,stretch=False)
        self.table.column("Enrollment_Status",width=120,stretch=False)
    def initialize_data_from_database(self):
        students = get_all_students()
        for student in students:
            student_id = str(student[0])
            Student_Name = str(student[1])
            Year = str(student[3])
            Course = str(student[2])
            Organization = str(student[6])
            Adviser = str(student[5])
            Enrollment_Status = str(student[4])
            data = (student_id,Student_Name,Year,Course,Organization,Adviser,Enrollment_Status)
            self.table.insert(parent='',index = CTk.END,values = data)
    
    def create_controls_frame(self):
        self.controls=CTk.CTkFrame(self.window,bg_color="transparent")
        self.controls.columnconfigure(0,weight=0,minsize=370)
        self.controls.columnconfigure(1,weight=1)
        self.controls.grid(row=1,column=0, padx=20, pady=(0,0), sticky="wens")

        self.info_frame=CTk.CTkFrame(self.controls)
        self.info_frame.columnconfigure(0,weight=0,minsize=200)
        self.info_frame.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.buttons_frame=CTk.CTkFrame(self.controls)
        self.buttons_frame.grid(row=0,column=1,padx=5,pady=5,sticky="nwe")

    def setup_info_frame(self):
 
        description_frame = CTk.CTkFrame(self.info_frame,bg_color="transparent",fg_color="transparent")
        description_frame.grid(row=0,column = 0,padx=5,sticky="nw")

        info_frame_label = CTk.CTkLabel(description_frame,text="STUDENT INFORMATION SECTION",
                                        font=(CTk.CTkFont("Arial",weight="bold")),fg_color="green",
                                        corner_radius=20,bg_color="transparent")
        info_frame_label.grid(row=0,column = 0,padx=(45,0),pady=(3,7),sticky="w")

        self.view_mode_toggler=CTk.CTkSwitch(self.info_frame,corner_radius=15, text="Edit Mode", command= self.toggle_info_frame)
        self.view_mode_toggler.grid(row=0,column=0,padx=(0,15),pady=(3,7),sticky="e")


        self.entry_frame = CTk.CTkFrame(self.info_frame,bg_color="transparent",fg_color="transparent")
        self.entry_frame.grid(row=1,column=0,padx=0,pady=(0,3),sticky="s")

        row=1
        self.column_label=0
        self.column_entry=1
        for header in self.headers:
            label = CTk.CTkLabel(self.entry_frame,text=header)
            label.grid(row=row,column=self.column_label,padx=5,sticky="w")
            row+=1
        
        self.create_student_entry()
        self.setup_infos_as_entry_for_view_mode()

    def create_student_entry(self):
        self.student_id = CTk.CTkEntry(self.entry_frame,width=350,state="disabled")
        self.student_id.grid(row=1,column=self.column_entry,padx=5,sticky="e")
        self.student_name = CTk.CTkEntry(self.entry_frame,width=350)
        self.student_name.grid(row=2,column=self.column_entry,padx=5,sticky="e")
        self.student_name.bind('<KeyPress>',lambda event: self.invalid_input_on_entry(event=event,Entry=self.student_name,name="name_is_valid"))
        
        
    def setup_infos_as_combobox_for_edit_mode(self):
        self.create_student_entry()
        self.year = CTk.CTkComboBox(self.entry_frame,width=350,values=self.year_dropdown)
        self.year.grid(row=3,column=self.column_entry,padx=5,sticky="e")
        self.year.bind('<KeyPress>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.year,dropdown=self.year_dropdown,name="year_is_valid"))
        self.year.bind('<ButtonRelease>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.year,dropdown=self.year_dropdown,name="year_is_valid"))
        
        self.course = CTk.CTkComboBox(self.entry_frame,width=350,values=self.course_dropdown)
        self.course.grid(row=4,column=self.column_entry,padx=5,sticky="e")
        self.course.bind('<KeyPress>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.course,dropdown=self.course_dropdown,name="course_is_valid"))
        self.course.bind('<ButtonRelease>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.course,dropdown=self.course_dropdown,name="course_is_valid"))
        
        self.organization = CTk.CTkComboBox(self.entry_frame,width=350,values=self.organization_dropdown)
        self.organization.grid(row=5,column=self.column_entry,padx=5,sticky="e")
        self.organization.bind('<KeyPress>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.organization,dropdown=self.organization_dropdown,name="organization_is_valid"))
        self.organization.bind('<ButtonRelease>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.organization,dropdown=self.organization_dropdown,name="organization_is_valid"))
        
        self.adviser = CTk.CTkComboBox(self.entry_frame,width=350, values=self.adviser_dropdown)
        self.adviser.grid(row=6,column=self.column_entry,padx=5,sticky="e")
        self.adviser.bind('<KeyPress>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.adviser,dropdown=self.adviser_dropdown,name="adviser_is_valid"))
        self.adviser.bind('<ButtonRelease>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.adviser,dropdown=self.adviser_dropdown,name="adviser_is_valid"))
         
        self.enrollment_status = CTk.CTkComboBox(self.entry_frame,width=350,values=self.enrollment_status_dropdown)
        self.enrollment_status.grid(row=7,column=self.column_entry,padx=5,sticky="e")
        self.enrollment_status.bind('<KeyPress>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.enrollment_status,dropdown=self.enrollment_status_dropdown,name="enrollment_status_is_valid"))
        self.enrollment_status.bind('<ButtonRelease>',lambda event: self.invalid_input_on_combobox(
            event=event,combobox=self.enrollment_status,dropdown=self.enrollment_status_dropdown,name="enrollment_status_is_valid"))


    def setup_infos_as_entry_for_view_mode(self):
        self.create_student_entry()
        self.year = CTk.CTkEntry(self.entry_frame,width=350)
        self.year.grid(row=3,column=self.column_entry,padx=5,sticky="e")
        
        self.course = CTk.CTkEntry(self.entry_frame,width=350)
        self.course.grid(row=4,column=self.column_entry,padx=5,sticky="e")
        
        self.organization = CTk.CTkEntry(self.entry_frame,width=350)
        self.organization.grid(row=5,column=self.column_entry,padx=5,sticky="e")
        
        self.adviser = CTk.CTkEntry(self.entry_frame,width=350)
        self.adviser.grid(row=6,column=self.column_entry,padx=5,sticky="e")
         
        self.enrollment_status = CTk.CTkEntry(self.entry_frame,width=350)
        self.enrollment_status.grid(row=7,column=self.column_entry,padx=5,sticky="e")

    def setup_buttons_frame(self):
        actual_buttons = CTk.CTkFrame(self.buttons_frame)
        actual_buttons.grid(row=0,column=0,sticky="nswe",padx=0,pady=0)
        self.new_button=CTk.CTkButton(actual_buttons,width=230,corner_radius=15,text="New Student",command=self.create_new_student)
        self.new_button.grid(row=0,column=0,pady=(10,10),padx=(5,0),sticky="w")
        self.save_button=CTk.CTkButton(actual_buttons,width=230,corner_radius=15,text="Save Changes", command=self.save_student)
        self.save_button.grid(row=0,column=1,pady=(10,10),padx=(15,15),sticky="we")
        self.delete_button=CTk.CTkButton(actual_buttons,width=230,corner_radius=15,text="Delete Student",command=self.delete_student_from_database)
        self.delete_button.grid(row=0,column=2,pady=(10,10),padx=(0,25),sticky="e")
        self.generate_button=CTk.CTkButton(actual_buttons,width=230,corner_radius=15,text="GENERATE RANDOM STUDENT",command=self.generate_random_student)
        self.generate_button.grid(row=1,column=0,pady=(10,10),padx=(5,0),sticky="w")
        self.exit_button=CTk.CTkButton(actual_buttons,width=230,corner_radius=15,text="EXIT", command=self.window.quit)
        self.exit_button.grid(row=1,column=1,pady=(10,10),padx=(15,15),sticky="ew")

        self.setup_instruction_section()
    def setup_instruction_section(self):
        instructions_frame=CTk.CTkFrame(self.buttons_frame)
        instructions_frame.grid(row=1)
        text = 'This project aims to create a relational database management system using SQLite3 and implement a user-friendly graphical user interface (GUI) using customtkinter. The application will consist of six distinct tables: users, advisers, courses, year, enrollment_status and organization. The use of a database will ensure efficient data storage and retrieval by avoiding repetition of strings. Simple Project by Denver James Duran.\n\
        \nNEW STUDENT: Add new data to the database. \n\
SAVE CHANGES: Update or save the modified data.\n\
DELETE STUDENT: Delete selected data from the database.\n\
To exit the application, click the "exit" button.\n'

        instructions = CTk.CTkLabel(instructions_frame,text=text,width=585,wraplength=700,text_color="grey")
        instructions.grid(row = 1,padx = 45,pady=5,sticky="w")
    def bind_functions(self):
        self.table.bind('<<TreeviewSelect>>', self.item_select)
        self.table.bind('<Double-1>', self.show_to_info_frame)


    def show_to_info_frame(self,data: any=None):
        selected_student = self.table.selection()
        student_details=self.table.item(selected_student)['values']
        # At first start of app, there are no selected student yet and  
        # the codes below will cause an index error
        
        try:
            if not self.reset_info_on_info_frame():
                self.student_id.configure(True,state="normal")
                self.student_id.insert(0,student_details[0])
                self.student_id.configure(True,state="disabled")
                self.student_name.insert(0,student_details[1])
                self.year.set(student_details[2])
                self.course.set(student_details[3])
                self.organization.set(student_details[4])
                self.adviser.set(student_details[5])
                self.enrollment_status.set(student_details[6])
                return
            self.student_id.configure(True,state="normal")
            self.student_id.insert(0,student_details[0])
            self.student_id.configure(True,state="disabled")
            self.student_name.insert(0,student_details[1])
            self.year.insert(0,student_details[2])
            self.course.insert(0,student_details[3])
            self.organization.insert(0,student_details[4])
            self.adviser.insert(0,student_details[5])
            self.enrollment_status.insert(0,student_details[6])
        except IndexError:
                pass
    def reset_info_on_info_frame(self):
        self.student_id.configure(True,state="normal")
        self.student_id.delete(0,END)
        self.student_id.configure(True,state="disabled")
        self.student_name.delete(0,END)

        if not self.is_in_View_Mode: 
            self.year.set(EMPTY_STRING)
            self.course.set(EMPTY_STRING)
            self.organization.set(EMPTY_STRING)
            self.adviser.set(EMPTY_STRING)
            self.enrollment_status.set(EMPTY_STRING)
            return False

        self.year.delete(0,END)
        self.course.delete(0,END)
        self.organization.delete(0,END)
        self.adviser.delete(0,END)
        self.enrollment_status.delete(0,END)
        return True
    def delete_widgets_on_info_frame(self):
        self.student_id.destroy()
        self.student_name.destroy()
        self.year.destroy()
        self.course.destroy()
        self.organization.destroy()
        self.adviser.destroy()
        self.enrollment_status.destroy()

    def item_select(self,_):
        self.reset_info_on_info_frame()
    
    def toggle_info_frame(self):      
        self.delete_widgets_on_info_frame()
        self.new_button.configure(fg_color="#1c6ca4")
        self.is_in_new_mode = False
        if self.is_in_View_Mode: 
            self.setup_infos_as_combobox_for_edit_mode()
            self.is_in_View_Mode = False
            self.show_to_info_frame()
        else: 
            self.setup_infos_as_entry_for_view_mode()
            self.is_in_View_Mode = True
            self.show_to_info_frame()

    def generate_random_student(self):
        first_names = ['Bob', 'Maria', 'Alex', 'James', 'Susan', 'Henry', 'Lisa', 'Anna', 'Lisa']
        last_names = ['Smith', 'Brown', 'Wilson', 'Thomson', 'Cook', 'Taylor', 'Walker', 'Clark']
        five=[1,2,3,4,5]
        four=[1,2,3,4]
                
        random_name = f'{choice(first_names)} {choice(last_names)}'
        random_year = choice(four)
        random_course = choice(five)
        random_organization = choice(five)
        random_adviser = choice(five)
        random_enrollment_Status = choice(four)
        self.add_student_to_database(Student_Name=random_name,
                Organization_id=random_organization,
                Enrollment_Status_id=random_enrollment_Status,
                Adviser_id=random_adviser,
                Course_id=random_course,
                Year_id = random_year)
    def get_info_from_info_frame(self) -> dict:
        student_id = self.student_id.get()
        student_name = self.student_name.get()
        year = self.year.get()
        course = self.course.get()
        organization = self.organization.get()
        adviser = self.adviser.get()
        enrollment_status = self.enrollment_status.get()
        return {"id":student_id,
                "Student_Name":student_name,
                "Year_id":self.year_dropdown.index(year)+1,
                "Course_id":self.course_dropdown.index(course)+1,
                "Organization_id":self.organization_dropdown.index(organization)+1,
                "Adviser_id":self.adviser_dropdown.index(adviser)+1,
                "Enrollment_status_id":self.enrollment_status_dropdown.index(enrollment_status)+1 }
    def create_new_student(self):
        if self.is_in_View_Mode:
            self.view_mode_toggler.toggle()
            self.is_in_View_Mode = False
            self.delete_widgets_on_info_frame()
            self.setup_infos_as_combobox_for_edit_mode()
        self.is_in_new_mode = True
        self.show_to_info_frame()
        self.reset_info_on_info_frame()
        self.new_button.configure(fg_color="green")
        self.student_id.configure(True,state="disabled")

    def save_student(self):

        input_is_valid=all([self.name_is_valid, 
            self.year_is_valid, 
            self.course_is_valid, 
            self.organization_is_valid, 
            self.adviser_is_valid, 
            self.enrollment_status_is_valid])

        
        if self.is_in_new_mode and input_is_valid:
            student_info=self.get_info_from_info_frame()
            student_info.pop("id")
            self.add_student_to_database(**student_info)
            self.reset_info_on_info_frame()
            self.toggle_info_frame()
            self.setup_infos_as_entry_for_view_mode()
        
        
    def add_student_to_database(self,**kwargs):
        create(table_name.students,
                **kwargs)
        # The area below is totally optional, much better way is to just reassign the values
        # instead of reading from the disk. But for the purpose of the project, 
        # we need to apply the CRUD

        student = read(table_name.students,-1,limit=limit.One)
        student_id = str(student[0])
        Student_Name = str(student[1])
        Year = str(student[3])
        Course = str(student[2])
        Organization = str(student[6])
        Adviser = str(student[5])
        Enrollment_Status = str(student[4])
        data = (student_id,Student_Name,Year,Course,Organization,Adviser,Enrollment_Status)
        self.table.insert(parent='',index = CTk.END,values = data)

    def delete_student_from_database(self):
        selected_student = self.table.selection()
        student_details=self.table.item(selected_student)['values']
        delete(table_name.students,student_details[0])
        self.table.delete(selected_student)

    def invalid_input_on_combobox(self,event,combobox: CTk.CTkComboBox,dropdown,name):
        match event.char:
            case '\x08':
                current = combobox.get()[:-1]
            case '??':
                current = combobox.get()
            case _:
                current = combobox.get() + str(event.char)
        if current in dropdown:
            self.set_border_color_to_green_if_acceptable(combobox,True,name)
            return
        self.set_border_color_to_green_if_acceptable(combobox,False,name)

    def invalid_input_on_entry(self,event,Entry:CTk.CTkEntry,name):

        if Entry.get().replace(" ",'').isalpha() == EMPTY_STRING and event.char.isalpha():
            self.set_border_color_to_green_if_acceptable(Entry,True,name)

        elif Entry.get().replace(" ",'').isalpha() and event.char.isalpha(): 
            self.set_border_color_to_green_if_acceptable(Entry,True,name)

        elif Entry.get()[:-1].replace(" ",'').isalpha() and (event.char == '\x08' or event.char == '\t'):
            self.set_border_color_to_green_if_acceptable(Entry,True,name)

        else:self.set_border_color_to_green_if_acceptable(Entry,False,name)

    def set_border_color_to_green_if_acceptable(self,Object,valid: bool,name):
        if valid:
            Object.configure(True,border_color='green')
            setattr(self,name,True)
        else: 
            Object.configure(True,border_color='red')
            setattr(self,name,False)

    def get_center_of_screen(self,window = None, width = None,height = None,X_OFFSET=0,Y_OFFSET=-100) -> str:

        if window is None: 
            window = self.window
        
        if width is None:
            width = self.WIDTH

        if height is None:
            height=self.HEIGHT

        self.screen_width = window.winfo_screenwidth()//2
        self.screen_height = window.winfo_screenheight()//2
        x = (self.screen_width - (self.WIDTH // 2)) + X_OFFSET
        y = (self.screen_height - (self.HEIGHT // 2)) + Y_OFFSET

        return f'{width}x{height}+{x}+{y}'
    
if __name__ == "__main__":
    main_window()