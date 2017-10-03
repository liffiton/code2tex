#!/usr/bin/env python3

import re
import subprocess
import sys

from collections import defaultdict
from pathlib import Path

import code2tex


def main():
    if len(sys.argv) != 2:
        sys.exit('''Usage: %s [DIRECTORY]
 Outputs .tex files and generate PDFs in CWD
 Languages (for syntax highlighting) determined from file extensions.''' % (sys.argv[0],))

    # Check existence of folder
    directory = Path(sys.argv[1])
    if not directory.is_dir():
        sys.exit("Directory not found: %s" % directory)

    matched = defaultdict(list)
    not_matched = []

    # Regexes for matching various LMS filenames
    patterns = {}
    patterns['Moodle'] = re.compile(r"([^/]+?_\d+)_assignsubmission_file_/(.+)$")
    patterns['Canvas'] = re.compile(r"([^/]+?_\d+)_\d+_(.+)$")

    # Gather all files in directory
    files = directory.glob('**/*')

    # Match filenames against any LMS patterns, storing those that match
    for f in files:
        if f.is_dir():
            continue

        for pattern in patterns.values():
            match = re.search(pattern, str(f))
            if match:
                matchinfo = (str(f), match.group(2))
                matched[match.group(1)].append(matchinfo)
                break
        else:
            # triggered if end of for loop reached, break *not* used
            not_matched.append(str(f))

    # Output .tex and create PDFs for all matched files, grouped by name
    for name in matched:
        output_file_name = (name + "_files.tex").replace(" ", "_")
        output_file = open(output_file_name, "w")

        code2tex.makeTop(output_file)
        for fullpath, filename in matched[name]:
            code2tex.addListing(fullpath, filename, output_file)
        code2tex.makeBottom(output_file)

        output_file.close()

        # Convert to PDF
        print("[32m{}[m".format(output_file_name))
        subprocess.call(["pdflatex", "-interaction=batchmode", output_file_name])

    print()
    print("CONVERTED FILES FOR NAMES")
    for name in matched or ["---None---"]:
        print(name)
    print()
    print("FILES NOT MATCHED")
    for file in not_matched or ["---None---"]:
        print(file)


if __name__ == "__main__":
    main()
