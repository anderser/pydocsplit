#!/usr/bin/env python
# encoding: utf-8

import os
import re
import subprocess
from pydocsplit.exceptions import ExtractionError
from pydocsplit.info_extractor import InfoExtractor
from pydocsplit.command_runner import run, RunError

class TextExtractor:
    def __init__(self):
        
        self.i = InfoExtractor()
        self.output = None
        self.filename = None
    
    def extract(self, pdfs, **kwargs):
        """
        Extracts text from a PDF
        The text is saved as a text file with same base name as your document in the 
        output dir specified. 

        Usage:
        >>>d = TextExtractor()
        >>>d.extract('/path/to/my/pdffile.pdf', output='/path/to/outputdir/')

        """
        
        self.output = kwargs.get('output', '.')
        pages = kwargs.get('pages', None)
        
        if not os.path.exists(self.output):
            os.makedirs(self.output)    
        
        if pages == "all":
            pages = None
        
        #TODO: change to allow OCR if no text present
        for pdf in pdfs:
            self.filename, ext = os.path.splitext(os.path.basename(pdf))
            self.extract_from_pdf(pdf, pages)
            
    def extract_from_pdf(self, pdf, pages):            
            
            if not pages is None:
                for page in pages:
                    self.extract_page(pdf, page)
            else:
                self.extract_full(pdf)
                
    
    def extract_full(self, pdf):
        
        text_path = os.path.join(self.output, "%s.txt" % self.filename)
        try:
            subprocess.check_call(["pdftotext", "-enc", "UTF-8", pdf, text_path])
        except subprocess.CalledProcessError, e:
            raise ExtractionError(e.cmd, e.returncode)
         
    def extract_page(self, pdf, page):
         
        text_path = os.path.join(self.output, "%s_%i.txt" % (self.filename, page))
        try:
            subprocess.check_call(["pdftotext", "-enc", "UTF-8", "-f", str(page),"-l", str(page) , pdf, text_path])
        except subprocess.CalledProcessError, e:
            raise ExtractionError(e.cmd, e.returncode)
       
    def contains_text(self, pdf):

        """
        Check if the PDF contains text by checing if fonts are included in the file.
        Returns True if pdf contains text, False if it does not contain text 
        """
        
        try:
            result = run('pdffonts', '"%s" 2>&1' % pdf)
            
            
        except RunError, err:
            raise Exception, err
        else:
            m = re.search(r"---------\n\Z", result, re.MULTILINE)
            if m: 
                return False
            else: 
                return True
            return m