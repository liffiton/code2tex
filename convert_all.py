#!/usr/bin/python

import code2tex
import os
import re
import StringIO
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

    name_to_files = {}
    not_matched = []
    for item in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, item)):
            continue

        matches = re.findall("(.+?_\d+)_assignsubmission_file_(.+)$", item)

        if len(matches) == 0:
            not_matched.append(item)
        else:
            if matches[0][0] not in name_to_files:
                name_to_files[matches[0][0]] = []

            name_to_files[matches[0][0]].append(matches[0][1])

    for (name, files) in name_to_files.items():
        oldStdout = sys.stdout
        sys.stdout = out = StringIO.StringIO()

        code2tex.makeTop()
        for file in files:
            full_file_name = name + "_assignsubmission_file_" + file
            full_file_path = os.path.join(directory, full_file_name)

            code2tex.addListing(full_file_path, file)
        code2tex.makeBottom()

        sys.stdout = oldStdout

        output_file_name = name + "_files.tex"
        with open(output_file_name, "w") as output_file:
            output_file.write(out.getvalue())

        # Convert to PDF
        subprocess.call(["pdflatex", output_file_name])

    print "CONVERTED FILES FOR NAMES"
    for name in name_to_files.keys():
        print name
    print
    print "FILES NOT MATCHED"
    for file in not_matched:
        print file

if __name__ == "__main__":
    main()
