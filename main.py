# Import các thư viện cần thiết
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from student import Student
from train import Train
from facedetec_from import Face_Recognition
from attendance import Attendance
import os

# Định nghĩa lớp chương trình chính
class Face_Recognition_System:
    def __init__(self, root):
        # Khởi tạo cửa sổ giao diện chương trình
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face_Recogonition_System")
        # This part is image labels setting start 
        # first header image  
        img=Image.open(r"Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.ANTIALIAS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # Tạo background image
        bg1 = Image.open(r"Images_GUI\bg4.png")
        bg1 = bg1.resize((1366, 768), Image.ANTIALIAS)
        self.photobg1 = ImageTk.PhotoImage(bg1)
        # Set image làm label
        bg_img = Label(self.root, image=self.photobg1)
        bg_img.place(x=0, y=130, width=1366, height=768)

        # Tiêu đề chương trình
        title_lb1 = Label(bg_img, text="Điểm Danh Sinh Viên Bằng Nhận Dạng Khuôn Mặt", font=("verdana", 30, "bold"), bg="white", fg="navyblue")
        title_lb1.place(x=0, y=0, width=1366, height=45)

        # Tạo các nút cho chương trình
        # ------------------------------------------------------------------------------------------------------------------- 
        # Nút Sinh viên
        std_img_btn = Image.open(r"Images_GUI\std1.jpg")
        std_img_btn = std_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.std_img1 = ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img, command=self.student_pannels, image=self.std_img1, cursor="hand2")
        std_b1.place(x=250, y=100, width=180, height=180)

        std_b1_1 = Button(bg_img, command=self.student_pannels, text="Sinh Viên", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        std_b1_1.place(x=250, y=280, width=180, height=45)

        # Nút Nhận Dạng 
        det_img_btn = Image.open(r"Images_GUI\det2.jpg")
        det_img_btn = det_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.det_img1 = ImageTk.PhotoImage(det_img_btn)

        det_b1 = Button(bg_img, command=self.face_rec, image=self.det_img1, cursor="hand2")
        det_b1.place(x=600, y=100, width=180, height=180)

        det_b1_1 = Button(bg_img, command=self.face_rec, text="Nhận Dạng", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        det_b1_1.place(x=600, y=280, width=180, height=45)

        # Nút Điểm danh
        att_img_btn = Image.open(r"Images_GUI\att.jpg")
        att_img_btn = att_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.att_img1 = ImageTk.PhotoImage(att_img_btn)

        att_b1 = Button(bg_img, command=self.attendance_pannel, image=self.att_img1, cursor="hand2")
        att_b1.place(x=940, y=100, width=180, height=180)

        att_b1_1 = Button(bg_img, command=self.attendance_pannel, text="Điểm Danh", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        att_b1_1.place(x=940, y=280, width=180, height=45)
        
        # Nút Train dữ liệu
        tra_img_btn = Image.open(r"Images_GUI\tra1.jpg")
        tra_img_btn = tra_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.tra_img1 = ImageTk.PhotoImage(tra_img_btn)

        tra_b1 = Button(bg_img, command=self.train_pannels, image=self.tra_img1, cursor="hand2")
        tra_b1.place(x=420, y=360, width=180, height=180)

        tra_b1_1 = Button(bg_img, command=self.train_pannels, text="Train dữ liệu", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        tra_b1_1.place(x=420, y=540, width=180, height=45)

        # Nút Thoát
        exi_img_btn = Image.open(r"Images_GUI\exi.jpg")
        exi_img_btn = exi_img_btn.resize((180, 180), Image.ANTIALIAS)
        self.exi_img1 = ImageTk.PhotoImage(exi_img_btn)

        exi_b1 = Button(bg_img, command=self.Close, image=self.exi_img1, cursor="hand2")
        exi_b1.place(x=780, y=360, width=180, height=180)

        exi_b1_1 = Button(bg_img, command=self.Close, text="Thoát", cursor="hand2", font=("tahoma", 15, "bold"), bg="white", fg="navyblue")
        exi_b1_1.place(x=780, y=540, width=180, height=45)
        # ==================Functions Buttons=====================

    # Hàm mở cửa sổ Sinh viên
    def student_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    # Hàm mở cửa sổ Train dữ liệu
    def train_pannels(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    # Hàm mở cửa sổ Nhận Dạng
    def face_rec(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    # Hàm mở cửa sổ Điểm Danh
    def attendance_pannel(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    # Hàm đóng cửa sổ chương trình
    def Close(self):
        root.destroy()

# Chạy chương trình khi được gọi
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
