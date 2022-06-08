from xml.etree import ElementTree as et

classes = ["background",
			"aeroplane",
			"bicycle",
			"bird",
			"boat",
			"bottle",
			"bus",
			"car",
			"cat",
			"chair",
			"cow",
			"diningtable",
			"dog",
			"horse",
			"motorbike",
			"person",
			"pottedplant",
			"sheep",
			"sofa",
			"train",
			"tvmonitor"]
labels = []
boxes = []
tree = et.parse("object_det/pascal_test/VOCdevkit/VOC2007/Annotations/000001.xml")
root = tree.getroot()
print(root)
for member in root.findall('object'):
	labels.append(classes.index(member.find('name').text))
	# xmin = left corner x-coordinates
	xmin = int(member.find('bndbox').find('xmin').text)
	# xmax = right corner x-coordinates
	xmax = int(member.find('bndbox').find('xmax').text)
	# ymin = left corner y-coordinates
	ymin = int(member.find('bndbox').find('ymin').text)
	# ymax = right corner y-coordinates
	ymax = int(member.find('bndbox').find('ymax').text)
			
			# resize the bounding boxes according to the...
			# ... desired `width`, `height`
	xmin_final = (xmin/1)*1
	xmax_final = (xmax/1)*1
	ymin_final = (ymin/1)*1
	yamx_final = (ymax/1)*1
			
	boxes.append([xmin_final, ymin_final, xmax_final, yamx_final])
print(labels)
print(boxes)