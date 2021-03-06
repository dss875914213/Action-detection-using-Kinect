from tkinter import *
from tkinter.tix import Tk, Control, ComboBox  #升级的组合控件包
from tkinter.messagebox import showinfo, showwarning, showerror #各种类型的提示框
from PIL import Image, ImageTk

from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import cv2 
import numpy as np

from mylib.pk_func import to_kinect,draw_body
from mylib.train import train

class basic_desk():
    def __init__(self,master):
        self.master = master    
        self.basic_func()
        self.bottom_func()

    def bottom_func(self):    
        # 底栏Frame
        self.bottom_frame = Frame(self.master)
        self.bottom_frame.pack(side=BOTTOM,anchor=SW)
        # 进入下一界面
        change = Button(self.bottom_frame,text='Continue',command=self.change_func)
        change.grid(row=1,column=1)
        # return to last Frame
        back = Button(self.bottom_frame,text='Back',command=self.back_func)
        back.grid(row=1,column=2)
        # 退出
        _quit = Button(self.bottom_frame,text='  Quit  ',command=self.master.quit)
        _quit.grid(row=1,column=3)


    def basic_func(self):   
        # 初始化进入界面
        self.basic = Frame(self.master,width=1000,height=1000)
        self.basic.pack()
        # 标题
        Label(self.basic,text='Action Recognition',font=("Arial",15)).pack()
        # =======================================================================
        model_frame = Frame(self.basic)
        model_frame.pack()
        # Choose Neural Model
        # Create label
        model_label = Label(model_frame,text='The neural model: ',anchor='w')
        model_label.grid(row=1,column=0,rowspan=2,columnspan=2)
        
        self.model_type = StringVar()
        self.model_type.set('LSTM')
        model_LSTM = Radiobutton(model_frame,text='LSTM',variable=self.model_type,value='LSTM')
        model_LSTM.grid(row=5,column=1)
        model_CNN = Radiobutton(model_frame,text='CNN',variable=self.model_type,value='CNN')
        model_CNN.grid(row=5,column=6)
        # ===========================================================================
        skeleton_frame = Frame(self.basic)
        skeleton_frame.pack()
        # Choose the skeleton algorithm 
        # Create label
        skeleton_label = Label(skeleton_frame,text='The skeleton algorithm: ')
        skeleton_label.grid(row=1,column=0,rowspan=2,columnspan=2)
        
        self.skeleton_type = StringVar()
        self.skeleton_type.set('Kinect')
        skeleton_Kinect = Radiobutton(skeleton_frame,text='Kinect',variable=self.skeleton_type,value='Kinect')
        skeleton_Kinect.grid(row=5,column=1)
        skeleton_openpose = Radiobutton(skeleton_frame,text='OpenPose',variable=self.skeleton_type,value='OpenPose')
        skeleton_openpose.grid(row=5,column=6)
        # ===============================================================================
        train_frame = Frame(self.basic)
        train_frame.pack()

        Label(train_frame,text='如果进行训练，请将数据集放入data文件夹，其中要有Skeleton.txt:空格隔开，label.txt:逗号隔开，回车键换行，格式为：标签，开始帧，结束帧;'
            ,font=("Arial",10),width = 60,height = 3,wraplength = 400,justify = 'left').pack()

        train = Button(train_frame,text='Start training',command=self.train_func)
        train.pack(side=RIGHT)
      
    def change_func(self):
        try:
            if  self.basic._name in self.master.children:
                self.basic.destroy()
                self.detect()
        except:
            pass
        try:
            if self.train._name in self.master.children:
                model = self.training_model.get()
                print('The model is {}, the label is {}'.format(model,self.label_text))
                # temp = train(model=model)
                # self.trained_rate.set(' The accuracy of the model is {:.2f}'.format(temp))
        except:
            pass 
        # self.bottom_frame.destroy()
        # detect_desk(self.master,device=self.device,flag=flag)

    def back_func(self):
        # 不满意（︶^︶）
        try:
            if self.detect_frame._name in self.master.children:
                self.detect_frame.destroy()
                self.basic_func()
        except:
            pass
        try:
            if self.train._name in self.master.children:
                self.train.destroy()
                self.basic_func()
        except:
            pass

    def train_func(self):
        if  self.basic._name in self.master.children:
            self.basic.destroy()
        self.train = Frame(self.master,width=1000,height=1000)
        self.train.pack()
        # ===================================================================================
        word = Frame(self.train)
        word.pack()
        Label(word,text='Action Recognition',font=("Arial",15)).pack()
        Label(word,text='Training the model',font=("Arial",13)).pack()
        # ====================================================================================
        select = Frame(self.train)
        select.pack()
        # Choose Neural Model
        # Create label
        model_label = Label(select,text='The model to train : ')
        model_label.grid(row=1,column=0,rowspan=2,columnspan=2)
        
        self.training_model = StringVar()
        self.training_model.set('LSTM')
        model_LSTM = Radiobutton(select,text='LSTM',variable=self.training_model,value='LSTM')
        model_LSTM.grid(row=5,column=1)
        model_CNN = Radiobutton(select,text='CNN',variable=self.training_model,value='CNN')
        model_CNN.grid(row=5,column=6)
        
        self.label_text = StringVar()
        entry_label = Entry(select,textvariable=self.label_text)
        self.label_text.set('falling,waving,kicking,punching,standing,walking,jumping')
        entry_label.grid(row=6,column=1)
        # ========================================================================================
        result = Frame(self.train)
        result.pack()
        # display the correct rate
        self.trained_rate = StringVar()
        self.trained_rate.set(' The accuracy of the model is ')
        trained_label = Label(result,textvariable=self.trained_rate,justify = 'left',font=("Arial",12))
        trained_label.grid(row=1,column=0,rowspan=2,columnspan=2)
        change_model = Button(result,text='Change the model',command=self.open_file)
        change_model.grid(row=6,column=1)
        show_matrix = Button(result,text='Show the confusion matrix',command=self.show_confusion)
        show_matrix.grid(row=6,column=2)

    def show_confusion(self):
        '''
        功能实现应该简单吧？
        '''
        import os
        try:
            os.startfile('data\cm.jpg')
        except:
            os.startfile('data/cm.jpg')

    def open_file(self):
        import os
        path = ['']
        if self.training_model.get() == 'LSTM':
            path = ['LSTM_Train\lstm.py','LSTM_Train/lstm.py']
        elif self.training_model.get() == 'CNN':
            path = ['CNN_Train\keleton_based_classfication.py','CNN_Train/keleton_based_classfication.py']

        try:
            os.startfile(path[0])
        except:
            os.startfile(path[1])

    def detect(self):
        # 初始化进入界面
        self.detect_frame = Frame(self.master,width=1000,height=1000)
        self.detect_frame.pack()

        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Depth)

        # label info
        self.label = StringVar()
        self.last_label = 'preparing'
        self.label.set(self.last_label)
        
        if self.model_type.get() == 'LSTM':
            from LSTM_Train.lstm_model import lstm
            self.model = lstm()
        elif self.model_type.get() =='CNN':
            from CNN_Train.cnn_model import cnn
            self.model = cnn()
        # print(self.model_type)
        if self.skeleton_type.get() == 'OpenPose':
            from mylib.SkeletonDetector import SkeletonDetector
            self.detector = SkeletonDetector("mobilenet_thin","432x368")
        # image panel
        self.panel = Label(self.detect_frame)
        self.panel.pack()
        self.loop()

        # label info2
        action_label = Label(self.detect_frame,textvariable=self.label)
        action_label.pack(side=LEFT)
        
    def loop(self):
        # self.label.set("test")
        try:
            img = self._kinect.get_last_color_frame()
        except:
            success = False
        else:
            img = np.reshape(img,[1080,1920,4])
            self.img = cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)           
            success = True

        if success:
            temp_joints = np.array([],dtype=float)
            # get skeleton
            if self.skeleton_type.get() == 'Kinect':
                if self._kinect.has_new_body_frame(): 
                    self._bodies = self._kinect.get_last_body_frame()
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if not body.is_tracked: 
                            continue           
                        joints = body.joints 
                        # convert joint coordinates to color space 
                        joint_points = self._kinect.body_joints_to_color_space(joints)
                        # self.draw_body(joints, joint_points)
                        self.img = draw_body(joints,joint_points,self.img)
                        for i in range(0,25):
                            temp_joints = np.append(temp_joints,joints[i].Position.x)
                            temp_joints = np.append(temp_joints,joints[i].Position.y)
                            temp_joints = np.append(temp_joints,joints[i].Position.z)
            elif self.skeleton_type.get() == 'OpenPose':
                if self._kinect.has_new_depth_frame():
                    self.img = cv2.resize(self.img,(432,368))
                    humans = self.detector.detect(self.img)
                    skeletons,scale_y = self.detector.humans_to_skelsList(humans)
                    self.detector.draw(self.img,humans)
                    # pos = get_world_pos(self._kinect,skeletons)
                    # pos = np.array(pos[0])
                    # temp_joints = np.append(temp_joints,pos)
                    temp_joints = to_kinect(self._kinect,skeletons) # I do not know it is right

            if temp_joints.shape[0] != 0:
                # input data and output label
                # print(temp_joints)
                temp_label = self.model.data_input(temp_joints)
                if temp_label != ' ':
                    self.last_label = temp_label
                # print(temp_label)
                self.label.set(self.last_label)

            # output image
            self.img = cv2.resize(self.img,(640,480))
            current_img = Image.fromarray(self.img)
            imgtk = ImageTk.PhotoImage(image=current_img)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
        self.detect_frame.after(1,self.loop)

if __name__ == "__main__":
    # initialize Tk
    root = Tk() 
    root.title("Action Recognition")   
    root.geometry("640x550")    
    root.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
    root.tk.eval('package require Tix')  #引入升级包

    basic_desk(root)

    root.mainloop()