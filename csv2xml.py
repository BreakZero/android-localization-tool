import csv
import sys
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from collections import defaultdict

def prettify_xml(elem: ET.Element) -> bytes:
    """Convert an ElementTree element into a pretty-printed XML byte string with indentation."""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

def generate_strings_xml_from_csv(csv_path, output_dir):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

        if 'Key' not in fieldnames:
            raise ValueError("The first column of the CSV must contain 'Key'")

        # Prepare dictionary: lang -> { normal strings, array strings }
        lang_strings = {lang: {} for lang in fieldnames if lang != 'Key'}
        lang_arrays = {lang: defaultdict(dict) for lang in fieldnames if lang != 'Key'}

        for row in reader:
            key = row['Key']
            for lang in lang_strings:
                value = row[lang].strip()
                if not value:
                    continue

                if '[' in key and key.endswith(']'):
                    base, index = key.rsplit('[', 1)
                    index = int(index.rstrip(']'))
                    lang_arrays[lang][base][index] = value
                else:
                    lang_strings[lang][key] = value

    # Generate strings.xml for each language
    for lang in lang_strings:
        resources = ET.Element('resources')

        # Add normal <string> elements
        for key, val in lang_strings[lang].items():
            string = ET.SubElement(resources, 'string')
            string.set('name', key)
            string.text = val

        # Add <string-array> elements
        for array_name, items in lang_arrays[lang].items():
            arr = ET.SubElement(resources, 'string-array')
            arr.set('name', array_name)
            for i in sorted(items.keys()):
                item = ET.SubElement(arr, 'item')
                item.text = items[i]

        # Write prettified XML to file
        pretty_xml_bytes = prettify_xml(resources)
        lang_dir = os.path.join(output_dir, f'values-{lang}')
        os.makedirs(lang_dir, exist_ok=True)
        xml_path = os.path.join(lang_dir, 'strings.xml')

        with open(xml_path, 'wb') as f:
            f.write(pretty_xml_bytes)

        print(f'✅ Generate File: {xml_path}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("❗Usage: python script.py <输入CSV路径> <输出目录>")
        print("📌Example: python generate.py translations.csv output")
        sys.exit(1)

    csv_file = sys.argv[1]
    out_dir = sys.argv[2]

    generate_strings_xml_from_csv(csv_file, out_dir)
