#!/usr/bin/python

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
	"tcl" : "tcl",
	"cs" : "sharpc",
	"ts" : "typescript"
}

allowedExtensions = ["cs", "html", "ts", "scss"]

latexspecials = "\\{}_^#&$%~"
specials_re = re.compile(
	'(%s)' % '|'.join(re.escape(c) for c in latexspecials)
)


def makeTop(output=sys.stdout):
	# print out the file header
	print('''
\\documentclass{article}
\\usepackage[hmargin=1in,vmargin=1in]{geometry}
\\usepackage{listings}

\\lstset{
	numbers=left,				   % where to put the line-numbers
	showspaces=false,			   % show spaces adding special underscores
	showstringspaces=false,		 % underline spaces within strings
	showtabs=false,				 % show tabs within strings adding particular underscores
	frame=lines,					% add a frame around the code
	tabsize=4,						% default tabsize: 4 spaces
	breaklines=true,				% automatic line breaking
	breakatwhitespace=false,		% automatic breaks should only happen at whitespace
	basicstyle=\\ttfamily
}

\\begin{document}
''')  # noqa -- flake8 doesn't think this is valid; it is.


def makeBottom(output=sys.stdout):
	print("\\end{document}")


def addListing(filename, custom_heading=None, output=sys.stdout):
	heading = filename
	if custom_heading is not None:
		heading = custom_heading

	heading_escaped = re.sub(specials_re, r'\\\1', heading)
	print("\\section*{%s}" % heading_escaped)

	ext = filename.split('.')[-1]
	lang = exts.get(ext, '')
	# uses '' if extension not found in our dictionary
	print("\\lstinputlisting{\"code/%s\"}" % (filename))
	print("")


def main():
	if len(sys.argv) < 2:
		sys.exit('''Usage: %s FILE [FILE2] [FILE3] [...]
 Outputs .tex file to STDOUT (redirect with \"%s FILE.py > FILE.tex\")
 Languages (for syntax highlighting) determined from file extensions.''' % (sys.argv[0], sys.argv[0]))

	filepath = sys.argv[1]
	files = next(os.walk(filepath))[2]

	# Check existence of all files first
	for infile in files:
		if not os.path.isfile(str(filepath + infile)):
			sys.exit("File not found: %s" % infile)
			
	# Make the file (output to STDOUT)
	makeTop()
	for infile in files:
		ext = os.path.splitext(infile)[1].strip(".")
		if ext in allowedExtensions:
			addListing(infile)
	makeBottom()


if __name__ == "__main__":
	main()
