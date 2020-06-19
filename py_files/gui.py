from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from face_emo_cog import FaceEmoCog
import numpy as np
import cv2


class App():

    def __init__(self):
        self.recognizer = FaceEmoCog()
        self.window = Tk()
        self.window.title("Facial Emotion Recognition")
        self.window.geometry("800x800")
        self.homeScreen()
        self.img_path = "../no_image.jpg"


    def homeScreen(self):
        self.frame = Frame(self.window, bg="#004d66", width=800, height=800)
        self.frame.pack()
        self.title = Label(self.frame, font=("OpenSansCondensedLight", 40, "bold"), text="Facial Emotion Recognition", fg="#ff6600", bg="#004d66")
        self.title.place(relx=0.2, rely=0.35)
        next_button = Label(self.frame, text="Try it", font=("OpenSansCondensedLight", 20, "bold"), fg="#ff6600", bg="#004d66", cursor="hand1")
        next_button.place(relx=0.48, rely=0.5)
        next_button.bind("<Button-1>", self.secondScreen)

    
    def secondScreen(self, event):
        self.frame.destroy()
        
        self.frame = Frame(self.window, bg="#004d66", width=1200, height=800)
        self.frame.place(relx=0, rely=0)

        top_frame = Frame(self.frame, bg="#004d66", width=1200, height=60)
        top_frame.place(relx=0, rely=0)

        title=Label(top_frame, font=("OpenSansCondensedLight", 30, "bold"), text="Facial Emotion Recognition", fg="#ff6600", bg="#004d66")
        title.place(relx=0.17, rely=0.08)

        bottom_frame = Frame(self.frame, width=1200, height= 800 - 60)
        bottom_frame.place(relx=0, rely=0.1)

        self.img_container = Frame(bottom_frame, highlightbackground="#004d66", highlightcolor="#004d66", highlightthickness=2, width=600, height=600, bg="#000")
        self.img_container.place(relx=0.08, rely=0.01)

        self.displayImage()

        browse_files_label = Label(bottom_frame, font=("OpenSansCondensedLight", 16, "bold"), cursor="hand1", fg="#ff6600", text="Choose File")
        browse_files_label.bind("<Button-1>", self.filePicker)
        browse_files_label.place(relx=0.08, rely=0.85)

        live_cam_label = Label(bottom_frame, font=("OpenSansCondensedLight", 16, "bold"), cursor="hand1", fg="#ff6600", text="Live Camera")
        live_cam_label.bind("<Button-1>", self.triggerLiveCam)
        live_cam_label.place(relx=0.22, rely=0.85)

        predict_label = Label(bottom_frame, font=("OpenSansCondensedLight", 16, "bold"), cursor="hand1", fg="#ff6600", text="Predict")
        predict_label.bind("<Button-1>", self.predictEmotions)
        predict_label.place(relx=0.52, rely=0.85)


    def predictEmotions(self, event):
        recognized = self.recognizer.recognize_within_image(self.img_path)
        self.photo.destroy()
        self.displayImage(image=recognized)

    
    def filePicker(self, event):
        filename = filedialog.askopenfilename(initialdir="/home/raghu/Desktop/final-year-project/data/ppt images", title="Select file", filetypes=(("jpeg files","*.jpg"), ("png files","*.png"), ("mp4 files", "*.mp4")))
        extension = filename.split('.')[-1]
        if extension in 'jpeg, jpg, png'.split(', '):
            self.img_path = filename
            print(filename)
            self.photo.destroy()
            self.displayImage()
        elif extension == 'mp4':
            self.displayVideo(path=filename, live_cam=False)

    
    def triggerLiveCam(self, event):
        self.displayVideo(live_cam = True)

    
    def displayVideo(self, path="", live_cam=True):
        self.photo.destroy()
        self.img_path = "../no_image.jpg"
        self.displayImage()
        if(live_cam):
            self.recognizer.recognize_within_video(live_cam = live_cam)
        else:
            self.recognizer.recognize_within_video(filepath = path)


    def getResizedImage(self, filename="", image=None):
        img = image
        if image is None:
            img = Image.open(filename)
        img = self.resizeWithAspectRatio(img)
        disp = ImageTk.PhotoImage(img)
        rel_x, rel_y = self.getRelativePosition(img.size)
        return disp, rel_x, rel_y


    def resizeWithAspectRatio(self, img):
        new_width, new_height = img.width, img.height
        # print(new_width, new_height)
        if img.width >= 596:
            new_width = 590
            new_height = round(img.height * 590 / img.width)
        if img.height >= 596:
            new_height = 590
            new_width = round(img.width * 590 / img.height)
        print(new_width, new_height)
        return img.resize((new_width, new_height))


    def getRelativePosition(self, size):
        rel_x = (594 - size[0]) / 1200
        rel_y = (594 - size[1]) / 1200
        return rel_x, rel_y

    
    def displayImage(self, image=None):
        disp, rel_x, rel_y = None, None, None
        if image != None:
            disp, rel_x, rel_y = self.getResizedImage(image=image)
        else:
            disp, rel_x, rel_y = self.getResizedImage(self.img_path)
        self.photo = Label(self.img_container, image=disp)
        self.photo.image=disp
        self.photo.place(relx=rel_x, rely=rel_y)


    def run(self):
        self.window.mainloop()


App().run()

print("yo!")
