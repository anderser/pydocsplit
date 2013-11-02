#!/usr/bin/env python
# encoding: utf-8

import os
import re
import shutil
import subprocess
import tempfile
from pydocsplit.exceptions import ExtractionError
from pydocsplit.info_extractor import InfoExtractor
from pydocsplit.command_runner import run, RunError

MEMORY_ARGS =  "-limit memory 256MiB -limit map 512MiB"
OCR_FLAGS   = '-density 400x400 -colorspace GRAY'

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
        force_ocr = kwargs.get('force_ocr', None)
        forbid_ocr = kwargs.get('forbid_ocr', None)
        self.language = kwargs.get('language', 'eng')
        
        if not os.path.exists(self.output):
            os.makedirs(self.output)    
        
        if pages == "all":
            pages = None
        
        #TODO: change to allow OCR if no text present
        for pdf in pdfs:
            self.filename, ext = os.path.splitext(os.path.basename(pdf))
            if force_ocr or (not forbid_ocr and not self.contains_text(pdf)):
                self.extract_from_ocr(pdf, pages)
            else:
                self.extract_from_pdf(pdf, pages)
            
    def extract_from_pdf(self, pdf, pages):            
            
            if not pages is None:
                for page in pages:
                    self.extract_page(pdf, page)
            else:
                self.extract_full(pdf)

    def extract_from_ocr(self, pdf, pages):            
            
            tempdir = tempfile.mkdtemp()
            basename, ext = os.path.splitext(os.path.basename(pdf))
            base_path = os.path.join(self.output, self.filename)

            if not pages is None:
                for page in pages:
                    tiff = "%s/%s_%i.tif" % (tempdir, self.filename, page)
                    outfile = "%s_%i" % (base_path, page)
                    run('MAGICK_TMPDIR=%s OMP_NUM_THREADS=2 gm convert -despeckle +adjoin %s %s "%s"[%i] "%s" 2>&1' % (tempdir, MEMORY_ARGS, OCR_FLAGS, pdf, (page-1), tiff))
                    run('tesseract %s %s -l %s 2>&1' % (tiff, outfile, self.language))
            else:
                tiff = "%s/%s.tif" % (tempdir, self.filename)
                run('MAGICK_TMPDIR=%s OMP_NUM_THREADS=2 gm convert -despeckle %s %s "%s" "%s" 2>&1' % (tempdir, MEMORY_ARGS, OCR_FLAGS, pdf, tiff))
                run('tesseract "%s" "%s" -l %s 2>&1' % (tiff, base_path, self.language))
            
            if os.path.exists(tempdir):
                shutil.rmtree(tempdir)

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