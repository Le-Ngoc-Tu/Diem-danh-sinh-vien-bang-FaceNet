from tkinter import* 
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import time
import os
# Testing Connection 
"""
conn = mysql.connector.connect(host="localhost",user="root",password="",database="face_recognition")
cursor = conn.cursor()

cursor.execute("show databases")

data = cursor.fetchall()

print(data)

conn.close()
"""
class Student:
    def __init__(self,root):
        # Khởi tạo giao diện
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Quản lí sinh viên")

        #-----------Các thuộc tính của sinh viên-------------------
        self.masv = StringVar()
        self.tensv = StringVar()
        self.ngaysinh = StringVar()
        self.gioitinh = StringVar()
        self.email = StringVar()
        self.sodienthoai = StringVar()
        self.diachi = StringVar()
        self.Khoa = StringVar()
        self.Lop = StringVar()
        # This part is image labels setting start 
        # first header image  
        img=Image.open(r"Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

         # backgorund image 
        bg1=Image.open(r"Images_GUI\bg3.jpg")
        bg1=bg1.resize((1366,768),Image.ANTIALIAS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Quản Lí Sinh Viên",font=("Times New Roman",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Creating Frame 
        main_frame = Frame(bg_img,bd=2,bg="white") #bd mean border 
        main_frame.place(x=5,y=55,width=1355,height=510)

        # Left Label Frame 
        left_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Thông tin sinh viên",font=("Times New Roman",12,"bold"),fg="navyblue")
        left_frame.place(x=10,y=10,width=660,height=480)
        #Class Student Information
        class_Student_frame = LabelFrame(left_frame,bd=2,bg="white",relief=RIDGE,text="Thông tin sinh viên",font=("Times New Roman",12,"bold"),fg="navyblue")
        class_Student_frame.place(x=10,y=10,width=635,height=300)
        #Mã sinh viên
        studentId_label = Label(class_Student_frame,text="Mã sinh viên:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        studentId_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)

        studentId_entry = ttk.Entry(class_Student_frame,textvariable=self.masv,width=15,font=("Times New Roman",12,"bold"))
        studentId_entry.grid(row=0,column=1,padx=5,pady=5,sticky=W)
        #Tên sinh viên
        student_name_label = Label(class_Student_frame,text="Tên sinh viên:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_name_label.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        student_name_entry = ttk.Entry(class_Student_frame,textvariable=self.tensv,width=15,font=("Times New Roman",12,"bold"))
        student_name_entry.grid(row=0,column=3,padx=5,pady=5,sticky=W)
        #Giới tính
        student_gender_label = Label(class_Student_frame,text="Giới tính:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_gender_label.grid(row=2,column=0,padx=5,pady=5,sticky=W)
        #combo box 
        gender_combo=ttk.Combobox(class_Student_frame,textvariable=self.gioitinh,width=13,font=("Times New Roman",12,"bold"),state="readonly")
        gender_combo["values"]=("Nam","Nữ")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=5,pady=5,sticky=W)
        #Ngày sinh
        student_dob_label = Label(class_Student_frame,text="Ngày sinh:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_dob_label.grid(row=2,column=2,padx=5,pady=5,sticky=W)

        student_dob_entry = ttk.Entry(class_Student_frame,textvariable=self.ngaysinh,width=15,font=("Times New Roman",12,"bold"))
        student_dob_entry.grid(row=2,column=3,padx=5,pady=5,sticky=W)
        #Email
        student_email_label = Label(class_Student_frame,text="Email:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_email_label.grid(row=3,column=0,padx=5,pady=5,sticky=W)

        student_email_entry = ttk.Entry(class_Student_frame,textvariable=self.email,width=15,font=("Times New Roman",12,"bold"))
        student_email_entry.grid(row=3,column=1,padx=5,pady=5,sticky=W)
        #Số điện thoại
        student_mob_label = Label(class_Student_frame,text="Số điện thoại:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_mob_label.grid(row=3,column=2,padx=5,pady=5,sticky=W)

        student_mob_entry = ttk.Entry(class_Student_frame,textvariable=self.sodienthoai,width=15,font=("Times New Roman",12,"bold"))
        student_mob_entry.grid(row=3,column=3,padx=5,pady=5,sticky=W)
        #Địa chỉ
        student_address_label = Label(class_Student_frame,text="Địa chỉ:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_address_label.grid(row=4,column=0,padx=5,pady=5,sticky=W)

        student_address_entry = ttk.Entry(class_Student_frame,textvariable=self.diachi,width=15,font=("Times New Roman",12,"bold"))
        student_address_entry.grid(row=4,column=1,padx=5,pady=5,sticky=W)
        #Chọn Khoa
        student_khoa_label = Label(class_Student_frame,text="Khoa:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_khoa_label.grid(row=4,column=2,padx=5,pady=5,sticky=W)

        #combo box 
        khoa_combo=ttk.Combobox(class_Student_frame,textvariable=self.Khoa,width=13,font=("Times New Roman",12,"bold"),state="readonly")
        khoa_combo["values"]=("Công Nghệ Thông Tin","Khoa Ngoại Ngữ")
        khoa_combo.current(0)
        khoa_combo.grid(row=4,column=3,padx=5,pady=5,sticky=W)
        #Chọn Lớp
        student_class_label = Label(class_Student_frame,text="Lớp:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        student_class_label.grid(row=5,column=0,padx=5,pady=5,sticky=W)

        #combo box 
        class_combo=ttk.Combobox(class_Student_frame,textvariable=self.Lop,width=13,font=("Times New Roman",12,"bold"),state="readonly")
        class_combo["values"]=("K13THO1","K14THO1")
        class_combo.current(0)
        class_combo.grid(row=5,column=1,padx=5,pady=5,sticky=W)
        #Radio Buttons
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(class_Student_frame,text="Chụp ảnh mẫu",variable=self.var_radio1,value="Yes")
        radiobtn1.grid(row=6,column=0,padx=10,pady=10,sticky=W)

        radiobtn1=ttk.Radiobutton(class_Student_frame,text="không thêm ảnh mẫu",variable=self.var_radio1,value="No")
        radiobtn1.grid(row=6,column=1,padx=10,pady=10,sticky=W)
        #Button Frame
        btn_frame = Frame(left_frame,bd=2,bg="white",relief=RIDGE)
        btn_frame.place(x=10,y=250,width=635,height=60)
        #Lưu button
        save_btn=Button(btn_frame,command=self.add_data,text="Lưu",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        save_btn.grid(row=0,column=0,padx=5,pady=10,sticky=W)
        #update button
        update_btn=Button(btn_frame,command=self.update_data,text="Sửa",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        update_btn.grid(row=0,column=1,padx=5,pady=8,sticky=W)

        #delete button
        del_btn=Button(btn_frame,command=self.delete_data,text="Xóa",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        del_btn.grid(row=0,column=2,padx=5,pady=10,sticky=W)

        #reset button
        reset_btn=Button(btn_frame,command=self.reset_data,text="Làm Lại",width=7,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        reset_btn.grid(row=0,column=3,padx=5,pady=10,sticky=W)
        #take photo button
        take_photo_btn=Button(btn_frame,command=self.generate_dataset,text="Lấy Ảnh",width=9,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        take_photo_btn.grid(row=0,column=4,padx=5,pady=10,sticky=W)
        #----------------------------------------------------------------------
        # Right Label Frame 
        right_frame = LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Danh sách sinh viên",font=("Times New Roman",12,"bold"),fg="navyblue")
        right_frame.place(x=680,y=10,width=660,height=480)

        #Searching System in Right Label Frame 
        search_frame = LabelFrame(right_frame,bd=2,bg="white",relief=RIDGE,text="Tìm kiếm",font=("Times New Roman",12,"bold"),fg="navyblue")
        search_frame.place(x=10,y=5,width=635,height=80)
        search_label = Label(search_frame,text="Tìm kiếm:",font=("Times New Roman",12,"bold"),fg="navyblue",bg="white")
        search_label.grid(row=0,column=0,padx=5,pady=5,sticky=W)
        self.var_searchTX=StringVar()
        #combo box 
        search_combo=ttk.Combobox(search_frame,textvariable=self.var_searchTX,width=12,font=("Times New Roman",12,"bold"),state="readonly")
        search_combo["values"]=("Tìm kiếm","Rỗng")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=5,pady=15,sticky=W)

        self.var_search=StringVar()
        search_entry = ttk.Entry(search_frame,textvariable=self.var_search,width=12,font=("Times New Roman",12,"bold"))
        search_entry.grid(row=0,column=2,padx=5,pady=5,sticky=W)

        search_btn=Button(search_frame,command=self.search_data,text="Tìm kiếm",width=9,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        search_btn.grid(row=0,column=3,padx=5,pady=10,sticky=W)

        showAll_btn=Button(search_frame,command=self.fetch_data,text="Xem tất cả",width=8,font=("Times New Roman",12,"bold"),fg="white",bg="navyblue")
        showAll_btn.grid(row=0,column=4,padx=5,pady=10,sticky=W)
                # -----------------------------Table Frame-------------------------------------------------
        #Table Frame 
        #Searching System in Right Label Frame 
        table_frame = Frame(right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=10,y=90,width=635,height=360)

        #scroll bar 
        scroll_x = ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame,orient=VERTICAL)

        #create table 
        self.student_table = ttk.Treeview(table_frame,column=("MaSv","TenSV","GioiTinh","NgaySinh","Email","SDT","DiaChi","MaKhoa","MaLop"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("MaSv",text="Mã sinh viên")
        self.student_table.heading("TenSV",text="Họ tên")
        self.student_table.heading("GioiTinh",text="Giới tính")
        self.student_table.heading("NgaySinh",text="Ngày sinh")
        self.student_table.heading("Email",text="Email")
        self.student_table.heading("SDT",text="Số điện thoại")
        self.student_table.heading("DiaChi",text="Địa chỉ")
        self.student_table.heading("MaKhoa",text="Khoa")
        self.student_table.heading("MaLop",text="Lớp")
        self.student_table["show"]="headings"
        # Set Width of Colums 
        self.student_table.column("MaSv",width=100)
        self.student_table.column("TenSV",width=200)
        self.student_table.column("GioiTinh",width=100)
        self.student_table.column("NgaySinh",width=200)
        self.student_table.column("Email",width=200)
        self.student_table.column("SDT",width=100)
        self.student_table.column("DiaChi",width=200)
        self.student_table.column("MaKhoa",width=100)
        self.student_table.column("MaLop",width=100)
        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()
# ==================Các hàm chức năng==============================
    def add_data(self):
        if self.masv.get() == "" or self.tensv.get() == "" or self.ngaysinh.get() == "" or self.gioitinh.get() == "" or self.email.get() == "" or self.sodienthoai.get() == "" or self.diachi.get()=="" or self.Khoa.get() == "" or self.Lop.get() == "":
            messagebox.showerror("Error","Hãy điền vào các thông tin còn thiếu!",parent=self.root)
        else:
            try:
                if(self.Khoa.get() == "Công Nghệ Thông Tin"):
                    self.Khoa.set("CNTT")
                elif(self.Khoa.get() == "Khoa Ngoại Ngữ"):
                    self.Khoa.set("KNN")
                conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                mycursor = conn.cursor()
                mycursor.execute("insert into sinhvien values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                self.masv.get(),
                self.tensv.get(),
                self.gioitinh.get(),
                self.ngaysinh.get(),              
                self.email.get(),
                self.sodienthoai.get(),
                self.diachi.get(),
                self.Khoa.get(),
                self.Lop.get(),
                ))

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Tất cả dữ liệu đã được lưu!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    # ===========================Lấy dữ liệu sinh viên và load dữ liệu lên giao diện ================================

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
        mycursor = conn.cursor()

        mycursor.execute("select MaSv,TenSV,GioiTinh,Ngaysinh,Email,SDT,DiaChi,khoa.TenKhoa,MaLop from sinhvien INNER JOIN Khoa on sinhvien.MaKhoa = Khoa.MaKhoa")
        data=mycursor.fetchall()

        if len(data)!= 0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    #================================Hàm lấy dữ liệu từ Treeview khi người dùng chọn một dòng=======================
    def get_cursor(self,event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.masv.set(data[0]),
        self.tensv.set(data[1]),
        self.gioitinh.set(data[2]),
        self.ngaysinh.set(data[3]),
        self.email.set(data[4]),
        self.sodienthoai.set(data[5]),
        self.diachi.set(data[6]),
        self.Khoa.set(data[7]),
        self.Lop.set(data[8]),
        self.var_radio1.set(data[9])
    # ========================================Update Function==========================
    def update_data(self):
        if self.masv.get() == "" or self.tensv.get() == "" or self.ngaysinh.get() == "" or self.gioitinh.get() == "" or self.email.get() == "" or self.sodienthoai.get() == "" or self.diachi.get()==""or self.Khoa.get() == "" or self.Lop.get() == "":
            messagebox.showerror("Error","Hãy điền vào các thông tin còn thiếu!",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Bạn có muôn cập nhật thông tin sinh viên!",parent=self.root)
                if Update > 0:
                    if(self.Khoa.get() == "Công Nghệ Thông Tin"):
                        self.Khoa.set("CNTT")
                    elif(self.Khoa.get() == "Khoa Ngoại Ngữ"):
                        self.Khoa.set("KNN")
                    conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                    mycursor = conn.cursor()
                    mycursor.execute("update sinhvien set TenSV=%s,GioiTinh=%s,NgaySinh=%s,Email=%s,SDT=%s,DiaChi=%s,MaKhoa=%s,MaLop=%s where MaSv=%s",( 

                    self.tensv.get(),
                    self.gioitinh.get(),
                    self.ngaysinh.get(),              
                    self.email.get(),
                    self.sodienthoai.get(),
                    self.diachi.get(),
                    self.Khoa.get(),
                    self.Lop.get(),
                    self.masv.get()  
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success","Cập nhật dữ liệu thành công!",parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    
    #==============================Delete Function=========================================
    def delete_data(self):
        if self.masv.get()=="":
            messagebox.showerror("Error","Cần tồn tại mã sinh viên muốn xóa!",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Delete","Bạn có muốn xóa sinh viên này không?",parent=self.root)
                if delete>0:
                    conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                    mycursor = conn.cursor() 
                    sql="delete from sinhvien where MaSv=%s"
                    val=(self.masv.get(),)
                    mycursor.execute(sql,val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Xóa thành công!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    # Reset Function 
    def reset_data(self):
        self.masv.set(""),
        self.tensv.set(""),
        self.gioitinh.set("Nam"),
        self.ngaysinh.set(""),
        self.email.set(""),
        self.sodienthoai.set(""),
        self.diachi.set(""),
        self.Khoa.set(""),
        self.Lop.set(""),
        self.var_radio1.set("")
    
    # ===========================Search Data===================
    def search_data(self):
        if self.var_search.get()=="" or self.var_searchTX.get()=="Select":
            messagebox.showerror("Error","Hãy chọn hình thức bạn muốn tìm kiếm và nhập thông tin bạn muốn tìm",parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                my_cursor = conn.cursor()
                # "MaSv","TenSV","GioiTinh","NgaySinh","Email","SDT","DiaChi"
                sql = "SELECT MaSv,TenSV,GioiTinh,NgaySinh,Email,SDT,DiaChi,khoa.TenKhoa,MaLop FROM sinhvien INNER JOIN khoa on sinhvien.MaKhoa = khoa.MaKhoa where MaSv='" +str(self.var_search.get()) + "'" 
                my_cursor.execute(sql)
                # my_cursor.execute("select * from student where MaSV= " +str(self.var_search.get())+" "+str(self.var_searchTX.get())+"")
                rows=my_cursor.fetchall()        
                if len(rows)!=0:
                    self.student_table.delete(*self.student_table.get_children())
                    for i in rows:
                        self.student_table.insert("",END,values=i)
                    if rows==None:
                        messagebox.showerror("Error","Không tìm thấy dữ liệu",parent=self.root)
                        conn.commit()
                conn.close()
            except Exception as es:
                messagebox.showerror("Error",f"Due To :{str(es)}",parent=self.root)

# ==================================Hàm lấy dữ liệu từ camera và lưu vào thư mục train_img=========================
    def generate_dataset(self):
        if self.masv.get() == "" or self.tensv.get() == "" or self.ngaysinh.get() == "" or self.gioitinh.get() == "" or self.email.get() == "" or self.sodienthoai.get() == "" or self.diachi.get()=="":
            messagebox.showerror("Error","Hãy điền các thông tin còn thiếu!",parent=self.root)
        else:
            try:                
                # conn = mysql.connector.connect(host="localhost",user="root",password="",database="DiemDanhSinhVien")
                # mycursor = conn.cursor()
                # mycursor.execute("select * from sinhvien")
                # myreslut = mycursor.fetchall()


                # mycursor.execute("update sinhvien set TenSV=%s,GioiTinh=%s,NgaySinh=%s,Email=%s,SDT=%s,DiaChi=%swhere MaSv=%s",( 
                #     self.masv.get(),
                #     self.tensv.get(),
                #     self.ngaysinh.get(),
                #     self.gioitinh.get(),
                #     self.email.get(),
                #     self.sodienthoai.get(),
                #     self.diachi.get(),
                #     self.var_radio1.get(), 
                #     ))
                # conn.commit()
                # self.fetch_data()
                # self.reset_data()
                # conn.close()
                # ====================part of opencv=======================
                cap=cv2.VideoCapture(0)
                count = 0
                path = 'train_img/'
                nameID = self.masv.get()
                while True:
                    success, img = cap.read()
                    count = count + 1
                    name = os.path.join(path, f'{nameID}_{count}.jpg')
                    cv2.imwrite(name, img)
                    cv2.imshow("Camera", img)
                    cv2.waitKey(1)
                    time.sleep(0.2)
                    if count > 100:
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Lấy dữ liệu thành công!",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root) 
# main class object

if __name__ == "__main__":
    root=Tk()
    obj=Student(root)
    root.mainloop()




