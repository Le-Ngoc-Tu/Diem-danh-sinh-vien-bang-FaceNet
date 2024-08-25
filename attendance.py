# import re
import re
from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
import csv
from tkinter import filedialog
import pandas as pd
#Global variable for importCsv Function 
mydata=[]
class Attendance:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Attendance Pannel")
        self.last_MaSv = None
        self.last_time = None

        #-----------Thuộc tính cần lưu trữ-------------------
        self.masv=StringVar()
        self.tensv=StringVar()
        self.var_time=StringVar()
        self.var_date=StringVar()
        self.var_attend=StringVar()
        self.khoa=StringVar()
        self.lop=StringVar()
        # This part is image labels setting start 
        # first header image  
        img=Image.open(r"Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r"Images_GUI\bg4.png")
        bg1=bg1.resize((1366,768),Image.ANTIALIAS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Bảng điểm danh",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        #========================Section Creating==================================

        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_frame.place(x=5,y=55,width=1355,height=570)

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Thông tin học sinh",font=("verdana",12,"bold"),fg="navyblue")
        left_frame.place(x=10,y=10,width=660,height=540)
        
        # ==================================Text boxes and Combo Boxes====================
        #Mã sinh viên
        studentId_label = Label(left_frame,text="Mã sinh viên:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        studentId_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        studentId_entry = ttk.Entry(left_frame,textvariable=self.masv,width=15,font=("verdana",12,"bold"))
        studentId_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        #Tên sinh viên
        student_name_label = Label(left_frame,text="Họ tên:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_name_label.grid(row=1,column=0,padx=5,pady=5,sticky=W)

        student_name_entry = ttk.Entry(left_frame,textvariable=self.tensv,width=15,font=("verdana",12,"bold"))
        student_name_entry.grid(row=1,column=1,padx=5,pady=5,sticky=W)
        #time
        time_label = Label(left_frame,text="Thời gian:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        time_label.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        time_entry = ttk.Entry(left_frame,textvariable=self.var_time,width=15,font=("verdana",12,"bold"))
        time_entry.grid(row=1,column=3,padx=5,pady=5,sticky=W)

        #Date 
        date_label = Label(left_frame,text="Ngày:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        date_label.grid(row=2,column=0,padx=5,pady=5,sticky=W)

        date_entry = ttk.Entry(left_frame,textvariable=self.var_date,width=15,font=("verdana",12,"bold"))
        date_entry.grid(row=2,column=1,padx=5,pady=5,sticky=W)
        #Attendance
        student_attend_label = Label(left_frame,text="Trạng thái:",font=("verdana",12,"bold"),fg="navyblue",bg="white")
        student_attend_label.grid(row=2,column=2,padx=5,pady=5,sticky=W)

        attend_combo=ttk.Combobox(left_frame,textvariable=self.var_attend,width=13,font=("verdana",12,"bold"),state="readonly")
        attend_combo["values"]=("Status","present","Absent")
        attend_combo.current(0)
        attend_combo.grid(row=2,column=3,padx=5,pady=5,sticky=W)

        # ===============================Table Sql Data View==========================
        table_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=100,width=635,height=310)

        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #create table
        self.attendanceReport_left = ttk.Treeview(table_frame,column=("MaSv","TenSV","Time","Date","Attend"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.attendanceReport_left.xview)
        scroll_y.config(command=self.attendanceReport_left.yview)

        self.attendanceReport_left.heading("MaSv",text="Mã sinh viên")
        self.attendanceReport_left.heading("TenSV",text="Họ tên")
        self.attendanceReport_left.heading("Time",text="Thời gian")
        self.attendanceReport_left.heading("Date",text="Ngày")
        self.attendanceReport_left.heading("Attend",text="Trạng thái")
        self.attendanceReport_left["show"]="headings"
        # Set Width of Colums 
        self.attendanceReport_left.column("MaSv",width=100)
        self.attendanceReport_left.column("TenSV",width=100)
        self.attendanceReport_left.column("Time",width=100)
        self.attendanceReport_left.column("Date",width=100)
        self.attendanceReport_left.column("Attend",width=100)
        
        self.attendanceReport_left.pack(fill=BOTH,expand=1)
        self.attendanceReport_left.bind("<ButtonRelease>",self.get_cursor_left)
        # =========================button section========================

        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=390,width=635,height=120)

        #Improt button
        save_btn=Button(btn_frame,command=self.importCsv,text="Thêm CSV",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        save_btn.grid(row=0,column=0,padx=6,pady=10,sticky=W)

        #Exprot button
        export_btn=Button(btn_frame,command=self.exportCsv,text="Xuất CSV",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        export_btn.grid(row=0,column=1,padx=6,pady=8,sticky=W)
        #Exprot button
        export_btn=Button(btn_frame,command=self.exportCsv_Khoa,text="Xuất Theo Khoa",width=13,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        export_btn.grid(row=1,column=0,padx=6,pady=8,sticky=W)
        #Exprot button
        export_btn=Button(btn_frame,command=self.exportCsv_Lop,text="Xuất Theo Lớp",width=13,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        export_btn.grid(row=1,column=1,padx=6,pady=8,sticky=W)
        #Update button
        del_btn=Button(btn_frame,command=self.action,text="Lưu",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=2,padx=6,pady=10,sticky=W)

        #reset button
        reset_btn=Button(btn_frame,command=self.reset_data,text="Làm mới",width=12,font=("verdana",12,"bold"),fg="white",bg="navyblue")
        reset_btn.grid(row=0,column=3,padx=6,pady=10,sticky=W)

        # Right section=======================================================
        # Phần bên phải =======================================================
        
        # Khung nhãn bên phải
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Thông tin điểm danh học sinh", font=("verdana", 12, "bold"), fg="navyblue")
        right_frame.place(x=680, y=10, width=660, height=480)
        
        # ----------------------------- Khung bảng -------------------------------------------------
        # Khung bảng 
        # Hệ thống tìm kiếm trong khung nhãn bên phải 
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=10, y=90, width=635, height=360)
        
        # Thanh cuộn 
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
        
        # Tạo bảng
        self.attendanceReport = ttk.Treeview(table_frame, column=("MaSv", "TenSV", "Time", "Date", "Attend","MaKhoa","MaLop"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.attendanceReport.xview)
        scroll_y.config(command=self.attendanceReport.yview)
        
        self.attendanceReport.heading("MaSv", text="Mã sinh viên")
        self.attendanceReport.heading("TenSV", text="Họ tên")
        self.attendanceReport.heading("Time", text="Thời gian")
        self.attendanceReport.heading("Date", text="Ngày")
        self.attendanceReport.heading("Attend", text="Trạng thái")
        self.attendanceReport.heading("MaKhoa", text="Khoa")
        self.attendanceReport.heading("MaLop", text="Lớp")
        self.attendanceReport["show"] = "headings"
        # Đặt chiều rộng cho cột 
        self.attendanceReport.column("MaSv", width=100)
        self.attendanceReport.column("TenSV", width=100)
        self.attendanceReport.column("Time", width=100)
        self.attendanceReport.column("Date", width=100)
        self.attendanceReport.column("Attend", width=100)
        self.attendanceReport.column("MaKhoa", width=100)
        self.attendanceReport.column("MaLop", width=100)
        self.attendanceReport.pack(fill=BOTH, expand=1)
        self.attendanceReport.bind("<ButtonRelease>", self.get_cursor_right)
        self.fetch_data()
    # =================================update for mysql button================
    #Update button
        update_btn = Button(right_frame, command=self.update_data, text="Sửa", width=12, font=("verdana", 12, "bold"), fg="white", bg="navyblue")
        update_btn.grid(row=0, column=1, padx=6, pady=10, sticky=W)
    #Delete button
        delete_btn = Button(right_frame, command=self.delete_data, text="Xóa", width=12, font=("verdana", 12, "bold"), fg="white", bg="navyblue")
        delete_btn.grid(row=0, column=2, padx=6, pady=10, sticky=W)
    #combo box 
        khoa_combo=ttk.Combobox(right_frame,textvariable=self.khoa,width=20,font=("Times New Roman",12,"bold"),state="readonly")
        khoa_combo["values"]=("Công Nghệ Thông Tin","Khoa Ngoại Ngữ")
        khoa_combo.current(0)
        khoa_combo.grid(row=1,column=1,padx=5,pady=5,sticky=W)
    #combo box 
        lop_combo=ttk.Combobox(right_frame,textvariable=self.lop,width=20,font=("Times New Roman",12,"bold"),state="readonly")
        lop_combo["values"]=("K13THO1","K14THO1")
        lop_combo.current(0)
        lop_combo.grid(row=1,column=2,padx=5,pady=5,sticky=W)
    # ===============================update function for mysql database=================
    def update_data(self):
        if self.masv.get() =="" or self.tensv.get() =="" or self.var_time.get() == "" or self.var_date.get() == "" or self.var_attend.get() == "Status":
            messagebox.showerror("Error","Hãy nhập đầy đủ thông tin!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muốn cập nhật dữ liệu điểm danh của danh sách sinh viên này không!",parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                    mycursor = conn.cursor()
                    mycursor.execute("update stdattendance set time=%s,std_date=%s,attendance=%s where MaSv=%s",( 
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attend.get(),
                    self.masv.get()
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Cập nhật thành công!",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    # =============================Delete Attendance form my sql============================
    def delete_data(self):
        try:
                # Hiển thị cảnh báo xác nhận trước khi xóa
                delete = messagebox.askyesno("Delete", "Bạn có muốn xóa tất cả dữ liệu không?", parent=self.root)

                if delete > 0:
                    # Mở kết nối đến cơ sở dữ liệu
                    conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
                    mycursor = conn.cursor()

                    # Thực hiện xóa tất cả dữ liệu
                    mycursor.execute("DELETE FROM stdattendance")

                    # Commit và đóng kết nối
                    conn.commit()
                    conn.close()

                    # Cập nhật lại Treeview
                    self.fetch_data()

                    messagebox.showinfo("Delete", "Tất cả dữ liệu đã được xóa thành công!", parent=self.root)

        except Exception as es:
                messagebox.showerror("Error", f"Đã xảy ra lỗi: {str(es)}", parent=self.root) 
    # ===========================fatch data form mysql attendance===========
    
    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
        mycursor = conn.cursor()

        mycursor.execute("SELECT stdattendance.MaSv,sinhvien.TenSV,stdattendance.time,stdattendance.std_date,stdattendance.attendance, khoa.TenKhoa, lop.MaLop FROM stdattendance INNER JOIN sinhvien on stdattendance.MaSv = sinhvien.MaSv INNER JOIN khoa ON sinhvien.MaKhoa = khoa.MaKhoa INNER JOIN lop ON sinhvien.MaLop = lop.MaLop")
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.attendanceReport.delete(*self.attendanceReport.get_children())
            for i in data:
                self.attendanceReport.insert("",END,values=i)
            conn.commit()
        conn.close()

    #============================Reset Data======================
    def reset_data(self):
        self.masv.set("")
        self.tensv.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attend.set("Status")

    # =========================Fetch Data Import data ===============

    def fetchData(self,rows):
        global mydata
        mydata = rows
        self.attendanceReport_left.delete(*self.attendanceReport_left.get_children())
        for i in rows:
            self.attendanceReport_left.insert("",END,values=i)
            print(i)
        
    def importCsv(self):
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*.csv"),("All File","*.*")),parent=self.root)
        with open(fln, encoding='ISO-8859-1') as myfile:
            csvread=csv.reader(myfile,delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in csvread:
                mydata.append(i)
        self.fetchData(mydata)
            

    #==================Experot CSV=============
    def exportCsv(self):
        try:
            # Yêu cầu người dùng chọn nơi lưu file .csv
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)

            # Kiểm tra xem người dùng đã chọn một file hay không
            if not fln:
                return False

            # Mở kết nối đến cơ sở dữ liệu
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            mycursor = conn.cursor()

            # Thực hiện truy vấn để lấy dữ liệu từ bảng stdattendance
            mycursor.execute("SELECT stdattendance.MaSv,sinhvien.TenSV,stdattendance.time,stdattendance.std_date,stdattendance.attendance, khoa.TenKhoa, lop.MaLop FROM stdattendance INNER JOIN sinhvien on stdattendance.MaSv = sinhvien.MaSv INNER JOIN khoa ON sinhvien.MaKhoa = khoa.MaKhoa INNER JOIN lop ON sinhvien.MaLop = lop.MaLop")

            # Lấy dữ liệu từ kết quả truy vấn
            rows = mycursor.fetchall()

            # Đóng kết nối
            conn.close()

            # Ghi dữ liệu vào file .csv
            with open(fln, mode="w", newline="", encoding="utf-8-sig") as myfile:
                exp_write = csv.writer(myfile, delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Viết header
                exp_write.writerow(["Mã sinh viên", "Tên sinh viên", "Thời gian vào", "Ngày", "Trạng thái","Khoa","Lớp" ,"Thời gian ra"])

                current_student_id = ""
                current_attendance_status = ""
                current_time_out = ""

                for i, row in enumerate(rows):
                    if row[0] and row[1] and row[2] and row[3] and row[4] != "Status" and row[5] and row[6]:
                        if row[0] != current_student_id:
                            # Ghi dòng trước của sinh viên trước đó
                            if current_student_id:
                                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])

                            # Cập nhật giá trị cho sinh viên mới
                            current_student_id = row[0]
                            current_student_name = row[1]
                            current_time_in = row[2]
                            current_date = row[3]
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_khoa=row[5]
                            current_lop=row[6]
                            current_time_out = row[2]

                        else:
                            # Nếu MaSv trùng với dữ liệu trước đó, cập nhật giá trị "Absent" cho cột "Trạng thái"
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_time_out = row[2] if i > 0 and rows[i - 1][0] == row[0] else ""

                # Ghi dòng cuối cùng
                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])
            # # Mở kết nối đến cơ sở dữ liệu
            # conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            # mycursor = conn.cursor()

            # # Thực hiện xóa tất cả dữ liệu
            # mycursor.execute("DELETE FROM stdattendance")

            # # Commit và đóng kết nối
            # conn.commit()
            # conn.close()

            # # Cập nhật lại Treeview
            # self.fetch_data()
            messagebox.showinfo("Thành công", "Xuất dữ liệu thành công!")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Do lỗi: {str(es)}", parent=self.root)
    def exportCsv_Khoa(self):
        try:
            # Lấy giá trị đã chọn từ lop_combo
            selected_khoa = self.khoa.get()
            # Kiểm tra xem đã chọn lớp hay chưa
            if not selected_khoa:
                messagebox.showerror("Lỗi", "Hãy chọn một lớp!", parent=self.root)
                return

            # Tạo tên file với định dạng .csv
            file_name_khoa = f"{selected_khoa}_attendance.csv"
            # Yêu cầu người dùng chọn nơi lưu file .csv
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")),defaultextension=".csv", initialfile=file_name_khoa, parent=self.root)

            # Kiểm tra xem người dùng đã chọn một file hay không
            if not fln:
                return False
            # Mở kết nối đến cơ sở dữ liệu
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            mycursor = conn.cursor()

            # Thực hiện truy vấn để lấy dữ liệu từ bảng stdattendance
            mycursor.execute("SELECT stdattendance.MaSv,sinhvien.TenSV,stdattendance.time,stdattendance.std_date,stdattendance.attendance, khoa.TenKhoa, lop.MaLop FROM stdattendance INNER JOIN sinhvien on stdattendance.MaSv = sinhvien.MaSv INNER JOIN khoa ON sinhvien.MaKhoa = khoa.MaKhoa INNER JOIN lop ON sinhvien.MaLop = lop.MaLop WHERE khoa.TenKhoa = %s",(selected_khoa,))

            # Lấy dữ liệu từ kết quả truy vấn
            rows = mycursor.fetchall()

            # Đóng kết nối
            conn.close()

            # Ghi dữ liệu vào file .csv
            with open(fln, mode="w", newline="", encoding="utf-8-sig") as myfile:
                exp_write = csv.writer(myfile, delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Viết header
                exp_write.writerow(["Mã sinh viên", "Tên sinh viên", "Thời gian vào", "Ngày", "Trạng thái","Khoa","Lớp" ,"Thời gian ra"])

                current_student_id = ""
                current_attendance_status = ""
                current_time_out = ""

                for i, row in enumerate(rows):
                    if row[0] and row[1] and row[2] and row[3] and row[4] != "Status" and row[5] and row[6]:
                        if row[0] != current_student_id:
                            # Ghi dòng trước của sinh viên trước đó
                            if current_student_id:
                                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])

                            # Cập nhật giá trị cho sinh viên mới
                            current_student_id = row[0]
                            current_student_name = row[1]
                            current_time_in = row[2]
                            current_date = row[3]
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_khoa=row[5]
                            current_lop=row[6]
                            current_time_out = row[2]

                        else:
                            # Nếu MaSv trùng với dữ liệu trước đó, cập nhật giá trị "Absent" cho cột "Trạng thái"
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_time_out = row[2] if i > 0 and rows[i - 1][0] == row[0] else ""

                # Ghi dòng cuối cùng
                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])
            # # Mở kết nối đến cơ sở dữ liệu
            # conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            # mycursor = conn.cursor()

            # # Thực hiện xóa tất cả dữ liệu
            # mycursor.execute("DELETE FROM stdattendance")

            # # Commit và đóng kết nối
            # conn.commit()
            # conn.close()

            # # Cập nhật lại Treeview
            # self.fetch_data()
            messagebox.showinfo("Thành công", "Xuất dữ liệu thành công!")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Do lỗi: {str(es)}", parent=self.root)
    def exportCsv_Lop(self):
        try:
            # Lấy giá trị đã chọn từ lop_combo
            selected_lop = self.lop.get()
            # Kiểm tra xem đã chọn lớp hay chưa
            if not selected_lop:
                messagebox.showerror("Lỗi", "Hãy chọn một lớp!", parent=self.root)
                return

            # Tạo tên file với định dạng .csv
            file_name = f"{selected_lop}_attendance.csv"
            # Yêu cầu người dùng chọn nơi lưu file .csv
            fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save CSV", filetypes=(("CSV File", "*.csv"), ("All File", "*.*")), defaultextension=".csv", initialfile=file_name, parent=self.root)

            # Kiểm tra xem người dùng đã chọn một file hay không
            if not fln:
                return False
            # Lấy giá trị đã chọn từ khoa_combo
            # Mở kết nối đến cơ sở dữ liệu
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            mycursor = conn.cursor()

            # Thực hiện truy vấn để lấy dữ liệu từ bảng stdattendance
            mycursor.execute("SELECT stdattendance.MaSv,sinhvien.TenSV,stdattendance.time,stdattendance.std_date,stdattendance.attendance, khoa.TenKhoa, lop.MaLop FROM stdattendance INNER JOIN sinhvien on stdattendance.MaSv = sinhvien.MaSv INNER JOIN khoa ON sinhvien.MaKhoa = khoa.MaKhoa INNER JOIN lop ON sinhvien.MaLop = lop.MaLop WHERE lop.MaLop = %s",(selected_lop,))

            # Lấy dữ liệu từ kết quả truy vấn
            rows = mycursor.fetchall()

            # Đóng kết nối
            conn.close()

            # Ghi dữ liệu vào file .csv
            with open(fln, mode="w", newline="", encoding="utf-8-sig") as myfile:
                exp_write = csv.writer(myfile, delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Viết header
                exp_write.writerow(["Mã sinh viên", "Tên sinh viên", "Thời gian vào", "Ngày", "Trạng thái","Khoa","Lớp" ,"Thời gian ra"])

                current_student_id = ""
                current_attendance_status = ""
                current_time_out = ""

                for i, row in enumerate(rows):
                    if row[0] and row[1] and row[2] and row[3] and row[4] != "Status" and row[5] and row[6]:
                        if row[0] != current_student_id:
                            # Ghi dòng trước của sinh viên trước đó
                            if current_student_id:
                                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])

                            # Cập nhật giá trị cho sinh viên mới
                            current_student_id = row[0]
                            current_student_name = row[1]
                            current_time_in = row[2]
                            current_date = row[3]
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_khoa=row[5]
                            current_lop=row[6]
                            current_time_out = row[2]

                        else:
                            # Nếu MaSv trùng với dữ liệu trước đó, cập nhật giá trị "Absent" cho cột "Trạng thái"
                            current_attendance_status = "Absent" if row[4] == "Absent" else "Present"
                            current_time_out = row[2] if i > 0 and rows[i - 1][0] == row[0] else ""

                # Ghi dòng cuối cùng
                exp_write.writerow([current_student_id, current_student_name, current_time_in, current_date, current_attendance_status,current_khoa,current_lop, current_time_out])
            # # Mở kết nối đến cơ sở dữ liệu
            # conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            # mycursor = conn.cursor()

            # # Thực hiện xóa tất cả dữ liệu
            # mycursor.execute("DELETE FROM stdattendance")

            # # Commit và đóng kết nối
            # conn.commit()
            # conn.close()

            # # Cập nhật lại Treeview
            # self.fetch_data()
            messagebox.showinfo("Thành công", "Xuất dữ liệu thành công!")
        except Exception as es:
            messagebox.showerror("Lỗi", f"Do lỗi: {str(es)}", parent=self.root)
    #=============Cursur Function for CSV========================

    def get_cursor_left(self,event=""):
        cursor_focus = self.attendanceReport_left.focus()
        content = self.attendanceReport_left.item(cursor_focus)
        data = content["values"]

        self.masv.set(data[0]),
        self.tensv.set(data[1]),
        self.var_time.set(data[2]),
        self.var_date.set(data[3]),
        self.var_attend.set(data[4])

    #=============Cursur Function for mysql========================

    def get_cursor_right(self,event=""):
        cursor_focus = self.attendanceReport.focus()
        content = self.attendanceReport.item(cursor_focus)
        data = content["values"]

        self.masv.set(data[0]),
        self.tensv.set(data[1]),
        self.var_time.set(data[2]),
        self.var_date.set(data[3]),
        self.var_attend.set(data[4])  

    #=========================================Action CSV============================
    # export Action
    def action(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="DiemDanhSinhVien")
            mycursor = conn.cursor()

            # Lấy dữ liệu từ Treeview attendanceReport_left
            rows = []
            for child in self.attendanceReport_left.get_children():
                row = self.attendanceReport_left.item(child)['values']
                rows.append(row)

            for row in rows:
                if row[0] and row[1] and row[2] and row[3] and row[4] != "Status":
                    # Kiểm tra xem MaSv đã tồn tại trong cơ sở dữ liệu hay chưa
                    mycursor.execute("SELECT * FROM stdattendance WHERE MaSv = %s", (row[0],))
                    result = mycursor.fetchall()

                    if len(result) >= 2:
                        # Trường hợp đã tồn tại nhiều hơn hoặc bằng 2 dữ liệu, thay thế dòng cuối cùng
                        mycursor.execute("DELETE FROM stdattendance WHERE MaSv = %s AND Time = %s AND std_date = %s AND attendance = %s",
                                        (result[-1][0], result[-1][2], result[-1][3], result[-1][4]))

                    # Lưu dòng dữ liệu vào cơ sở dữ liệu
                    mycursor.execute("INSERT INTO stdattendance (MaSv, TenSV, time, std_date, attendance) VALUES (%s, %s, %s, %s, %s)",
                                    (row[0], row[1], row[2], row[3], row[4]))

            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Tất cả dữ liệu đã được lưu!", parent=self.root)

        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)



