#!/usr/bin/env python3

import sys
import re
# import os.path
from os import listdir, chdir
from pathlib import Path
from subprocess import call

# TODO: read extensions, header from files found in sys.path?

# A subset of the languages supported by the Listings latex package
# File extensions mapped to language names
exts = {
    "ada": "Ada",
    "adb": "Ada",
    "ads": "Ada",
    "awk": "Awk",
    "c": "C",
    "h": "C++",
    "hh": "C++",
    "hpp": "C++",
    "cxx": "C++",
    "cpp" : "C++" ,
    "caml" : "Caml" ,
    "ex" : "Euphoria" ,
    "exw" : "Euphoria" ,
    "f" : "Fortran" ,
    "for" : "Fortran" ,
    "f90" : "Fortran" ,
    "fpp" : "Fortran" ,
    "html" : "HTML" ,
    "xhtml" : "HTML" ,
    "has" : "Haskell" ,
    "hs" : "Haskell" ,
    "idl" : "IDL" ,
    "java" : "Java" ,
    # pde = Processing
    "pde" : "Java" ,
    "lsp" : "Lisp" ,
    "lgo" : "Logo" ,
    "ml" : "ML" ,
    "php" : "PHP" ,
    "php3" : "PHP" ,
    "p" : "Pascal" ,
    "pas" : "Pascal" ,
    "pl" : "Perl" ,
    # pl for perl conflicts with pl for Prolog...
    "py" : "Python" ,
    "r" : "R" ,
    "rb" : "Ruby" ,
    "sas" : "SAS" ,
    "sql" : "SQL" ,
    "tex" : "TeX" ,
    "vbs" : "VBScript" ,
    "vhd" : "VHDL" ,
    "vrml" : "VRML" ,
    "v" : "Verilog" ,
    "xml" : "XML" ,
    "xslt" : "XSLT" ,
    "bash" : "bash" ,
    "csh" : "csh" ,
    "ksh" : "ksh" ,
    "sh" : "sh" ,
    "tcl" : "tcl"
}

latexspecials = "\\{}_^#&$%~"
specials_re = re.compile(
    '(%s)' % '|'.join(re.escape(c) for c in latexspecials)
)


def makeTop(output=sys.stdout, show_whitespace="false"):
    # print out the file header
    header = '''
\\documentclass{article}
\\usepackage[hmargin=1in,vmargin=1in]{geometry}
\\usepackage{listings}
\\usepackage{color}

% For better handling of unicode (Latin characters, anyway)
\\IfFileExists{lmodern.sty}{\\usepackage{lmodern}}{}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{inputenc}

\\lstset{
    numbers=left,                   % where to put the line-numbers
    numberstyle=\\small \\ttfamily \\color[rgb]{0.4,0.4,0.4},
                % style used for the linenumbers
    showspaces=__WHITESPACE__,               % show spaces adding special underscores
    showstringspaces=false,         % underline spaces within strings
    showtabs=__WHITESPACE__,                 % show tabs within strings adding particular underscores
    frame=lines,                    % add a frame around the code
    tabsize=4,                        % default tabsize: 4 spaces
    breaklines=true,                % automatic line breaking
    breakatwhitespace=false,        % automatic breaks should only happen at whitespace
    basicstyle=\\ttfamily,
    %identifierstyle=\\color[rgb]{0.3,0.133,0.133},   % colors in variables and function names, if desired.
    keywordstyle=\\color[rgb]{0.133,0.133,0.6},
    commentstyle=\\color[rgb]{0.133,0.545,0.133},
    stringstyle=\\color[rgb]{0.627,0.126,0.941},
}

\\begin{document}
'''
    print(header.replace('__WHITESPACE__', show_whitespace), file=output)


def makeBottom(output=sys.stdout):
    print("\\end{document}", file=output)


def addListing(filename, custom_heading=None, output=sys.stdout):
    heading = filename
    if custom_heading is not None:
        heading = custom_heading

    heading_escaped = re.sub(specials_re, r'\\\1', heading)
    print("\\section*{%s}" % heading_escaped, file=output)

    ext = filename.split('.')[-1]
    lang = exts.get(ext, '')
    # uses '' if extension not found in our dictionary
    print("\\lstinputlisting[language=%s]{\"%s\"}" % (lang, filename),
          file=output)
    print("", file=output)


def main():
    if len(sys.argv) != 2:
        sys.exit('''Usage: %s [DIRECTORY]
                 Outputs .tex files and generate PDFs in CWD
                 Languages (for syntax highlighting) determined from file
                 extensions.''' % (sys.argv[0],))

    # Check existence of folder
    code_folder = Path(sys.argv[1])
    if not code_folder.is_dir():
        sys.exit("code_folder not found: %s" % code_folder)

    # Gather the files
    files = listdir(code_folder)
    # Change directory to code folder
    chdir(code_folder)

    # Make the file
    output_file = open('output_file_name.tex', "w")
    makeTop(show_whitespace="false", output=output_file)
    for infile in files:
        addListing(infile, output=output_file)
    makeBottom(output=output_file)
    output_file.close()

    # Make pdf
    call(["pdflatex", "-interaction=batchmode", 'output_file_name.tex'])

    # Change directory back
    chdir('../')


if __name__ == "__main__":
    main()
