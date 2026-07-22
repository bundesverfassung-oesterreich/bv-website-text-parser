# bv-commentary-parser
Creates tei-files from generic docx-files fetched from google-docs.
This is done to provide the basic introduction texts on the website.
Based on [grocerist](https://github.com/grocerist/grocerist-tei).

## usage

* `python scripts/download_docx.py` downloads docx from gdrive, converts it via oxgarage into an XML/TEI Document and saves it into `tmp/source.xml`
* `python scripts/split.py` splits `tmp/source.xml` in single XML/TEI files and enriches them with baserow-data

## Workflows

* `.github/workflows/make_teis.yml` is the old workflow.
    * It downloads source DOCX files from Google Drive to `tmp`.
    * It performs DOCX -> TEI base conversion via TEI-Garage.
    * It then runs local Python post-processing.
    * Processed output is written to `tei`.
* `.github/workflows/make_teis_local.yml` is the new simple local-conversion workflow.
    * It downloads source DOCX files from Google Drive to `tmp`.    
    * It performs DOCX -> TEI base conversion locally via the vendored TEI Stylesheets toolchain (`third_party/tei-stylesheets`) using Ant/XSLT.
    * The conversion logic is implemented in `scripts/convert_docx_to_base_tei.sh`.
    * It then runs local Python post-processing without any download step (`scripts/postprocess_local_xmls.py`).
    * Processed output is written to `tei`.

## Licensing

All code unless otherwise noted is licensed under the terms [MIT License](https://opensource.org/licenses/MIT).

This repository vendors third-party source code in `third_party/tei-stylesheets`.
See `THIRD_PARTY_NOTICES.md` and the included upstream license files for details.

For DOCX to TEI base conversion, the canonical in-repository toolchain source is
`third_party/tei-stylesheets`. The legacy bare `Stylesheets.git` folder is no
longer used.

For licensing information of the data in this repository, please look into the individual folders/files for further information.
