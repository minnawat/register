import PIL
from PIL import Image
import pytesseract
import cv2 as cv
from PIL import ImageDraw
from kraken import pageseg


def crop_with_resize(image, faces):
    first = True
    faces_arrays = []
    for (x,y,w,h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv.cvtColor(face, cv.COLOR_BGR2RGB)
        pil_face = Image.fromarray(face)
        if first:
            height = pil_face.height
            width = pil_face.width
            first = False
        pil_face = pil_face.resize((width, height))
        faces_arrays.append(pil_face)
    return faces_arrays

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
keyword = input("input word you want to search: ")
# the rest is up to you!
#file_zip = "readonly/small_img.zip"

'''with ZipFile(file_zip, 'r') as zip:

    print('Extracting all the files now...')
    zip.extractall
    print('Done!')'''
for i in range(0,4):
    print("at a-" + str(i) + ".png right now")
    im = Image.open("a-" + str(i) + ".png")
    text = pytesseract.image_to_string(Image.open("a-" + str(i) + ".png"))
    print("image to string complete")
    cv_img=cv.imread("a-" + str(i) + ".png")
    if keyword in text:
        print("checking faces right now")
        faces = face_cascade.detectMultiScale(cv_img,1.35)
        #print ("Found: {0} faces.".format(len(faces)))
        print("Result found in file a-" + str(i) + ".png")
        if len(faces) > 0:
            #display(faces)
            crop_img = crop_with_resize(cv_img,faces)
            #display(crop_img)
            first_image=crop_img[0]
            contact_sheet=PIL.Image.new('RGB', (first_image.width*5,first_image.height*2))
            x=0
            y=0

            for img in crop_img:
                # Lets paste the current image into the contact sheet
                contact_sheet.paste(img, (x, y) )
                # Now we update our X position. If it is going to be the width of the image, then we set it to 0
                # and update Y as well to point to the next "line" of the contact sheet.
                if x+first_image.width == contact_sheet.width:
                    x=0
                    y=y+first_image.height
                else:
                    x=x+first_image.width

            # resize and display the contact sheet
            contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
            display(contact_sheet)
        else:
            print("but there is no face in that file!")