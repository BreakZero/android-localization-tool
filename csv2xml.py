import xml.etree.ElementTree as ET
import csv
import sys
import os

import xml.dom.minidom as minidom

def prettify_xml(elem: ET.Element) -> str:
    """Convert an ElementTree element into a pretty-printed XML string with indentation."""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

def generate_strings_xml_from_csv(csv_path, output_dir):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        if 'Key' not in fieldnames:
            raise ValueError("The first column of the CSV must contain 'Key'")

        lang_data = {lang: [] for lang in fieldnames if lang != 'Key'}

        for row in reader:
            key = row['Key']
            for lang in lang_data:
                value = row[lang]
                lang_data[lang].append((key, value))

    for lang, items in lang_data.items():
        resources = ET.Element('resources')
        for key, value in items:
            string = ET.SubElement(resources, 'string')
            string.set('name', key)
            string.text = value

        pretty_xml_bytes = prettify_xml(resources)

        dir_path = os.path.join(output_dir, f'values-{lang}')
        os.makedirs(dir_path, exist_ok=True)
        xml_path = os.path.join(dir_path, 'strings.xml')
        with open(xml_path, 'wb') as f:
            f.write(pretty_xml_bytes)

        print(f'✅ Generate File：{xml_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("❗Usage: python script.py <输入CSV路径> <输出目录>")
        print("📌Example: python generate.py translations.csv output")
        sys.exit(1)

    csv_file = sys.argv[1]
    out_dir = sys.argv[2]

    generate_strings_xml_from_csv(csv_file, out_dir)
