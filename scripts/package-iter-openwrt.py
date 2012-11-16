#!/usr/bin/python
# Copyright (C) 2012 Luis R. Rodriguez <mcgrof@do-not-panic.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import sys, getopt
import os, os.path
import mmap
from debian import deb822

openwrt_git_dir = os.environ['HOME'] + '/devel/openwrt/'
openwrt_gitweb_url = 'http://nbd.name/gitweb.cgi?p=openwrt.git;a=blob;f='
openwrt_tree_url =   'http://nbd.name/gitweb.cgi?p=openwrt.git;a=tree;f='

def usage():
	print ''
	print 'This program accepts an OpenWrt Packages file, a list of'
	print 'package names (consider your opkg list_installed output) '
	print 'and based on the two spits out wiki page content for OpenWrt'
	print 'to standard output. It also will build documentation for each'
	print 'package in package list into the specified output directory'
	print 'The stdout is targeted for usage on a page like:'
	print ''
	print 'http://wiki.openwrt.org/doc/devel/packages/list'
	print ''
	print 'Consider using xclip as follows to copy+paste:'
	print ''
	print 'prog | xclip -sel clip'
	print ''
	print 'Individual package documentation is targeted for pages'
	print 'for each package. For example:'
	print ''
	print 'http://wiki.openwrt.org/doc/devel/packages/busybox'
	print ''

	print 'Usage: %(cmd)s -p packages -l opkg-list -o output_dir' % \
		{ "cmd": sys.argv[0] }
	sys.exit(2)

def check_file(file_input):
	if not os.path.isfile(file_input):
		print 'File not found: %(file)s' % { "file": file_input }
		usage()

def pkg_in_opkg_list(pkg, opkg_list):
	f = file(opkg_list)
	for pkg_line in f:
            if pkg in pkg_line:
                return True
		f.close()
        return False
	f.close()

def main():
	packages_file  = ''
	pkg_list_file  = ''
	package_output = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hp:l:o:")
	except getopt.GetoptError, err:
		print str(err)
		usage()

	for o, a in opts:
		if o in ("-p"):
			check_file(a)
			packages_file = a
		elif o in ("-l"):
			check_file(a)
			pkg_list_file = a
		elif o in ("-o"):
			if os.path.exists(a):
				print 'Directory provided (%(dir)s) exists, supply empty directory' % { "dir": a }
				usage()
			os.makedirs(a)
			package_output = a
		elif o in ("-h", "--help"):
			usage()

	if len(packages_file) == 0 or \
	   len(pkg_list_file) == 0 or \
	   len(package_output) == 0:
		usage()

	pkg_list_f = open(pkg_list_file, "r")

	print 'This page documents all packages installed by default on the AA-12.09-beta2 release.'
	print 'This page and each package documentation was automatically generated with a set of'
	print 'scripts as part of the [[https://github.com/mcgrof/openwrt-doc-scripts|openwrt-doc-scripts]] project.'
	print ''

	# What we ideally also want:
	# * License - this needs some work with Debian / OpenWrt folks
	# * Number of bugs - this needs some coordination with OpenWrt
	# * Project URL - probably some scraping
	print '^Package^Version^Delta^Section^Maintainer^'

	for pkg in deb822.Packages.iter_paragraphs(file(packages_file)):

		if not pkg_in_opkg_list(pkg['package'], pkg_list_file):
			continue

		package_patches = openwrt_git_dir + 'package/' + pkg['package'] + '/patches/'

		if os.path.isdir(package_patches):
			num_patches = len([name for name in os.listdir(package_patches) if os.path.isfile(package_patches + name)])
			patches_url = openwrt_tree_url + \
				      'package/' + pkg['package'] + \
				      '/patches'
			patches_url = '[[' + patches_url + '|' + str(num_patches) + ']]'
		else:
			num_patches = "unknown"
			patches_url = "unknown"

		print '|[[doc/devel/packages:%(package)s|%(package)s]]|%(version)s|%(delta)s|%(section)s|%(maintainer)s|' % \
			 { \
			   "package": pkg['package'], \
			   "version": pkg['version'], \
			   "delta": patches_url, \
			   "section": pkg['section'], \
			   "maintainer": pkg['maintainer'] \
			}

		f = open(package_output + '/' + pkg['package'], 'w')
		f.write('====== %(package)s OpenWrt package ======\n%(version_details)s\n%(description)s\n' % \
			{ \
			   "package": pkg['package'], \
			   "version_details": 'Source: ' + pkg['package'] + ' Version: ' + pkg['version'], \
			   "description": pkg['description'].strip() \
			} )
		f.write('====== %(package)s %(version)s ======\n%(description)s\n' % \
			{ \
			   "package": pkg['package'], \
			   "version": pkg['version'], \
			   "description": pkg['description'].strip() \
			} )
		f.write('====== Maintainer ======\n%(maintainer)s\n' % \
			{ "maintainer": "  * " + pkg['maintainer'] } )
		f.write('====== Delta with upstream on %(package)s on OpenWrt ======\n' % \
			{ "package": pkg['package'].title()})
		f.write('There are %(delta)s patches in openwrt packages/%(package)s/patches/\n' % \
			{ \
			   "delta": num_patches, \
			   "package": pkg['package'], \
			} )
		
		if num_patches > 0 and num_patches != 'unknown' :
			for name in os.listdir(package_patches):
				if os.path.isfile(package_patches + name):
					patch_url = openwrt_gitweb_url + \
						    'package/' + pkg['package'] + \
						    '/patches/' + name
					f.write('  * [[%(patch_url)s|%(patch_name)s]]\n' % \
						{
						  "patch_url": patch_url, \
						  "patch_name": name, \
						} )
		f.close()

if __name__ == "__main__":
	main()
