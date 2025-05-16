import os
import xml.etree.ElementTree as ET
import csv
import sys

def strings_xml_to_csv(input_xml_path, output_csv_path):
    tree = ET.parse(input_xml_path)
    root = tree.getroot()

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Key', 'Value'])

        for elem in root:
            if elem.tag == 'string':
                writer.writerow([elem.attrib['name'], elem.text or ''])
            elif elem.tag == 'string-array':
                for i, item in enumerate(elem.findall('item')):
                    key = f"{elem.attrib['name']}[{i}]"
                    writer.writerow([key, item.text or ''])

def batch_convert_folder(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.xml'):
                input_path = os.path.join(root, file)

                # 构造输出路径
                relative_path = os.path.relpath(input_path, input_folder)
                relative_dir = os.path.dirname(relative_path)
                output_dir = os.path.join(output_folder, relative_dir)
                output_path = os.path.join(output_dir, file.replace('.xml', '.csv'))

                print(f"📄 Transfer: {input_path} → {output_path}")
                strings_xml_to_csv(input_path, output_path)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python batch_convert_xml2csv.py inputDir outputDir")
        print("Example: python batch_convert_xml2csv.py res csv_out")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    batch_convert_folder(input_dir, output_dir)
