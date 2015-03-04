#!usr/bin/python

# formatDirectoryForTokenizer.py
# David Folarin @ Cornell University 2015

# Formats the files in a directory for VW tokenizer
# Because File names become doc_id
# File names cannont have whitespace, | ' or :

import os
import argparse

def rename_files(direct):
	""" renames all files in source directory by removing | : and ' """
	fnames = os.listdir(direct)
	qualified_filenames = (os.path.join(direct, filename) for filename in fnames)
	files = [name for name in qualified_filenames if os.path.isfile(name)]
	for name in files:
		os.rename(name,name.replace(' ','_').replace('|','').replace("'",'').replace(':',''))


def main():
	parser = argparse.ArgumentParser(description='Rename all files in a directory to fit Tokenizer specs')
	parser.add_argument('directory',type=str,help='path to directory')

	args = parser.parse_args()

	direct = args.directory

	rename_files(direct)

if __name__ == '__main__':
	main()