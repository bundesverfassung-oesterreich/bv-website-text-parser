import glob
import os
import shutil

from lxml import etree as ET

from config import TEI_DIR


BASE_TEI_DIR = "./tmp/base-tei"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"


def setup_tei_dir():
    print("setting up tei-dir")
    shutil.rmtree(TEI_DIR, ignore_errors=True)
    os.makedirs(TEI_DIR, exist_ok=True)


def normalize_raw_xml(text):
    # Keep legacy normalization rules from the previous conversion pipeline.
    text = text.replace("heading=h.", "heading_h_")
    text = text.replace('xml:id="', 'xml:id="xmlid__')
    return text


def dedupe_xml_ids(root):
    seen = {}
    for elem in root.iter():
        xml_id = elem.attrib.get(XML_ID)
        if not xml_id:
            continue
        count = seen.get(xml_id, 0)
        if count > 0:
            elem.attrib[XML_ID] = f"{xml_id}__{count + 1}"
        seen[xml_id] = count + 1


def normalize_rend_to_rendition(root):
    for elem in root.iter():
        rend = elem.attrib.get("rend")
        if not rend:
            continue
        if "rendition" not in elem.attrib:
            elem.attrib["rendition"] = rend
        del elem.attrib["rend"]


def process_local_xmls():
    source_files = sorted(glob.glob(f"{BASE_TEI_DIR}/*.xml"))
    if not source_files:
        raise FileNotFoundError(f"No xml files found in {BASE_TEI_DIR}")

    setup_tei_dir()
    for xml_filepath in source_files:
        print(f"processing xml of {xml_filepath}")
        with open(xml_filepath, "r", encoding="utf-8") as f:
            data = normalize_raw_xml(f.read())

        parser = ET.XMLParser(recover=True, remove_blank_text=False, huge_tree=True)
        root = ET.fromstring(data.encode("utf-8"), parser=parser)
        dedupe_xml_ids(root)
        normalize_rend_to_rendition(root)

        xml_filename = os.path.basename(xml_filepath)
        new_xml_filepath = f"{TEI_DIR}/{xml_filename}"
        print(f"saving final file to {new_xml_filepath}")
        tree = ET.ElementTree(root)
        tree.write(new_xml_filepath, encoding="utf-8", pretty_print=True, xml_declaration=True)


if __name__ == "__main__":
    process_local_xmls()