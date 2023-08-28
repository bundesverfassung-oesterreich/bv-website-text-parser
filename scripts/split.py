import os
import shutil
import lxml.etree as ET
import glob
from acdh_tei_pyutils.tei import TeiReader
from config import TEI_DIR, TMP_DIR

def setup_tei_dir():
    shutil.rmtree(TEI_DIR, ignore_errors=True)
    os.makedirs(TEI_DIR, exist_ok=True)

if __name__ == "__main__":
    xml_files_from_tmp = glob.glob(
        f"{TMP_DIR}/*.mxl"
    )
    if xml_files_from_tmp:
        setup_tei_dir()
        for xml_filepath in xml_files_from_tmp:
            shutil.copy(xml_filepath, TEI_DIR)

