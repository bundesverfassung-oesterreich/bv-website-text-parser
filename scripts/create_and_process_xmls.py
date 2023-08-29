# # import lxml.etree as ET
import os
import shutil
from config import TEI_DIR
from download_docx import create_xml_files, TeiReader

def setup_tei_dir():
    print("setting up tei-dir")
    shutil.rmtree(TEI_DIR, ignore_errors=True)
    return os.makedirs(TEI_DIR, exist_ok=True)

if __name__ == "__main__":
    xml_docs = create_xml_files()
    setup_tei_dir()
    for doc in xml_docs:
        doc: TeiReader
        # explitly setting doc.file to path in download_docx.request_xml_doc
        xml_filepath = doc.file
        print(f"processing xml of {xml_filepath}")
        # # do something with it
        # # 
        xml_filename = xml_filepath.split("/")[-1]
        new_xml_filepath = f"{TEI_DIR}/{xml_filename}"
        print(f"saving final file to {new_xml_filepath}")
        doc.tree_to_file(new_xml_filepath)