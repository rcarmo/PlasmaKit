#!/usr/bin/python
"""
Build script

Usage:
    python setup.py py2app
"""
from distutils.core import setup
import py2app
from glob import glob

version = "0.0.1" 

plist = dict(
  CFBundleName="Plasma Player",
  NSMainNibFile="MainMenu",
  NSPrincipalClass='PlasmaApplication',
  CFBundleIdentifier="eu.codebits.plasma", # historical
  CFBundleShortVersionString=version,
  CFBundleVersion=version,
  NSHumanReadableCopyright="Copyright 2011 Rui Carmo.",
  NSAppleScriptEnabled=False
)

setup(
  app=["main.py",],
  data_files= glob("resources/*.nib") + glob("resources/*.html") + glob("resources/*.gif") + glob("*.py") + glob("*/*.py") + glob("resources/*.css") + glob("resources/*.png"),
  options=dict(py2app=dict(
    plist=plist,
    iconfile="resources/Icon.icns",
  )),
)

