#!/usr/bin/env python
# encoding: utf-8
"""
text_extractor.py

Created by Anders G Eriksen on 2011-12-10.
Copyright (c) 2011 AGE. All rights reserved.
"""

class TextExtractor:
    def __init__(self):
        
        self.i = InfoExtractor()
    
    def extract(self, pdfs, **kwargs):
        """
        Extracts text from a PDF
        The text is saved as a text file with same base name as your document in the 
        output dir specified. 

        Usage:
        >>>d = TextExtractor()
        >>>d.extract('/path/to/my/pdffile.pdf', output='/path/to/outputdir/')

        """
        
        raise NotImplementedError