from download_docx import download_all_docxfiles, setup_dirs


def main():
    setup_dirs()
    paths = download_all_docxfiles()
    if not paths:
        raise RuntimeError("No DOCX files downloaded")


if __name__ == "__main__":
    main()
