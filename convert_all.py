#!/usr/bin/env python3

import code2tex
import os
import re
import subprocess
import sys


def main():
    if len(sys.argv) != 2:
        sys.exit('''Usage: %s [DIRECTORY]
 Outputs .tex file to CWD
 Languages (for syntax highlighting) determined from file extensions.''' % (sys.argv[0],))

    # Check existence of folder
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        sys.exit("Directory not found: %s" % directory)

    matched = []
    not_matched = []

    pattern = re.compile(r".*/(.+?_\d+)_assignsubmission_file_(.*)$")

    for item in os.listdir(directory):
        item = os.path.join(directory, item)
        # Each student's submissions are stored in a separate directory
        if not os.path.isdir(item):
            continue

        match = re.match(pattern, item)
        if match:
            matched.append((match.group(1), item))
        else:
            not_matched.append(item)

    for name, dir in matched:
        output_file_name = (name + "_files.tex").replace(" ", "_")
        output_file = open(output_file_name, "w")

        code2tex.makeTop(output_file)
        for file in os.listdir(dir):
            full_file_path = os.path.join(dir, file)
            code2tex.addListing(full_file_path, file, output_file)
        code2tex.makeBottom(output_file)

        output_file.close()

        # Convert to PDF
        print("[32m{}[m".format(output_file_name))
        subprocess.call(["pdflatex", "-interaction=batchmode", output_file_name])

    print()
    print("CONVERTED FILES FOR NAMES")
    for name, _ in matched or [("---None---", "")]:
        print(name)
    print()
    print("FILES NOT MATCHED")
    for file in not_matched or ["---None---"]:
        print(file)


if __name__ == "__main__":
    main()
