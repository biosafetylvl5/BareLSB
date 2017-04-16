import cv2
from BareLSB import BareLSB

text = "Lorem ipsum dolor sit amet, ..." # Text to hide

Steg = BareLSB(cv2.imread('0.jpg')) # Initialize with image
Steg.addStr(text) # Add secret text

Steg = BareLSB(Steg.image) # New instance initilized with modified image
print(Steg.getText()) # Get text from modified image

cv2.imshow('Modified', Steg.image)
cv2.imshow('Original', cv2.imread('0.jpg'))
print(Steg.image.all() == initial_image.all())
cv2.waitKey(5000)
cv2.destroyAllWindows()
