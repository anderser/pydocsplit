#!/usr/bin/env python

#Python implementation of DocumentCloud's Docsplit Image Exctractor
#Original Ruby implementation: http://github.com/documentcloud/docsplit/blob/master/lib/docsplit/image_extractor.rb

DENSITY_ARG = "-density 150"
DEFAULT_FORMATS = ["png",]
DEFAULT_SIZES = ["500x",]

import re
import subprocess
import os

class ImageExtractionError(Exception):
    def __init__(self, cmd, msg):
        self.cmd = cmd
        self.msg = msg

class ImageExtractor:

    def __init__(self):
        self.options = {
            'output' : '.',
            'sizes' : DEFAULT_SIZES,
            'formats' : DEFAULT_FORMATS,
            'pages': None,
            }
    
    def extract(self, pdf, **kwargs):
        """ Extracts images of each page in a PDF document
        
        Usage:
        
        >>>i = ImageExtractor()
        >>>i.extract("/path/to/my/pdffile.pdf", output="/path/to/my/output/dir/", sizes=['500x', '250x'], formats=['png', 'jpg']) 
        """
        
        self.options.update(kwargs)
        
        for s in self.options['sizes']:
            for f in self.options['formats']:
                self.convert(pdf, s.lower(), f.lower())
                
    def normalize_option(self, key):
            
            if type(self.options[key])==type(list()):
                self.options[key] = ",".join([str(v) for v in self.options[key]])

    def resize_arg(self, size):
        
        if size is None:
            return ''
        return "-resize %s" % size
    
    def quality_arg(self, format):
        if format == "jpeg" or "jpg":
            return "-quality 85"
        else:
            return "-quality 100"
        
    def convert(self, pdf, size, format):
        
        basename, ext = os.path.splitext(os.path.basename(pdf))
        if size > 1: 
            subfolder = str(size)
        else:
            subfolder = ''
            
        directory = os.path.join(self.options['output'], subfolder)
        
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        out_file = os.path.join(directory, "%s_%%05d.%s" % (basename, format))
        
        args = '%s %s %s "%s%s" "%s" 2>&1' % (DENSITY_ARG, self.resize_arg(size), self.quality_arg(format), pdf, self.pages_arg(), out_file )
        args = args.strip()
        
        return self.run_gm(args)
    
    def pages_arg(self):
        
        self.normalize_option("pages")
        if self.options['pages'] is None:
           return ''
        else:
           p = re.compile(r'\d+')
           return "[%s]" % p.sub(self.page_subtract, self.options['pages'])
           
    def page_subtract(self, match):
        
        value = int( match.group() ) - 1
        return str(value)
    
    def run_gm(self, args):
        
        procs = subprocess.Popen('gm convert %s' % args, shell=True, stdout=subprocess.PIPE)

        if procs.wait() != 0:
            try:
                raise ImageExtractionError(args, procs.communicate()[0])
            except ImageExtractionError, err:
                print err.cmd, err.msg
                return False
        else:
            return True

