# BareLSB

"Steganography is one of the most powerful techniques to conceal the existence of hidden secret data inside a cover object. Images are the most popular cover objects for Steganography and in this work image steganography is adopted.

There are several techniques to conceal information inside cover-image. The spatial domain techniques manipulate the cover-image pixel bit values to embed the secret information. The secret bits are written directly to the cover image pixel bytes. Consequently, the spatial domain techniques are simple and easy to implement. The Least Significant Bit (LSB) is one of the main techniques in spatial domain image steganography." ([Champakamala](http://ijact.org/volume3issue4/IJ0340004.pdf))

``` python
import cv2
from BareLSB import BareLSB

text = "Lorem ipsum dolor sit amet, ..." # Text to hide

Steg = BareLSB(cv2.imread('0.jpg')) # Initialize with image
Steg.addStr(text) # Add secret text

Steg = BareLSB(Steg.image) # New instance initilized with modified image
print(Steg.getText()) # Get text from modified image
```
