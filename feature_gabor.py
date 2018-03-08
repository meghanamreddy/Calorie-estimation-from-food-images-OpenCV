
import numpy as np
import cv2
from multiprocessing.pool import ThreadPool


def build_filters():
    '''
    The Gabor kernel is calculated, which is later used to calculate the gabor features of an image
    '''
    filters = []
    ksize = 31
    for theta in np.arange(0, np.pi, np.pi / 8):
	for wav in [ 8.0, 13.0]:
		for ar in [0.8, 2.0]:
        		kern = cv2.getGaborKernel((ksize, ksize), 5.0, theta, wav, ar, 0, ktype=cv2.CV_32F)
			filters.append(kern)
    cv2.imshow('filt', filters[9])
    return filters
	
def process_threaded(img, filters, threadn = 8):
    accum = np.zeros_like(img)
    def f(kern):
        return cv2.filter2D(img, cv2.CV_8UC3, kern)
    pool = ThreadPool(processes=threadn)
    for fimg in pool.imap_unordered(f, filters):
        np.maximum(accum, fimg, accum)
    return accum

def EnergySum(img):
	mean, dev = cv2.meanStdDev(img)
	return mean[0][0], dev[0][0]
	
def process(img, filters):
    '''
    Given an image and gabor filters,
    the gabor features of the image are calculated.
    '''
    feature = []
    accum = np.zeros_like(img)
    for kern in filters:
    	fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)  
        a, b = EnergySum(fimg)
        feature.append(a)
        feature.append(b)
    	np.maximum(accum, fimg, accum)
    
    M = max(feature)
    m = min(feature)
    feature = map(lambda x: x * 2, feature)
    feature = (feature - M - m)/(M - m);
    mean=np.mean(feature)
    dev=np.std(feature)
    feature = (feature - mean)/dev;
    return feature

def getTextureFeature(img):
    '''
    Given an image, the gabor filters are calculated and
    then the texture features of the image are calculated
    '''
    filters = build_filters()
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res1 = process(gray_image, filters)
    return res1

if __name__ == '__main__':
    import sys
    #from common import Timer
    print __doc__
    try: img_fn = sys.argv[1]

    except: img_fn = 'test.JPG'
    img = cv2.imread(img_fn)
    
    print getTextureFeature(img)
   
    cv2.waitKey()
    cv2.destroyAllWindows()
