import xml.etree.ElementTree as ET
import sys


def get_float(node, path):
    return float(get_text(node, path))


def get_text(node, path):
    return node.findall(path)[0].text


tree = ET.parse(sys.argv[1])
root = tree.getroot()
filename = get_text(root, "./filename")

width = get_float(root, "./size/width")
height = get_float(root, "./size/height")

with open('bbs.csv', 'w') as csv_file:
    tags = root.findall("./object")
    for tag in tags:
        xmin = get_float(tag, "./bndbox/xmin")
        ymin = get_float(tag, "./bndbox/ymin")
        xmax = get_float(tag, "./bndbox/xmax")
        ymax = get_float(tag, "./bndbox/ymax")
        name = get_text(tag, "./name")

        top_left = f'{(xmin/ width)},{(ymax / height)}'
        bottom_right = f'{(xmax / width)},{(ymin / height)}'

        csv_file.write(f'UNASSIGNED,gs://autoset-vcm/annotated-photos/images/{filename},{name},{top_left},,,{bottom_right},,\n')
