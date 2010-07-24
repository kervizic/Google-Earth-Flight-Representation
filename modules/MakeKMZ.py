#!/usr/bin/python
#coding: utf-8

__author__ = "KERVIZIC Emmanuel (kervizic@hotmail.com"
__version__ = "0.0.1"
__license__ = ""
__copyright__ =""

from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os, sys

def makeFile(allObjects) :
    basedir = allObjects['path']['absKmlPath']
    archivename = allObjects['path']['absKmzPath']
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)
