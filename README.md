#pyDocsplit

A simple Python implementation of the great Docsplit utility from DocumentCloud
(http://github.com/documentcloud/docsplit)

##Requirements:

- Docsplit utility/gem and all its requirements: (http://documentcloud.github.com/docsplit/)

##Installation:

Follow the instructions to install the original Docsplit here: (http://documentcloud.github.com/docsplit/)

Put the pydocsplit folder on your python path and change the DOCSPLIT_JAVA_ROOT setting
in docsplit.py to point to your installation of the Ruby gem

Remember to run OpenOffice in headless mode if you want to convert documents to pdf. 
See the Docsplit docs for howto: http://documentcloud.github.com/docsplit/

##Usage:

	from pydocsplit import Docsplit

	d = Docsplit()
	d.extract_pdf('/path/to/my/document.doc', output='/path/to/outputdir/')
	d.extract_pages('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', pages='1-2')
	d.extract_text('/path/to/my/pdffile.pdf', output='/path/to/outputdir/')
	d.extract_images('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', sizes=['500x', '250x'], formats=['png', 'jpg'], pages=[1,2,5,7])
	documenttitle = d.extract_meta('/path/to/my/pdffile.pdf', 'title')

##TODO:

- Support multiple pdfs as input
- Enhance parsing of pages options/ranges
- Ensure pdfs before extracting text, images etc