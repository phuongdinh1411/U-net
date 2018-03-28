from PIL import Image
import glob
import os
list_files = glob.glob('/Users/qphuong/Desktop/1.png')

for indexx ,filename in enumerate(list_files):
    im = Image.open(filename)
    width, height = im.size
    basename =  os.path.basename(filename)
    print(os.path.basename(filename), width, height)
    imB = im.resize((256, 128))
    imB.save('/Users/qphuong/Cinnamon/unet/data/test/resize_test/'+ basename ,'PNG')
    #imB.show()  
