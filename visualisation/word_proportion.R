#!/usr/bin/RScript

# This script takes CSV data from stdin for multiple (labelled) languages
# and produces the proportion of the words by language (i.e. to see if this
# technique causes single words to dominate)

# USAGE: ./word_proportion.R graph_filename
# INPUT: standard language format
# OUTPUT: graph at graph_filename.pdf

library(ggplot2)

# output file name as first arg
args <- commandArgs(TRUE)
pdf.file.name <- paste(args[1], ".pdf", sep="")


# read colour data from STDIN into appropriate matrix form
samples <- read.delim("stdin", 
            sep=",", 
            allowEscapes=TRUE,
            stringsAsFactors=TRUE,
            header=TRUE)

ggplot(samples, aes(x=lang.name,fill=word)) + geom_bar(position="fill")
ggsave(file=pdf.file.name)
