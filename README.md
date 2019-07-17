# Digitize Printed Photos
Makes the best attempt of recovering photos saved only in physical form into digital form.

### Dependencies
* Python >= 3.5
* OpenCV2 (`pip install opencv-python`)
* Numpy (`pip install numpy`)

### Usage
Take high quality photos of your photos, one at a time, with a flat light source on a plain light colored background, as seen in the example below. Run the extraction script (`python3 extract.py`), provide photo directory when prompted and whether to trim background bleed. As seen in the bottom image below, pictures where the print is entirely flat will have some bending which will not be removed in the script. You can decide whether to retain 100% image information OR whether to produce "clean" photos.

### How's it work?
Performs photo simplification, converts to greyscale, performs edge detection, extrapolates lines from edges. From there, it finds the outermost lines of the image (the printed photo bounds), finds the corners, then performs perspective transformation to reconstruct the image from a "top down" perspective.

Example in photo

<img src="https://github.com/Harrison-Mitchell/Digitize-Printed-Photos/blob/master/examples/in.png" width="400">

Example out photo

<img src="https://github.com/Harrison-Mitchell/Digitize-Printed-Photos/blob/master/examples/out.png" width="400">

Example bend that can be removed

<img src="https://github.com/Harrison-Mitchell/Digitize-Printed-Photos/blob/master/examples/bend.png" width="400">
