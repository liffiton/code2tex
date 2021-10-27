#!/usr/bin/env python3

import sys
import re
import os.path

# TODO: read extensions, header from files found in sys.path?

# A subset of the languages supported by the Listings latex package
# File extensions mapped to language names
exts = {
    "ada" : "Ada" ,
    "adb" : "Ada" ,
    "ads" : "Ada" ,
    "awk" : "Awk" ,
    "c" : "C" ,
    "h" : "C++" ,
    "hh" : "C++" ,
    "hpp" : "C++" ,
    "cxx" : "C++" ,
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
    "js" : "JavaScript" ,
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

%
% JavaScript version 1.1 by Gary Hammock
%   https://github.com/ghammock/LaTeX_Listings_JavaScript_ES6
%
% Reference:
%   B. Eich and C. Rand Mckinney, "JavaScript Language Specification
%     (Preliminary Draft)", JavaScript 1.1.  1996-11-18.  [Online]
%     http://hepunx.rl.ac.uk/~adye/jsspec11/titlepg2.htm
%

\\lstdefinelanguage{JavaScript}{
  morekeywords=[1]{break, continue, delete, else, for, function, if, in,
    new, return, this, typeof, var, void, while, with},
  % Literals, primitive types, and reference types.
  morekeywords=[2]{false, null, true, boolean, number, undefined,
    Array, Boolean, Date, Math, Number, String, Object},
  % Built-ins.
  morekeywords=[3]{eval, parseInt, parseFloat, escape, unescape},
  sensitive,
  morecomment=[s]{/*}{*/},
  morecomment=[l]//,
  morecomment=[s]{/**}{*/}, % JavaDoc style comments
  morestring=[b]',
  morestring=[b]"
}[keywords, comments, strings]

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
    print("\\lstinputlisting[language=%s]{\"%s\"}" % (lang, filename), file=output)
    print("", file=output)


def main():
    if len(sys.argv) < 2:
        sys.exit('''Usage: %s [-s] FILE [FILE2] [FILE3] [...]
 Outputs .tex file to STDOUT (redirect with \"%s FILE.py > FILE.tex\")
 Languages (for syntax highlighting) determined from file extensions.
 If -s is given as the first argument, the resulting document will display
 whitespace in the code as printable characters.
 ''' % (sys.argv[0], sys.argv[0]))

    if sys.argv[1] == '-s':
        show_whitespace = "true"
        files = sys.argv[2:]  # get all other command line arguments
    else:
        show_whitespace = "false"
        files = sys.argv[1:]  # get all command line arguments

    # Check existence of all files first
    for infile in files:
        if not os.path.isfile(infile):
            sys.exit("File not found: %s" % infile)

    # Make the file (output to STDOUT)
    makeTop(show_whitespace=show_whitespace)
    for infile in files:
        addListing(infile)
    makeBottom()


if __name__ == "__main__":
    main()
