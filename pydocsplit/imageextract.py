#!/usr/bin/env python

import re
import subprocess
import os
import tempfile
import shutil
from exceptions import ExtractionError
from info_extractor import InfoExtractor

DEFAULT_DENSITY = '150'
DEFAULT_FORMATS = ["png",]
DEFAULT_SIZES = ["700x",]
MEMORY_ARGS =  "-limit memory 256MiB -limit map 512MiB"



class ImageExtractor:

    def __init__(self):
        self.options = {
            'output' : '.',
            'sizes' : DEFAULT_SIZES,
            'formats' : DEFAULT_FORMATS,
            'pages': None,
            'density': DEFAULT_DENSITY,
            'rolling': True,
            }
        self.info_extractor = InfoExtractor()  
    
    def extract(self, pdfs, **kwargs):
        """ Extracts images of each page in a PDF document
        Only supports to extract all pages in document at the moment
        
        Usage:
        
        >>>i = ImageExtractor()
        >>>i.extract("/path/to/my/pdffile.pdf", output="/path/to/my/output/dir/", sizes=['500x', '250x'], formats=['png', 'jpg']) 
        """
        
        self.options.update(kwargs)
        
        for pdf in pdfs:
            
            previous = None
            for s in self.options['sizes']:
                for f in self.options['formats']:
                    self.convert(pdf, s.lower(), f.lower(), previous)
                    
                if self.options['rolling']:
                    previous = s.lower()
                
    def normalize_option(self, key):
            
            if type(self.options[key])==type(list()):
                self.options[key] = ",".join([str(v) for v in self.options[key]])

    def resize_arg(self, size):
        
        if size is None:
            return ''
        return "-resize %s" % size
    
    def _copy_files(self,src, dest):
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)
    
    def quality_arg(self, format):
        if format == "jpeg" or "jpg":
            return "-quality 85"
        elif format == "png":
            return "-quality 100"
        else:
            format = ""
        
    def convert(self, pdf, size, format, previous=None):
        
        tempdir = tempfile.gettempdir()
        basename, ext = os.path.splitext(os.path.basename(pdf))
        if size > 1: 
            subfolder = str(size)
        else:
            subfolder = ''
            
        directory = os.path.join(self.options['output'], subfolder)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        #TODO add method to clean pages arg to range/list ref page_list in ruby ver

        pages = range(1,self.info_extractor.extract('length', pdf)+1)
        
        common = "%s -density %s %s %s" % (MEMORY_ARGS, self.options['density'], self.resize_arg(size), self.quality_arg(format))
        
        if previous:
            
            self._copy_files(os.path.join(self.options['output'], previous), directory)
            cmd = 'MAGICK_TMPDIR=%s OMP_NUM_THREADS=2 gm mogrify %s -unsharp 0x0.5+0.75 "%s/*.%s" 2>&1'% (tempdir, common, directory, format)
            self.run_gm(cmd.strip())
        else:
            
            for page in pages:
                out_file = os.path.join(directory, "%s_%i.%s" % (basename, page, format))
                cmd = "MAGICK_TMPDIR=%s OMP_NUM_THREADS=2 gm convert +adjoin %s %s[%i] %s 2>&1" % (tempdir, common, pdf, (page-1), out_file)
                self.run_gm(cmd.strip())
        return True
    
    def run_gm(self, args):
        
        procs = subprocess.Popen('%s' % args, shell=True, stdout=subprocess.PIPE)

        if procs.wait() != 0:
            raise ExtractionError(args, procs.communicate()[0])

