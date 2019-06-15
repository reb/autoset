import xml.etree.ElementTree as ET
import sys


tree  = ET.parse(sys.argv[1])
root = tree.getroot()
filename = root.findall("./filename")[0].text
tags = root.findall("./object")

width = float(root.findall("./size/width")[0].text)
height = float(root.findall("./size/height")[0].text)

with open('bbs.csv', 'w') as csv_file:
    for tag in tags:
        xmin = float(tag.findall("./bndbox/xmin")[0].text)
        ymin = float(tag.findall("./bndbox/ymin")[0].text)
        xmax = float(tag.findall("./bndbox/xmax")[0].text)
        ymax = float(tag.findall("./bndbox/ymax")[0].text)
        name = tag.findall("./name")[0].text

        top_left = f'{(xmin/ width)},{(ymax / height)}'
        bottom_right = f'{(xmax / width)},{(ymin / height)}'

        csv_file.write(f'UNASSIGNED,gs://autoset-vcm/annotated-photos/images/{filename},{name},{top_left},,,{bottom_right},,\n')
