# Calorie-estimation-from-food-images-opencv
An ML model which is trained to recognise food images, calculate volume and estimate calorie content
May 13, 2016

To Run: python learn.py  
learn.py calls two functions - training and testing. Once training is done, the model gets saved as a file. The same model is used for testing on a different set of images.

Description:
A set of 10 classes of food items were used. We use various image processing and classification techniques to identify the food, calculate the volume and the nutritional content. A mixture of methods including canny edge detection, watershed segmentation, morphological operators and Otsu’s method were used to segment the food item to obtain the contour of the fruit and the contour of the thumb. We use the thumb finger for calibration purposes. The thumb is placed next to the dish while clicking the photo and this thumb gives us the estimate of the real-life size of the food item and helps estimate volume accurately. 

Once the food item is extracted from the image, we extract the feature vector of the image for training/testing purposes. The feature vector is calculated by using hsv histogram for color features, Gabor filters for texture features, and hu moments for shape, and the area for size. The feature vector is a 95x1 dimensional vector. We used Support Vector Machine model
for training the images using our 95 dimensional feature vector. We obtained an accuracy of 94% in the classification of food item.

Once the food item is identified, we were able to calculate the volume of food items by approximating it to a geometric shape like
sphere, cylinder, etc. Once we have the volume, the mass of the food item is calculated using standard density tables. Using already available information of nutritional content of the given class of food, the total calorie content in the food image can be estimated.
