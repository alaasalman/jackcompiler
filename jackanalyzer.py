#!/usr/bin/env python
import sys
import os.path
from compilationengine import CompilationEngine


def main(argv):
    jackfilename = argv[1]
    
    #getting jack file name    
    (jfilename, jextension) = os.path.splitext(jackfilename)
    jackxml = jfilename + ".xml" #just to be consistent with the book
      
    compiler = CompilationEngine(jackfilename, jackxml)
    
    
if __name__ == "__main__":
    main(sys.argv)
