import requests
import shutil
import os
import gdown
from acdh_tei_pyutils.tei import TeiReader
from config import (
    SOURCE_DOC_GIDS,
    CONVERSION_DOMAIN,
    TMP_DIR,
    SOURCE_DOCX_BASE_URL
)

def setup_dirs():
    shutil.rmtree(TMP_DIR, ignore_errors=True)
    os.makedirs(TMP_DIR, exist_ok=True)


def download_all_docxfiles():
    # download all specified docx-files from google
    docpaths = []
    for gdoc_source_id, docname in SOURCE_DOC_GIDS.items():
        gdoc_doc_url = f"{SOURCE_DOCX_BASE_URL}{gdoc_source_id}"
        local_save_path = f"{TMP_DIR}/{docname}.docx"
        print(f"start download from {gdoc_doc_url} to {local_save_path}")
        gdown.download(gdoc_doc_url, local_save_path)
        if os.path.isfile(local_save_path):
            print(f"saved {local_save_path}")
            docpaths.append(local_save_path)
    return docpaths


def request_xml_doc(docx_path):
    print(f"posting {docx_path} to {CONVERSION_DOMAIN}")
    headers = {
        "accept": "application/octet-stream",
    }
    params = {
        #"properties": '<conversions><conversion index="0"><property id="oxgarage.getImages">false</property><property id="oxgarage.getOnlineImages">false</property><property id="oxgarage.lang">en</property><property id="oxgarage.textOnly">true</property><property id="pl.psnc.dl.ege.tei.profileNames">default</property></conversion></conversions>', # noqa
        "properties": '<conversions><conversion index="0"><property id="oxgarage.getImages">false</property><property id="oxgarage.getOnlineImages">false</property><property id="oxgarage.lang">de</property><property id="oxgarage.textOnly">true</property><property id="pl.psnc.dl.ege.tei.profileNames">default</property></conversion><conversion index="1"></conversion></conversions>'
    }
    files = {"fileToConvert": open(docx_path, "rb")}
    response = requests.post(
        #f"{CONVERSION_DOMAIN}ege-webservice/Conversions/docx%3Aapplication%3Avnd.openxmlformats-officedocument.wordprocessingml.document/TEI%3Atext%3Axml", # noqa
        f"{CONVERSION_DOMAIN}ege-webservice/Conversions/docx%3Aapplication%3Avnd.openxmlformats-officedocument.wordprocessingml.document/TEI%3Atext%3Axml/Simple%3Atext%3Axml/",
        params=params,
        headers=headers,
        files=files,
    )
    data = response.content.decode("utf-8")
    data = data.replace("heading=h.", "heading_h_")
    data = data.replace('xml:id="', 'xml:id="xmlid__')
    resulting_xml_path = docx_path.replace('.docx', '.xml')
    print(f"saving result as {resulting_xml_path}")
    with open(resulting_xml_path, "w") as f:
        f.write(data)
    xml_doc = TeiReader(data)
    # setting file attrib to path
    xml_doc.file = resulting_xml_path
    return xml_doc


def convert_local_docx(docx_paths):
    xml_docs = []
    for docx_path in docx_paths:
        xml_doc = request_xml_doc(docx_path)
        xml_docs.append(xml_doc)
    return xml_docs


def create_xml_files():
    """
    downloads docx files from 
    google-docs, converts them 
    to xml and stores them in tmp.
    Returns list of tei-reader-docs
    created in this process.
    """
    setup_dirs()
    docx_paths = download_all_docxfiles()
    xml_docs = convert_local_docx(docx_paths)
    return xml_docs


if __name__ == "__main__":
    setup_dirs()
    docx_paths = download_all_docxfiles()
    xml_docs = convert_local_docx(docx_paths)