from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

def load_image():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image files", "*.jpg *.png"), ("All files", "*.*")))
    if file_path:
        image = Image.open(file_path)
        # Resize image if needed
        image = image.resize((550, 450))
        photo = ImageTk.PhotoImage(image)
        image_label1.config(image=photo)
        image_label1.image = photo  

def identify_number():
    text_box.config(state="normal")  # Enable text box
    
    text_box.insert(END, "Đây là số 6 ")  # Insert text
    text_box.config(state="disabled")  # Disable text box


root = Tk()
root.title('Nhận diện chữ số')
root.geometry("1280x720")

# Tạo ảnh nền
load = Image.open('background.png')
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.place(x=-1, y=-1)

# Tạo chữ
name = Label(root, text="IDENTIFI", fg="#FFFFFF", bd=0, bg="#03152D")
name.config(font=("AVA", 40))
name.pack(pady=10)

#Tạo nút 
button_frame= Frame(root).pack(side=BOTTOM)
load_button= Button(button_frame, text="Load Image", font=("Arial", 10, 'bold'), bg='#303030', fg='#FFFFFF', command=load_image)
load_button.place(x=600, y=200)
identifi_button= Button(button_frame, text="Identifi", font=("Arial", 10, 'bold'), bg='#303030', fg='#FFFFFF',command=identify_number)
identifi_button.place(x=600, y=400)

# Tạo khung chứa ảnh
blank_image = Image.new("RGB", (550, 450), "white")
photo1 = ImageTk.PhotoImage(blank_image)
image_label1 = Label(root, image=photo1, width=550, height=450)
image_label1.place(x=30, y=100)

# Tạo khung chứa nhận diện
# image2 = Image.open('chuoi1.jpg')
# width, height = 550, 450
# image2 = image2.resize((width, height))
# photo2 = ImageTk.PhotoImage(image2)
# image_label2 = Label(root, image=photo2, width=width, height=height)
# image_label2.place(x=700, y=100)

# Tạo khung chứa ảnh nhận diện 
blank_image = Image.new("RGB", (550, 450), "white")
photo1 = ImageTk.PhotoImage(blank_image)
image_label2 = Label(root, image=photo1, width=550, height=450)
image_label2.place(x=700, y=100)

# Tạo ô văn bản
text_box = Text(root, font=("Arial", 20), width=37, height=2)
text_box.place(x=700, y=600)
text_box.config(state="disabled")

root.mainloop()
