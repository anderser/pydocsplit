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
        self.docsplit = Docsplit()
        self.tempdir = os.path.join(tempfile.gettempdir(), 'docsplittests')
    
    def test_infoextract(self):
        
        self.assertEqual(self.docsplit.extract_info('length', self.pdf), 8)
    
    def test_pageextract(self):
            
        self.assertEqual(self.docsplit.extract_pages([self.pdf], output=self.tempdir), True)
    
    def test_imageextract(self):
        
        imgpath = os.path.join(self.tempdir, "tv2","images_all")
        self.docsplit.extract_images(self.pdf, output=imgpath, sizes=['1000x', '700x', '180x'], formats=["jpg"])
        for i in range(1,6):
            self.assertEqual(os.path.exists(os.path.join(imgpath, "700x", "tv2_%i.jpg" % i)), True)
            self.assertEqual(os.path.exists(os.path.join(imgpath, "1000x", "tv2_%i.jpg" % i)), True)
            self.assertEqual(os.path.exists(os.path.join(imgpath, "180x", "tv2_%i.jpg" % i)), True)
                                                                                              
    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
    
if __name__ == '__main__':
    unittest.main()