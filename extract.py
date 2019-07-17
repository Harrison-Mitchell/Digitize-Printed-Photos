import cv2, os
import numpy as np
from math import hypot

# Easier to ask forgiveness than permission
try: os.mkdir("Out")
except: pass
try: os.mkdir("Failed")
except: pass

# Up to you to find your own value, all setups will be different
CANNY_UPPER = # If you must, here's what worked for my batch: 200
THRESHOLD = # 70

def extract (path):
	# Load our image, make it black and white to find edges easier, then find lines from edges
	img = cv2.imread(path, cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray, 50, CANNY_UPPER)
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, THRESHOLD, minLineLength=30, maxLineGap=250)

	# Set up vars: Points e.g Top Right Point, Distances: Bottom Left Distance, height, width
	trp, tlp, brp, blp = [(999999,999999)]*4
	trd, tld, brd, bld = [999999]*4
	h, w, _ = img.shape
	points = []

	# Get all the points found from the line detection algo
	for line in lines:
		x1, y1, x2, y2 = line[0]
		points.append((x1, y1))
		points.append((x2, y2))

	# For each point, check if it's the furthest to one of the image corners (to find outer rect)
	for point in points:
		trdl = hypot(w-point[0], 0-point[1])
		if trdl < trd: trd = trdl; trp = point
		tldl = hypot(0-point[0], 0-point[1])
		if tldl < tld: tld = tldl; tlp = point
		brdl = hypot(w-point[0], h-point[1])
		if brdl < brd: brd = brdl; brp = point
		bldl = hypot(0-point[0], h-point[1])
		if bldl < bld: bld = bldl; blp = point

	# # # Wacky perspective correction magic 
	rect = np.zeros((4, 2), dtype = "float32")
	rect[0], rect[1], rect[2], rect[3] = (tlp,trp,brp,blp)
	widthA = np.sqrt(((brp[0] - blp[0]) ** 2) + ((brp[1] - blp[1]) ** 2))
	widthB = np.sqrt(((trp[0] - tlp[0]) ** 2) + ((trp[1] - tlp[1]) ** 2))
	heightA = np.sqrt(((trp[0] - brp[0]) ** 2) + ((trp[1] - brp[1]) ** 2))
	heightB = np.sqrt(((tlp[0] - blp[0]) ** 2) + ((tlp[1] - blp[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	maxHeight = max(int(heightA), int(heightB))
	dst = np.array([[0, 0],[maxWidth-1, 0],[maxWidth-1, maxHeight-1],[0, maxHeight-1]], dtype="float32")
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
	# # # https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/

	margin = int(0.01 * w) # If we want to trim to remove background seep from bent photos
	if trim: warp = warp[margin:-margin, margin:-margin] # Then crop thin border
	cv2.imwrite("Out/"+path.split("/")[-1], warp) # Successful extraction goes into Out folder

imDir = input("Image folder (relative path): ")
trim = True if input("Trim 1% of outside to reduce background seep? (y/n): ").lower() == "y" else False
for im in next(os.walk(imDir + "/"))[2]:
	try: extract(imDir + "/" + im) # Because if it fails to extract
	except: # We save it to the failed folder for a rerun
		print(imDir + "/" + im + " failed, you'll have to rerun with different values")
		os.rename(imDir + "/" + im, "Failed/" + im)