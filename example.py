import cv2
from BareLSB import BareLSB

text = "Lorem ipsum dolor sit amet, ..."

image_array = cv2.imread('0.jpg')

Steg = BareLSB(image_array)
Steg.addStr(text)

steg_image = Steg.image

Steg = BareLSB(steg_image)
print(Steg.getText())

cv2.imshow('Modified', Steg.image)
cv2.imshow('Original', image_array)
cv2.waitKey(5000)
cv2.destroyAllWindows()
