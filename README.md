# Code2Tex

Addition to Mark Liffiton's code2tex project allowing quick conversion of all files when using the "Download all submissions" option.

## Usage

1. Use "Download all submissions" option in Moodle and extract the zip file.
2. run `convert\_all.py <directory>` where `<directory>` is the directory with the unzipped files.

The script will attempt to create PDFs from all the files. It parses the filenames constructed from Moodle and outputs PDFs named "First Last\_ID_files.pdf".
