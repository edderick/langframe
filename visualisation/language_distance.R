#!/usr/bin/RScript

# This script takes CSV data from stdin for multiple (labelled) languages
# and works out an estimated distance between the languages (essentially
# the percentage of a random sample of utterances whose meaning is agreed between
# the two languages)

# include as args comma-separated pairs of language labels to compare, e.g. to
# compare lang1 with lang2 and lang2 with lang3

# USAGE: ./language_distance.R lang1,lang2 lang2,lang3
#           -k --nearest : how many nearest neighbours?
#           -n --samples : how many random points to test?
#           -f --flat    : if this flag is present, use (x,y) at end for calculating
#                           k nearest neighbours
# INPUT: standard language format
# OUTPUT: single value measure of distance

library(optparse)

# parse command line arguments
option.list <- list(
    make_option(c("-k", "--nearest"), type="integer", default=1),
    make_option(c("-n", "--samples"), type="integer", default=100),
    make_option(c("-f", "--flat"), action="store_true", default=FALSE) )

option.parser <- OptionParser(usage="usage: %prog [options]",
                                option_list=option.list,
                                add_help_option=TRUE)

options <- parse_args(option.parser, args=commandArgs(trailingOnly=TRUE),
                        positional_arguments=TRUE)

k.nearest <- options$options$nearest
n.samples <- options$options$samples
use.flat <- options$options$flat
lang.pairs <- options$args

# collect data from stdin into data frame
all.data <- read.delim("stdin",
                sep=",",
                stringsAsFactors=TRUE,
                header=TRUE,
                na.strings="")

# for each 2-combination of language labels to compare...
for(pair in args) {
    # work out names (should be 2 comma-separated labels)
    langs <- strsplit(pair, ",")
    lang.name.1 <- langs[[1]][1]
    lang.name.2 <- langs[[1]][2]

    # select these labels
    data.l1 <- subset(all.data, lang.name==lang.name.1)
    data.l2 <- subset(all.data, lang.name==lang.name.2)

    # calculate which proportion are differently labelled
    count.total <- nrow(data.l1)
    count.diff <- sum(data.l1$word != data.l2$word)
    count.proportion.error <- count.diff / count.total
    print (count.proportion.error)
}
