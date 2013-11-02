#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
import unittest
import tempfile
from pydocsplit.docsplit import Docsplit


class PyDocsplitTests(unittest.TestCase):
    def setUp(self):
        self.pdf = "./fixtures/tv2.pdf"
        self.text_pdf = "./fixtures/obama_arts.pdf"
        self.doc = "./fixtures/obama_veterans.doc"
        self.docsplit = Docsplit()
        self.tempdir = os.path.join(tempfile.gettempdir(), 'docsplittests')
        
    def test_infoextract(self):
        
        self.assertEqual(self.docsplit.extract_info('length', self.pdf), 8)
    
    def test_pageextract(self):
            
        self.assertEqual(self.docsplit.extract_pages([self.pdf], output=self.tempdir), True)
    
    def test_pdfextract(self):
        
        self.docsplit.extract_pdf(self.doc, output=self.tempdir)
        self.assertEqual(os.path.exists(os.path.join(self.tempdir, "obama_veterans.pdf")), True)
        
    def test_imageextract(self):
        
        imgpath = os.path.join(self.tempdir, "tv2","images_all")
        self.docsplit.extract_images(self.pdf, output=imgpath, sizes=['1000x', '700x', '180x'], formats=["jpg"])
        for i in range(1,6):
            self.assertEqual(os.path.exists(os.path.join(imgpath, "700x", "tv2_%i.jpg" % i)), True)
            self.assertEqual(os.path.exists(os.path.join(imgpath, "1000x", "tv2_%i.jpg" % i)), True)
            self.assertEqual(os.path.exists(os.path.join(imgpath, "180x", "tv2_%i.jpg" % i)), True)
    
    def test_text_extraction_no_ocr_all_pages(self):
        
            self.docsplit.extract_text(self.text_pdf, output=self.tempdir, pages=[1])
            self.assertEqual(os.path.exists(os.path.join(self.tempdir, "obama_arts_1.txt")), True)

    def test_text_extraction_ocr_all_pages(self):
        
            self.docsplit.extract_text(self.pdf, output=self.tempdir, language='nor')
            self.assertEqual(os.path.exists(os.path.join(self.tempdir, "tv2.txt")), True)
                                                                                   
    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
    
if __name__ == '__main__':
    unittest.main()