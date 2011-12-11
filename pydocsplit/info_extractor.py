#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import re
from utils.command_runner import run, RunError


class InfoExtractor:
    
    """ 
    Extracts meta data from pdf file. Returns value of meta field as string/integer
    
    Valid meta data fields:
    author, date, creator, keywords, producer, subject, title, length
    
    Usage:
    >>>i = InfoExtractor()
    >>>i.extract('title','/path/to/my/pdffile.pdf')
    
    """
    
    def __init__(self):
        
        self.matchers = {
            'author': re.compile('^Author:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'date': re.compile('^CreationDate:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'creator': re.compile('^Creator:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'keywords': re.compile('^Keywords:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'producer': re.compile('^Producer:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'subject': re.compile('^Subject:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'title': re.compile('^Title:\s+?([^\n]+)', re.MULTILINE | re.UNICODE),
            'length': re.compile('^Pages:\s+?([^\n]+)', re.MULTILINE| re.UNICODE),
        }
        
        self.keymatch = re.compile('^[\w\s]*?:\s+([^\n]+)')
        
    def extract(self, key, pdfs, *args, **kwargs):
        
        pdf = pdfs[0] if isinstance(pdfs, list) else pdfs
        
        try:
            result = run('pdfinfo', '"%s"' % pdf)
            lines = result.splitlines(True)
        except RunError, err:
            raise Exception, err
        else:
            m = self.matchers[key].search(result)
            if m:
                if key == "length":
                    return int(m.group(1).strip())
                return m.group(1).strip()
            else:
                
                return None