# LDA-Pipeline

## Author
David Folarin @ Cornell University 2015  
Under Megan French & Jeff Hancock  
Provides one line command for topic modeling using LDA  

## Requisites
* Python 2.7
* Vowpal Wabbit (Yahoo Research)
* Rosetta (Columbia applied data science)
 
Recommended: create virtual environment then use 

	pip install requirements.txt

to install python requirements.

Then clone Vowpal Wabbit's github repo and:

	cd vowpal_wabbit
	make

Note: Vowpal Wabbit depends on boost headers

## Usage

	python topicModelingPipeline.py <path to directory containing source files> <path to directory where output 	goes> <number of topics to generate> <number of passes>

