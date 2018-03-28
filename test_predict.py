from unet import *
from data import *
import xlsxwriter
import os
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import cv2

myunet = myUnet()

model = myunet.get_unet()

model.load_weights('unet.hdf5')

#imgs_mask_test = model.predict(imgs_test, verbose=1)

#np.save('imgs_mask_test.npy', imgs_mask_test)
#imgs = np.load('imgs_mask_test.npy')
#for i in range(imgs.shape[0]):
#			img = imgs[i]
#			img = array_to_img(img)
#			img.save("%d.jpg"%(i))
workbook = xlsxwriter.Workbook('result.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_default_row(50)
list_files = glob.glob('/Users/qphuong/Cinnamon/unet/data/test/resize_test/*.png')

for index ,filename in enumerate(list_files):
	
	worksheet.insert_image(index,1, filename,{'x_scale': 0.25, 'y_scale': 0.25})

	img = load_img(filename ,grayscale = True,target_size=(128, 256))

	img = img_to_array(img)
	imgdatas = np.ndarray((1,128,256,1), dtype=np.uint8)
	imgdatas[0] = img
	basename =  os.path.basename(filename)

	predicted_image = model.predict(imgdatas, verbose=1)
	result = array_to_img(predicted_image[0])
	result.save(str(index)+'.png')
	im = cv2.imread(str(index)+'.png')
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,127,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	worksheet.insert_image(index,3, str(index)+'.png',{'x_scale': 0.25, 'y_scale': 0.25})
	worksheet.write(index,5,len(contours))
workbook.close()