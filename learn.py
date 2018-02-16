import numpy as np
import cv2
from create_feature import *
from calorie_calc import *
import csv

svm_params = dict( kernel_type = cv2.SVM_LINEAR, svm_type = cv2.SVM_C_SVC, C=2.67, gamma=5.383 )


def training():
	feature_mat = []
	response = []
	for j in [1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
		for i in range(1,21):
			print "../Dataset/images/All_Images/"+str(j)+"_"+str(i)+".jpg"
			fea, farea, skinarea, fcont, pix_to_cm = readFeatureImg("../Dataset/images/All_Images/"+str(j)+"_"+str(i)+".jpg")
			feature_mat.append(fea)
			response.append(float(j))

	trainData = np.float32(feature_mat).reshape(-1,94)
	responses = np.float32(response)

	svm = cv2.SVM()
	svm.train(trainData,responses, params=svm_params)
	svm.save('svm_data.dat')	

def testing():
	svm_model = cv2.SVM()
	svm_model.load('svm_data.dat')
	feature_mat = []
	response = []
	image_names = []
	pix_cm = []
	fruit_contours = []
	fruit_areas = []
	fruit_volumes = []
	fruit_mass = []
	fruit_calories = []
	skin_areas = []
	fruit_calories_100grams = []
	for j in [1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
		for i in range(21,26):	
			img_path = "../Dataset/images/Test_Images/"+str(j)+"_"+str(i)+".jpg"
			print img_path
			fea, farea, skinarea, fcont, pix_to_cm = readFeatureImg(img_path)
			pix_cm.append(pix_to_cm)
			fruit_contours.append(fcont)
			fruit_areas.append(farea)
			feature_mat.append(fea)
			skin_areas.append(skinarea)
			response.append([float(j)])
			image_names.append(img_path)

	testData = np.float32(feature_mat).reshape(-1,94)
	responses = np.float32(response)
	result = svm_model.predict_all(testData)
	mask = result==responses

	#calculate calories
	for i in range(0, len(result)):
		volume = getVolume(result[i], fruit_areas[i], skin_areas[i], pix_cm[i], fruit_contours[i])
		mass, cal, cal_100 = getCalorie(result[i], volume)
		fruit_volumes.append(volume)
		fruit_calories.append(cal)
		fruit_calories_100grams.append(cal_100)
		fruit_mass.append(mass)

	#write into csv file
	with open('output.csv', 'w') as outfile:
		writer = csv.writer(outfile)
		data = ["Image name", "Desired response", "Output label", "Volume (cm^3)", "Mass (grams)", "Calories for food item", "Calories per 100 grams"]
		writer.writerow(data)
		for i in range(0, len(result)):
			if (fruit_volumes[i] == None):
				data = [str(image_names[i]), str(responses[i][0]), str(result[i][0]), "--", "--", "--", str(fruit_calories_100grams[i])]
			else:
				data = [str(image_names[i]), str(responses[i][0]), str(result[i][0]), str(fruit_volumes[i]), str(fruit_mass[i]), str(fruit_calories[i]), str(fruit_calories_100grams[i])]
			writer.writerow(data)
		outfile.close()
	
	for i in range(0, len(mask)):
		if mask[i][0] == False:	
			print "(Actual Reponse)", responses[i][0], "(Output)", result[i][0], image_names[i]

	correct = np.count_nonzero(mask)
	print correct*100.0/result.size

	

if __name__ == '__main__':
	training()
	testing()


