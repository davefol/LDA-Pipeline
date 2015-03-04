#!usr/bin/python

# topicModelingPipeline.py
# David Folarin @ Cornell University 2015

# Takes path to directory of files and path to output files
# Runs all the scripts in pipeline
# Creates output file of topics 

import argparse
import formatDirectoryForTokenizer
from rosetta import TextFileStreamer, TokenizerBasic, MakeTokenizer
from rosetta.text.text_processors import SFileFilter, VWFormatter
from rosetta.text.vw_helpers import LDAResults
from nltk.corpus import stopwords
import string
import os
from subprocess import call
import warnings

cachedStopWords = stopwords.words("english")

def tokenizer_func(content):
	""" accepts string representing document and returns list of strings representing tokens """
	content = content.replace('\n', '').replace('|','').replace("'",'').replace(':','').lower() # Explicitly remove VW formatters
	with warnings.catch_warnings():
		warnings.simplefilter("ignore")
		content = ' '.join([word for word in content.split() if word not in cachedStopWords]) # Remove stop words
	content = content.translate(string.maketrans("",""), string.punctuation) # Remove punctuation
	return content.split()

def main():
	parser = argparse.ArgumentParser(description='Performs Topic Modeling on a directory of text files')
	parser.add_argument('directory',type=str,help='path to directory')
	parser.add_argument('output_path',type=str,help='path to output files')
	parser.add_argument('topics',type=int,help='number of topics to generate')
	parser.add_argument('passes',type=int,help='number of passes')

	args = parser.parse_args()

	direct = args.directory
	output = args.output_path
	num_topics = args.topics
	num_passes = args.passes

	# Check to see if output directory exists, if not then make it
	if not os.path.exists(output):
		print "%s does not exist, creating new directory..." % output
		os.makedirs(output)


	# 1 Format Directory
	print "Formating source files directory..."
	formatDirectoryForTokenizer.rename_files(direct)

	# 2 Stream directory of files into VW format
	print "Converting and Tokenizing source files"
	print "\tCreating Tokenizer"
	my_tokenizer = MakeTokenizer(tokenizer_func)
	print "\t Creating Streamer"
	stream = TextFileStreamer(text_base_path=direct, tokenizer=my_tokenizer)
	print "\t Streaming Text files to VW format"
	name_vw_file = '%s-doc_tokens.vw' % os.path.basename(direct)
	stream.to_vw(os.path.join(output,name_vw_file), n_jobs=-1)

	# 3 Create Sfile Filter and filter out tokens
	print "Filtering Tokens"
	print "\t creating Sfile Filter"
	sff = SFileFilter(VWFormatter())
	print "\t loading %s..." % name_vw_file
	sff.load_sfile(os.path.join(output,name_vw_file))
	print "\t filtering extremes minimum doc freq = 5, maximum fraction of doc = 0.8"
	sff.filter_extremes(doc_freq_min=5, doc_fraction_max=0.8)
	print "\t compacting filtered tokens"
	sff.compactify()
	print "\t saving Sfile Filter to pkl format"
	sff.save(os.path.join(output,'%s-sff_file.pkl' % os.path.basename(direct)))

	name_filtered_vw_file = '%s-doc_tokens_filtered.vw' % os.path.basename(direct)
	print "\t saving Filtered VW file to %s" % name_filtered_vw_file

	# This will raise an error (KeyError due to doc_id), we can safely ignore it
	try:
		sff.filter_sfile(os.path.join(output,name_vw_file), os.path.join(output,name_filtered_vw_file))
	except:
		pass

	# 4 Run VW on fitlered outputs
	# rm -f *cache
	# vw --lda 20 --cache_file ddrs.cache --passes 10 -p prediction.dat 
	# --readable_model topics.dat --bit_precision 16 filtered.vw --minibatch 2

	print "Running VW Latent Dirlecht Allocation"
	print "\t number of topics = %d" % num_topics
	print "\t number of passes = %d" % num_passes
	call(["rm","-f",os.path.join(output,"*cache")])
	call(["vw","--lda",str(num_topics),"--cache_file",os.path.join(output,"ddrs.cache"),"--passes",str(num_passes),"-p",os.path.join(output,"%s-prediction.dat" % os.path.basename(direct)),"--readable_model",os.path.join(output,"%s-topics.dat" % os.path.basename(direct)),"--bit_precision","16",os.path.join(output,name_filtered_vw_file),"--minibatch","2"])


	# 5 Output results
	print "Writing out results"
	lda = LDAResults(os.path.join(output,'%s-topics.dat' % os.path.basename(direct)), os.path.join(output,'%s-prediction.dat' % os.path.basename(direct)), os.path.join(output,'%s-sff_file.pkl' % os.path.basename(direct)), num_topics=num_topics)
	lda.print_topics(num_words = 10,outfile = os.path.join(output,'%s-LDA_results.txt' % os.path.basename(direct)))


if __name__ == '__main__':
	main()