import customtkinter as CTk
import tkinter as stk

from tkinter import ttk
from dataclasses import dataclass
from typing import Optional,Union

from queries import create,read,update,delete,get_all_students,get_data_for_dropdown
from utils import limit,table_name

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
    buttons_frame: Optional[CTk.CTkFrame] = None

    student_id: Optional[CTk.CTkEntry] = None
    student_name: Optional[CTk.CTkEntry] = None
    year: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    course: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    organization: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    adviser: Union[CTk.CTkComboBox,CTk.CTkEntry] = None
    enrollment_status: Union[CTk.CTkComboBox,CTk.CTkEntry] = None


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
        self.controls.columnconfigure(0,weight=0,minsize=585)
        self.controls.columnconfigure(1,weight=0,minsize=585)
        self.controls.grid(row=1,column=0, padx=20, pady=(0,0), sticky="wens")

        self.info_frame=CTk.CTkFrame(self.controls)
        self.info_frame.columnconfigure(0,weight=0,minsize=200)
        self.info_frame.grid(row=0,column=0,padx=5,pady=5,sticky="w")
        self.buttons_frame=CTk.CTkFrame(self.controls)
        self.buttons_frame.grid(row=0,column=1,padx=5,pady=5,sticky="e")
    def setup_info_frame(self):
 
        description_frame = CTk.CTkFrame(self.info_frame,bg_color="transparent",fg_color="transparent")
        description_frame.grid(row=0,padx=5,sticky="n")
        info_frame_label = CTk.CTkLabel(description_frame,text="STUDENT INFORMATION SECTION",
                                        font=(CTk.CTkFont("Arial",weight="bold")),fg_color="green",
                                        corner_radius=20,bg_color="transparent")
        info_frame_label.grid(row=0,padx=0,pady=(3,7),sticky="n")
        
        self.entry_frame = CTk.CTkFrame(self.info_frame,bg_color="transparent",fg_color="transparent")
        self.entry_frame.grid(row=1,padx=0,pady=(0,3),sticky="s")

        row=1
        self.column_label=0
        self.column_entry=1
        for header in self.headers:
            label = CTk.CTkLabel(self.entry_frame,text=header)
            label.grid(row=row,column=self.column_label,padx=5,sticky="w")
            row+=1
        self.student_id = CTk.CTkEntry(self.entry_frame,width=350)
        self.student_id.grid(row=1,column=self.column_entry,padx=5,sticky="e")

        self.student_name = CTk.CTkEntry(self.entry_frame,width=350)
        self.student_name.grid(row=2,column=self.column_entry,padx=5,sticky="e")
        self.setup_infos_as_entry_for_view_mode()

    def setup_infos_as_combobox_for_edit_mode(self):
        self.year = CTk.CTkComboBox(self.entry_frame,width=350,values=get_data_for_dropdown('year'))
        self.year.grid(row=3,column=self.column_entry,padx=5,sticky="e")
        
        self.course = CTk.CTkComboBox(self.entry_frame,width=350,values=get_data_for_dropdown('courses'))
        self.course.grid(row=4,column=self.column_entry,padx=5,sticky="e")
        
        self.organization = CTk.CTkComboBox(self.entry_frame,width=350,values=get_data_for_dropdown('organization'))
        self.organization.grid(row=5,column=self.column_entry,padx=5,sticky="e")
        
        self.adviser = CTk.CTkComboBox(self.entry_frame,width=350, values=get_data_for_dropdown('advisers'))
        self.adviser.grid(row=6,column=self.column_entry,padx=5,sticky="e")
         
        self.enrollment_status = CTk.CTkComboBox(self.entry_frame,width=350,values=get_data_for_dropdown('enrollment_status'))
        self.enrollment_status.grid(row=7,column=self.column_entry,padx=5,sticky="e")

    def setup_infos_as_entry_for_view_mode(self):
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

        test_button=CTk.CTkButton(self.buttons_frame,610,text="SAMPLE BUTTON ", command= self.toggle_info_frame)
        test_button.grid(row=0,column=0,padx=0,pady=0,sticky="we")
    
    def bind_functions(self):
        self.table.bind('<<TreeviewSelect>>', self.item_select)
        self.table.bind('<Double-1>', self.show_to_info_frame)
    
    def show_to_info_frame(self,data):
        selected_student = self.table.selection()
        student_details=self.table.item(selected_student)['values']

        if not self.reset_info_on_info_frame(): return
        self.student_id.insert(0,student_details[0])
        self.student_name.insert(0,student_details[1])
        self.year.insert(0,student_details[2])
        self.course.insert(0,student_details[3])
        self.organization.insert(0,student_details[4])
        self.adviser.insert(0,student_details[5])
        self.enrollment_status.insert(0,student_details[6])

    def reset_info_on_info_frame(self):
        if not self.check_if_info_form_mode_is_entry(): return False
        self.student_id.delete(0,"end")
        self.student_name.delete(0,"end")
        self.year.delete(0,"end")
        self.course.delete(0,"end")
        self.organization.delete(0,"end")
        self.adviser.delete(0,"end")
        self.enrollment_status.delete(0,"end")
        return True

    def delete_widgets_on_info_frame(self):
        self.year.destroy()
        self.course.destroy()
        self.organization.destroy()
        self.adviser.destroy()
        self.enrollment_status.destroy()

    def item_select(self,_):
        self.reset_info_on_info_frame()
    
    def check_if_info_form_mode_is_entry(self):
        return isinstance(self.year,CTk.CTkEntry)
    def toggle_info_frame(self):
        isEntry=self.check_if_info_form_mode_is_entry()

        self.delete_widgets_on_info_frame()
        if isEntry: self.setup_infos_as_combobox_for_edit_mode()
        else: self.setup_infos_as_entry_for_view_mode()

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
    
main_window()