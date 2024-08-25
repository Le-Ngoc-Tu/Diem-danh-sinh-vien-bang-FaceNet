# import re
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
import facenet
import detect_face
import time
import pickle
import tensorflow.compat.v1 as tf
import csv
class Face_Recognition:

    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Pannel")
        img = Image.open(r"Images_GUI\banner.jpg")
        img = img.resize((1366, 130), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)
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
        title_lb1 = Label(bg_img,text="Chào mừng bạn đến với chương trình nhận dạng khuôn mặt",font=("Times New Roman",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Nút nhận dạng
        std_img_btn=Image.open(r"Images_GUI\f_det.jpg")
        std_img_btn=std_img_btn.resize((180,180),Image.ANTIALIAS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.face_recog,image=self.std_img1,cursor="hand2")
        std_b1.place(x=600,y=170,width=180,height=180)

        std_b1_1 = Button(bg_img,command=self.face_recog,text="Nhận dạng",cursor="hand2",font=("Times New Roman",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=600,y=350,width=180,height=45)
    #=====================Điểm danh===================
    def mark_attendance(self,name,names_id):
        file_path = "attendance.csv"
        now = datetime.now()
        d1 = now.strftime("%d/%m/%Y")
        dtString = now.strftime("%H:%M:%S")

        time_threshold_vaosang = datetime.strptime("07:30:00", "%H:%M:%S")
        time_threshold_rasang = datetime.strptime("11:10:00", "%H:%M:%S")
        time_threshold_vaochieu = datetime.strptime("13:30:00", "%H:%M:%S")
        time_threshold_rachieu = datetime.strptime("17:10:00", "%H:%M:%S")

        if (now.time() > time_threshold_vaosang.time() and now.time() < time_threshold_rasang.time()) or \
                (now.time() > time_threshold_vaochieu.time() and now.time() < time_threshold_rachieu.time()):
            status = "present"
        else:
            status = "Absent"

        with open(file_path,"a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f,delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([name, names_id,dtString, d1, status])
    #================face recognition==================
    def face_recog(self):
        video=0
        modeldir = './model/20180402-114759.pb'
        classifier_filename = './class/classifier.pkl'
        npy='./npy'
        train_img="./train_img"
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.6)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                pnet, rnet, onet = detect_face.create_mtcnn(sess, npy)
                minsize = 30  # minimum size of face
                threshold = [0.6,0.7,0.7]  # three steps's threshold
                factor = 0.709  # scale factor
                margin = 44
                batch_size =100 #1000
                image_size = 182
                input_image_size = 160
                HumanNames = os.listdir(train_img)
                HumanNames.sort()
                facenet.load_model(modeldir)
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                embedding_size = embeddings.get_shape()[1]
                classifier_filename_exp = os.path.expanduser(classifier_filename)
                with open(classifier_filename_exp, 'rb') as infile:
                    (model, class_names) = pickle.load(infile,encoding='latin1')

                video_capture = cv2.VideoCapture(video)
                while True:
                    ret, frame = video_capture.read()
                            #frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #resize frame (optional)
                    if not ret:  # Kiểm tra xem việc đọc một khung hình có thành công không
                        break  # Thoát khỏi vòng lặp nếu không còn khung hình nào để đọc
                    timer =time.time()
                    if frame.ndim == 2:
                        frame = facenet.to_rgb(frame)
                    bounding_boxes, _ = detect_face.detect_face(frame, minsize, pnet, rnet, onet, threshold, factor)
                    faceNum = bounding_boxes.shape[0]
                    if faceNum > 0:
                        det = bounding_boxes[:, 0:4]
                        img_size = np.asarray(frame.shape)[0:2]
                        cropped = []
                        scaled = []
                        scaled_reshape = []
                        for i in range(faceNum):
                            emb_array = np.zeros((1, embedding_size))
                            xmin = int(det[i][0])
                            ymin = int(det[i][1])
                            xmax = int(det[i][2])
                            ymax = int(det[i][3])
                            
                            try:
                                # inner exception
                                if xmin <= 0 or ymin <= 0 or xmax >= len(frame[0]) or ymax >= len(frame):
                                    print('Face is very close!')
                                    continue
                                cropped.append(frame[ymin:ymax, xmin:xmax,:])
                                cropped[i] = facenet.flip(cropped[i], False)
                                scaled.append(np.array(Image.fromarray(cropped[i]).resize((image_size, image_size))))
                                scaled[i] = cv2.resize(scaled[i], (input_image_size,input_image_size),
                                                        interpolation=cv2.INTER_CUBIC)
                                scaled[i] = facenet.prewhiten(scaled[i])
                                scaled_reshape.append(scaled[i].reshape(-1,input_image_size,input_image_size,3))
                                feed_dict = {images_placeholder: scaled_reshape[i], phase_train_placeholder: False}
                                emb_array[0, :] = sess.run(embeddings, feed_dict=feed_dict)
                                predictions = model.predict_proba(emb_array)
                                best_class_indices = np.argmax(predictions, axis=1)
                                best_class_probabilities = predictions[np.arange(len(best_class_indices)), best_class_indices]
                                if best_class_probabilities>0.8:
                                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,255,255), 2)    #boxing face
                                    for H_i in HumanNames:
                                        if HumanNames[best_class_indices[0]] == H_i:
                                            result_names = HumanNames[best_class_indices[0]]
                                            print("Predictions : [ name: {} , accuracy: {:.3f} ]".format(HumanNames[best_class_indices[0]],best_class_probabilities[0]))
                                            # cv2.rectangle(frame, (xmin, ymin-20), (xmax, ymin-2), (0, 255,255), -1)
                                            cv2.putText(frame, result_names, (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                        1, (0,255,255), thickness=1, lineType=1)
                                            try:
                                                conn = mysql.connector.connect(user='root', password='',host='localhost',database='DiemDanhSinhVien',port=3306)
                                                cursor = conn.cursor()
                                                cursor.execute("SELECT `TenSV` FROM `sinhvien` WHERE Masv='" + str(result_names) + "'")
                                                name=cursor.fetchone()
                                                name="+".join(name)
                                                conn.commit()
                                                print("Name from Database:", name)
                                            except Exception as e:
                                                print("Error during SQL query:", e)
                                            # cv2.putText(frame, name, (xmin,ymin-30), cv2.FONT_HERSHEY_COMPLEX_SMALL,1, (0,255,255), thickness=1, lineType=1)
                                            self.mark_attendance(result_names,name)
                                            
                                else :
                                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,0,255), 2)
                                    # cv2.rectangle(frame, (xmin, ymin-20), (xmax, ymin-2), (0, 255,255), -1)
                                    cv2.putText(frame, "Unknown", (xmin,ymin-5), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                                        1, (0,255,255), thickness=1, lineType=1)
                            except:   
                                print("error")
                    endtimer = time.time()
                    fps = 1/(endtimer-timer)
                    cv2.rectangle(frame,(15,30),(135,60),(0,255,255),-1)
                    cv2.putText(frame, "fps: {:.2f}".format(fps), (20, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                    cv2.imshow('Face Recognition', frame)
                    key= cv2.waitKey(1)
                    if key== 113: # "q"
                        break
                video_capture.release()
                cv2.destroyAllWindows()
if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()