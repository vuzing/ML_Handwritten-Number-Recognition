import cv2
import numpy as np
from skimage.feature import hog
from sklearn.svm import LinearSVC
from tkinter import Tk, Button, filedialog, Label
from PIL import Image, ImageTk
from keras.datasets import mnist
from sklearn.metrics import accuracy_score
from tkinter import BOTTOM
from tkinter import Text
from tkinter import Frame

# Load dữ liệu số 
(X_train, y_train), (X_test, y_test) = mnist.load_data()
print("Loaded mnist data")

# Cho huấn luyện 
X_train_feature = []
for i in range(len(X_train)):
    feature = hog(X_train[i], orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), block_norm="L2")
    X_train_feature.append(feature)
X_train_feature = np.array(X_train_feature, dtype=np.float32)

# Cho thử nghiệm 
X_test_feature = []
for i in range(len(X_test)):
    feature = hog(X_test[i], orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), block_norm="L2")
    X_test_feature.append(feature)
X_test_feature = np.array(X_test_feature, dtype=np.float32)

print("Trained")

# Huyến luyện bằng thuật toán SVC  
model = LinearSVC(C=10, dual=True, max_iter=5000)
model.fit(X_train_feature, y_train)
y_pre = model.predict(X_test_feature)
print(accuracy_score(y_test, y_pre))

# Hiện thị ảnh cần nhận diện   
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global image_path
        image_path = file_path
        original_image = Image.open(image_path)
        original_image.thumbnail((550, 450))  
        tk_image = ImageTk.PhotoImage(original_image)
        image_label1.config(image=tk_image)
        image_label1.image = tk_image  
        
        
        
# Hàm nhận diện 
def identify_digits():
    global image_path
    if image_path:
        image = cv2.imread(image_path)
        im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        im_blur = cv2.GaussianBlur(im_gray, (5, 5), 0)
        im, thre = cv2.threshold(im_blur, 90, 255, cv2.THRESH_BINARY_INV)
        contours, hierachy = cv2.findContours(thre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        recognized_numbers = []  
        
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = thre[y:y + h, x:x + w]
            roi = np.pad(roi, (20, 20), 'constant', constant_values=(0, 0))
            roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
            roi = cv2.dilate(roi, (3, 3))
            roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1),
                             block_norm="L2")
            nbr = model.predict(np.array([roi_hog_fd], np.float32))
            recognized_numbers.append(int(nbr[0]))  # thêm các số nhận diện vào danh sách 
            
            cv2.putText(image, str(int(nbr[0])), (x, y), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 255), 3)
        
        # Chuyển đổi danh sách số thành dạng chuỗi 
        recognized_text = ', '.join(map(str, recognized_numbers))
        
        # Hiển thị trên thanh textbox 
        text_box.config(state="normal")
        text_box.delete(1.0, "end")  
        text_box.insert("end", recognized_text)
        text_box.config(state="disabled")
        
        # Hiển thị ảnh nhận diện 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(image=pil_image)
        image_label2.config(image=tk_image)
        image_label2.image = tk_image  


# Tạo cửa sổ 
root = Tk()
root.title("Digit Recognition")
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

# Tạo khung chứa ảnh
blank_image = Image.new("RGB", (550, 450), "white")
photo1 = ImageTk.PhotoImage(blank_image)
image_label1 = Label(root, image=photo1, width=550, height=450)
image_label1.place(x=30, y=100)

# Tạo khung chứa ảnh nhận diện 
blank_image = Image.new("RGB", (550, 450), "white")
photo1 = ImageTk.PhotoImage(blank_image)
image_label2 = Label(root, image=photo1, width=550, height=450)
image_label2.place(x=700, y=100)


#Tạo nút 
button_frame= Frame(root).pack(side=BOTTOM)
load_button= Button(button_frame, text="Load Image", font=("Arial", 10, 'bold'), bg='#303030', fg='#FFFFFF', command=select_image)
load_button.place(x=600, y=200)
identifi_button= Button(button_frame, text="Identifi", font=("Arial", 10, 'bold'), bg='#303030', fg='#FFFFFF',command=identify_digits)
identifi_button.place(x=600, y=400)


# tạo mới đường dẫn 
image_path = None

# Tạo ô văn bản
text_box = Text(root, font=("Arial", 20), width=37, height=2)
text_box.place(x=700, y=600)
text_box.config(state="disabled")

#Chạy chương trình 
root.mainloop()