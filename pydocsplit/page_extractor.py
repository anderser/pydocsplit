#!/usr/bin/env python
# encoding: utf-8

import sys
import os
from utils.command_runner import run, RunError

class PageExtractionError(Exception):
    def __init__(self, cmd, msg):
        self.cmd = cmd
        self.msg = msg

class PageExtractor:
    
    """ 
    Extracts PDFs into single pages as pdfname_pagenumber.pdf
    
    """
    
    def __init__(self):
        pass
        
    def extract(self, pdfs, *args, **kwargs):
        
        output = kwargs.get('output', '.')
        
        if not os.path.exists(output):
            os.makedirs(output)        

        for pdf in pdfs:
            filename, ext = os.path.splitext(os.path.basename(pdf))
            page_path = os.path.join(output, '%s_%%d.pdf' % filename)
            cmd = 'pdftk %s burst output %s 2>&1' % (pdf, page_path)

            try:
                result = run(cmd)
            except RunError, err:
                raise PageExtractionError, err
            else:
                if (os.path.exists('doc_data.txt')):
                    os.unlink('doc_data.txt')
                    
                return True