#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them

def listoffiles(dirs):

  abs_files = []

  for dir in dirs:

    files = os.listdir(dir)
    files_string = ' '.join(files)
    #print files_string
    filt_files = re.findall(r'\s(\S+__\w+__\S+)', files_string)

    for filt_file in filt_files:
      abs_files.append(os.path.join(os.path.abspath(dir), filt_file))

  return abs_files

def copy_dir(files_to_copy, dir_to_copy):

  if files_to_copy:
    
    err = ''
    
    if not os.path.exists(dir_to_copy):
      if dir_to_copy[0] not in ['/', '~', '.']:
        full_dir = os.path.join(os.getcwd(), dir_to_copy)
      else:
        full_dir = dir_to_copy
      print 'Making directory: '+full_dir
      
      try:
        os.mkdir(full_dir)
      except OSError as err:
        print err
      
    else:
      full_dir = os.path.abspath(dir_to_copy)

    #print files_to_copy, full_dir

    if not err:
      for file in files_to_copy:
        print 'Copying '+file+' to '+full_dir
        shutil.copy(file, full_dir)
    else:
      print 'There was an error in creating the dir, nothing done'
      
  else:
  
    print 'No files found, dir not created'
    
  return

def zip_dir(files_to_zip, dir_to_zip):

  if files_to_zip:
    files_to_zip_string = ' '.join(files_to_zip)
    #print 'Zipping '+files_to_zip_string+' to '+dir_to_zip
    command = 'zip -j '+dir_to_zip+' '+files_to_zip_string
    print 'Command: '+command
    (status, output) = commands.getstatusoutput(command)
    if status:
      print 'Zip failed, exiting'
      print sys.stderr.write(output)
      sys.exit(1)
  else:
    print 'No files found, zip not created'
    
  return
  

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  
  match_files = listoffiles(args)
  
  if todir:
    copy_dir(match_files, todir)
  elif tozip:
    zip_dir(match_files, tozip)
  else:
    print '\n'.join(match_files)
  
if __name__ == "__main__":
  main()
