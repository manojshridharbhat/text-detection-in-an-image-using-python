import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera")
img_counter = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:#esc
        print("Escape hit, closing...")
        break
    elif k%256 == 32:#space
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
cam.release()
cv2.destroyAllWindows()


#code for detacting text
import string
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
# Reading image 
img = cv2.imread(img_name)
# Convert to RGB 
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# Detect texts from image
texts = pytesseract.image_to_string(img)
print(texts)
conf = r'-c tessedit_char_whitelist='+string.digits

def draw_boxes_on_text(img):
    # Return raw information about the detected texts
    raw_data = pytesseract.image_to_data(img)

    print(raw_data)
    for count, data in enumerate(raw_data.splitlines()):
        if count > 0:
            data = data.split()
            if len(data) == 12:
                x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                cv2.rectangle(img, (x, y), (w+x, h+y), (0, 255, 0), 1)
                cv2.putText(img, content, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255) , 1)
                
    return img


img = draw_boxes_on_text(img)    

# show the output
cv2.imshow("Output", img)
cv2.waitKey(0)