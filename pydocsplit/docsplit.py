#!/usr/bin/env python

#Python implementation of the DocumentCloud's Docsplit utility
#http://github.com/anderser/pydocsplit
#
import os
import subprocess
import tempfile
import shlex
from pydocsplit.exceptions import ExtractionError
from pydocsplit.imageextract import ImageExtractor
from pydocsplit.page_extractor import PageExtractor
from pydocsplit.info_extractor import InfoExtractor
from pydocsplit.text_extractor import TextExtractor


DOCSPLIT_JAVA_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.pardir)

DOCSPLIT_CLASSPATH = os.path.join (DOCSPLIT_JAVA_ROOT,
                                    "build") + os.pathsep + os.path.join(DOCSPLIT_JAVA_ROOT, "vendor", "'*'")

DOCSPLIT_LOGGING = "-Djava.util.logging.config.file=%s/vendor/logging.properties" % DOCSPLIT_JAVA_ROOT

if os.path.exists("/usr/lib/openoffice"):
    office = '/usr/lib/openoffice'
elif os.path.exists("/usr/lib/libreoffice"):
    office = '/usr/lib/libreoffice'
else:
    office = None

if office:
    DOCSPLIT_OFFICEHOME = '-Doffice.home=%s" % office'
else: 
    DOCSPLIT_OFFICEHOME = ''

DOCSPLIT_HEADLESS = '-Djava.awt.headless=true'

class Docsplit:
    
    def __init__(self):
        pass
    
    def extract_pages(self, pdfs, **kwargs):
        """
        Extracts each page of a pdf file and saves as separate pdf files
        
        Usage:
        >>>d = Docsplit()
        >>>d.extract_pages('[/path/to/my/document1.doc','/path/to/my/document2.doc'], output='/path/to/outputdir/', pages='1-2')
        """
        pdf = self.ensure_pdfs(pdfs)
        p = PageExtractor()
        return p.extract(pdfs, **kwargs)
    
    def extract_text(self, docs, **kwargs):
        """
        Extracts text from a PDF
        The text is saved as a text file with same base name as your document in the 
        output dir specified. 
        
        Usage:
        >>>d = Docsplit()
        >>>d.extract_text('/path/to/my/pdffile.pdf', output='/path/to/outputdir/')
        >>>d.extract_text('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', returntext=True)
        """
        
        pdfs = self.ensure_pdfs(docs)
        t = TextExtractor()
        return t.extract(pdfs, **kwargs)
    
        
    def extract_pdf(self, docs, **kwargs):
        """
        Extracts pdf file from a document (i.e. .doc, .pdf, .rtf, .xls) using OpenOffice
        
        Usage:
        >>>d = Docsplit()
        >>>d.extract_pdf('/path/to/my/document.doc', output='/path/to/outputdir/')
        """
        output = kwargs.get('output', '.')
        
        if not os.path.exists(output):
            os.makedirs(output)        
        
        docs = [docs] if isinstance(docs, str) else docs
        
        for doc in docs:
            filename, ext = os.path.splitext(os.path.basename(doc))

            options = '-jar %s/vendor/jodconverter/jodconverter-core-3.0-beta-4.jar -r %s/vendor/conf/document-formats.js' % (DOCSPLIT_JAVA_ROOT, DOCSPLIT_JAVA_ROOT)
            
            args = ('%s %s %s/%s.pdf') % (options, doc, output, filename)
            
            return self._run(args, doc) 
    
    def ensure_pdfs(self, docs):
            
        """ 
        Makes sure the document exists as PDF, if not converts to PDF
        using office and saves in temp folder.
        """
        
        #make sure we get a list of docs even though only a single doc is provided
        docs = [docs] if isinstance(docs, str) else docs
        
        pdfs =[]
        for doc in docs:
            basename, ext = os.path.splitext(os.path.basename(doc))

            if ext.lower() == '.pdf':
                pdfs.append(doc)
            else:
                tempdir = os.path.join(tempfile.gettempdir(), 'docsplit')
                self.extract_pdf([doc], output=tempdir)
                pdfs.append("%s.pdf" % os.path.join(tempdir, basename))
        return pdfs
    
    def extract_images(self, pdfs, **kwargs):
        """
        Extracts each page of a pdf file and saves as images of given size and format
        
        Parameters:
        sizes: list of sizes i.e. ['500x', '250x']
        formats: list of formats i.e. ['jpg', 'png']
        pages (optional): list of pages either as list [1,2,5,6] or as a string in this format ['1-10']
        
        Usage:
        >>>d = Docsplit()
        >>>d.extract_images('/path/to/my/pdffile.pdf', output='/path/to/outputdir/', sizes=['500x', '250x'], formats=['png', 'jpg'], pages=[1,2,5,7])
        """
        pdfs = self.ensure_pdfs(pdfs)
        i = ImageExtractor()
        return i.extract(pdfs, **kwargs)
    
    def extract_info(self, metakey, pdfs, **kwargs):
        """
        Extracts meta data from pdf file. Returns value of meta field as string
        Valid meta data fields:
        author, date, creator, keywords, producer, subject, title, length
        
        Usage:
        >>>d = Docsplit()
        >>>d.extract_meta('/path/to/my/pdffile.pdf', 'title')
        """
        i = InfoExtractor()
        pdfs = self.ensure_pdfs(pdfs)
        return i.extract(metakey,pdfs)

        
    def _run(self, command, pdf, **kwargs):
        
        """
        Private method to run the office document converter via java
        """
        
        #TODO: Use args in subprocess and not shell=True
        
        cmd = "java %s %s %s -cp %s %s" % (DOCSPLIT_HEADLESS, DOCSPLIT_LOGGING, DOCSPLIT_OFFICEHOME, DOCSPLIT_CLASSPATH, command)
        
        try: 
            proc = subprocess.Popen(shlex.split(cmd),shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        except Exception, e:
            print e
        
        else: 
            if proc.wait() != 0:
                raise ExtractionError(cmd, proc.communicate()[0])
            else:
                return proc.communicate()[0]