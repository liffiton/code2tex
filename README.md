# Code2Tex

Code2tex was created to aid in grading programming assignments.  It takes
source code and inserts it into a simple LaTeX document from which a PDF can be
made.  This provides a document with syntax highlighting and clear headings for
each file that can be marked up and returned to the students.

## Usage

Its usage is fairly basic; simply run `code2tex.py` followed by any number of
filenames.  It will output the LaTeX document to standard out, which may be
redirected to a file:

    ./code2tex.py file [file [file [...]]] > output.tex

This will create `output.tex`, ready to pass to `latex` or `pdflatex`.  For
example, if a student with user id "jsmith" submitted several java files:

    ./code2tex.py jsmith*.java > jsmith.tex
    pdflatex jsmith.tex

This would create a PDF named `jsmith.pdf` containing the contents of all
`jsmith*.java` files, nicely formatted with syntax highlighting and a separate
header for each.

See the `hello_worlds` folder for an example; `hello_world.tex` and
`hello_world.pdf` were created from the various "Hello, World!" programs in
that directory.  The syntax highlighter recognizes a wide variety of
programming languages.

### convert_all.py

To quickly convert all user submissions downloaded from a Moodle assignment:
 1. Use the "Download all submissions" option in Moodle and extract the resulting zip file.
 2. run `convert_all.py <directory>` where `<directory>` is the directory with the unzipped files.

The script will attempt to create PDFs from all the files. It parses the filenames constructed from Moodle and outputs PDFs named "First\_Last\_ID\_files.pdf".

## Dependencies

The simple python script has no dependencies.

Producing a PDF of the LaTeX output requires LaTeX, however.  Code2tex's output
depends on a few packages that are not always included by default in a LaTeX
install; in Ubuntu, for example, you'll need to install the following packages
(along with their dependencies):

    texlive-fonts-recommended
    texlive-latex-extra
    texlive-latex-extra-doc
    texlive-math-extra
    texlive-pictures-doc

Install these with the following command:

    sudo apt-get install texlive-fonts-recommended texlive-latex-extra texlive-latex-extra-doc texlive-math-extra texlive-pictures-doc

On other systems, you will need to find the correct packages.  Look for
"[latex]-extra" and "math-extra" packages.

## Marking up PDFs

Once you have a PDF, various software can be used to mark it up.  I and my TAs
have had success with [PDF-XChange
Viewer](http://www.tracker-software.com/product/pdf-xchange-viewer), the best
free Windows software I've found for annotating PDFs.  It has a wide range of
tools for creating text boxes, circling things, pointing with arrows, etc.  In
Linux, [Xournal](http://xournal.sourceforge.net/) is a decent option.  Please
let me know if you find other applications that work well for this.

