#!/usr/bin/env python
# encoding: utf-8
"""
command_runner.py

Created by Anders G Eriksen on 2011-12-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.

Simple wrapper function to run shell commands

"""

import subprocess

class RunError(Exception):
    def __init__(self, cmd, msg):
        self.cmd = cmd
        self.msg = msg


def run(command, *args, **kwargs):
    
    ag = ' '.join(args)
    kwa = ' '.join(["--%s %s" % (key, kwargs[key]) for key in kwargs])
    cmd = "%s %s %s" % (command, kwa, ag)

    try: 
        proc = subprocess.Popen('%s' % cmd, shell=True, stdout=subprocess.PIPE)
        
    except OsError, e:
        raise RunError(cms, e)
    
    else: 
        if proc.wait() != 0:
            raise RunError(cmd, proc.communicate()[0])
        else:
            return proc.communicate()[0]