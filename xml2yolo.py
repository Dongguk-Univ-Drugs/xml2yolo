from xml.dom import minidom
import shutil
import os
import glob

lut = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 
    'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
    'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 
    'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 
    'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 
    'Z': 25, '1': 26, '2': 27, '3': 28, '4': 29, 
    '5': 30, '6': 31, '7': 32, '8': 33, '9': 34, '0': 35,
    'a': 36, 'b': 37, 'c': 38, 'd': 39, 'e': 40, 
    'f': 41, 'g': 42, 'h': 43, 'i': 45, 'j': 46,
    'k': 47, 'l': 48, 'm': 49, 'n': 50, 'o': 51, 
    'p': 52, 'q': 53, 'r': 54, 's': 55, 't': 56, 
    'u': 57, 'v': 58, 'w': 59, 'x': 60, 'y': 61, 
    'z': 62, '-': 63
}

def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_xml2yolo(lut, path, output):

    for fname in glob.glob(os.path.join(path, "*.xml")):
        xmldoc = minidom.parse(fname)
        fname_out = output+(fname[3:-4]+'.txt')

        with open(fname_out, "w") as f:
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "-1"
                    print ("warning: label '%s' not in look-up table" % classid)

                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert_coordinates((width,height), b)

                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print ("wrote %s" % fname_out)

def file_copy():
    here = os.path.dirname(os.path.realpath(__file__))
    xml_list = [file for file in os.listdir(here+"/tmp") if ".xml" in file]
    txt_list = [file for file in os.listdir(here+"/tmp") if ".txt" in file]
    image_list = [file for file in os.listdir(here+"/tmp") if ".jpg" in file]
    list(map(lambda file: shutil.copy("tmp/"+file, "xml_backup/"+file), xml_list))
    list(map(lambda file:shutil.copy("tmp/"+file, "result/"+file), txt_list))
    list(map(lambda file: shutil.copy("images/"+file, "result/"+file), image_list))
    list(map(lambda file: shutil.copy("images/"+file, "backup/"+file), image_list))
    for file in xml_list+txt_list+image_list:
        os.remove("tmp/"+file)

convert_xml2yolo(lut, "tmp", "result")
file_copy()
paths = glob.glob("backup/*.jpg")
with open("train.txt", "w") as f:
    for path in paths:
        path = path.replace("images", "data/obj").replace("\\", "/").replace("./", "")
        f.write(path + '\n')
