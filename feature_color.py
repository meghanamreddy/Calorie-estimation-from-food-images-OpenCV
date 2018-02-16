import cv2
import math
import sys
import numpy as np


#try: img_fn = sys.argv[1]
#   except: img_fn = 'test.jpg'
def getColorFeature(img):
	img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	h,s,v = cv2.split(img_hsv)
	
	hsvHist = [[[0 for _ in range(2)] for _ in range(2)] for _ in range(6)]
	
	featurevec = []
	hist = cv2.calcHist([img_hsv], [0, 1, 2], None, [6,2,2], [0, 180, 0, 256, 0, 256])	
	for i in range(6):
		for j in range(2):
			for k in range(2):
				featurevec.append(hist[i][j][k])
	feature = featurevec[1:]	
	M = max(feature)
   	m = min(feature)
    	feature = map(lambda x: x * 2, feature)
    	feature = (feature - M - m)/(M - m);
    	mean=np.mean(feature)
    	dev=np.std(feature)
    	feature = (feature - mean)/dev;

	return feature



if __name__ == '__main__':
	img = cv2.imread(sys.argv[1])
	featureVector = getColorFeature(img)
	print featureVector
	cv2.waitKey(0)
	cv2.destroyAllWindows()

