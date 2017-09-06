import os
import numpy as np
from PIL import Image


def preprocess(raw_img):
	data = np.empty((1,3, 187, 100), dtype="float32")	

	img = raw_img.resize((100,187))
	width, height=img.size

	r=np.zeros((187,100),dtype=float)
	g=np.zeros((187,100),dtype=float)
	b=np.zeros((187,100),dtype=float)

	for y in range(height):
		for x in range(width):
			rgb = img.getpixel((x,y))
			rgb=(rgb[0],rgb[1],rgb[2],);

			r[y][x]=rgb[0]
			g[y][x]=rgb[1]
			b[y][x]=rgb[2]
	AImg=[r,g,b]
	arr = np.asarray(AImg, dtype="float32")
	data[0, :, :, :] = arr

	return data



