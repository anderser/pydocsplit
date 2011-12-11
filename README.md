#pyDocsplit

A simple Python wrapper of the great Docsplit utility from DocumentCloud
<http://github.com/documentcloud/docsplit>

##Requirements:

- All the requirements for the original Ruby Docsplit (except the gem): <http://documentcloud.github.com/docsplit/>

##Installation:

Follow the instructions to install all the requirements for Docsplit here: 
<http://documentcloud.github.com/docsplit/>
(You don't have to install the Ruby gem if using the dev branch of pyDocsplit)

Clone this repo and add to PYTHONPATH

##Usage:

	from pydocsplit import Docsplit

	d = Docsplit()
	d.extract_pdf('/path/to/my/document.doc', output='/path/to/outputdir/')
	d.extract_pages('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', pages='1-2')
	d.extract_images('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', sizes=['500x', '250x'], formats=['png', 'jpg'], pages=[1,2,5,7])
	documenttitle = d.extract_info('title', /path/to/my/pdffile.pdf')

