#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def url_dict_sort(url):
  url_split = url.rsplit('-',2)
  if '/' in url_split[-2]:
    return url_split[-1]
  else:
    return (url_split[-1], url_split[-2])
  

def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  host_tmp = filename.split('_')
  host = host_tmp[1]
  f = open(filename, 'r')
  log = f.read()
  puzzle_urls = re.findall(r'GET\s(\S+puzzle\S+)\s', log)
  # \s = any whitespace
  # \S = any non-whitespace
  # \w = alphanumeric and _
  # . = any character
  url_dict = {}
  for url in puzzle_urls:
    if not url_dict.get('http://'+host+url):
      url_dict['http://'+host+url] = 1
  sorted_url_dict = sorted(url_dict.keys(), key=url_dict_sort)
  return sorted_url_dict
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """

  mkdir_err = ''

  if not os.path.exists(dest_dir):

    if dest_dir[0] not in ['/', '~', '.']:
      full_dir = os.path.join(os.getcwd(), dest_dir, '')
    else:
      full_dir = os.path.join(dest_dir, '')
    print 'Making directory: '+full_dir

    try:
      os.mkdir(full_dir)
    except OSError as mkdir_err:
      print mkdir_err
      sys.exit(1)
      
  else:

    full_dir = os.path.join(os.path.abspath(dest_dir), '')

#  print full_dir
  
  f = open(full_dir+'index.html', 'w')
  f.write(r'<html><body>''\n')

  for i in range(0,len(img_urls)):
    img_filename = 'img'+str(i)
    print 'Downloading '+img_urls[i]+' to '+full_dir+img_filename
    urllib.urlretrieve(img_urls[i], full_dir+img_filename)
    f.write(r'<img src="'+img_filename+r'">')

  f.write('\n'r'</body></html>')
  f.close()

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
