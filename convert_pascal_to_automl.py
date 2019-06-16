import xml.etree.ElementTree as ET
import sys
import glob


def get_float(node, path):
    return float(get_text(node, path))


def get_text(node, path):
    return node.findall(path)[0].text


def convert_folder(folder_name, csv_file):
    file_names = [f for f in glob.glob(f'{folder_name}*.xml')]
    for file_name in file_names:
        convert_file(file_name, csv_file)


def convert_file(file_name, csv_file):
    tree = ET.parse(file_name)
    root = tree.getroot()
    filename = get_text(root, "./filename")

    width = get_float(root, "./size/width")
    height = get_float(root, "./size/height")

    tags = root.findall("./object")
    for tag in tags:
        xmin = get_float(tag, "./bndbox/xmin")
        ymin = get_float(tag, "./bndbox/ymin")
        xmax = get_float(tag, "./bndbox/xmax")
        ymax = get_float(tag, "./bndbox/ymax")
        name = get_text(tag, "./name")

        top_left = f'{(xmin/ width)},{(ymax / height)}'
        bottom_right = f'{(xmax / width)},{(ymin / height)}'

        csv_file.write(f'UNASSIGNED,gs://annotated-photos/images/{filename},{name},{top_left},,,{bottom_right},,\n')


if __name__ == "__main__":
    with open('bbs.csv', 'w') as csv_file:
        convert_folder(sys.argv[1], csv_file)

