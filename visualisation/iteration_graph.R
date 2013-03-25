#!/usr/bin/RScript

library(ggplot2)

# output file name as first arg
args <- commandArgs(TRUE)
pdf.file.name <- paste(args[1], ".pdf", sep="")


# read colour data from STDIN into appropriate matrix form
distances <- read.delim("stdin", 
            sep=",", 
            allowEscapes=TRUE,
            stringsAsFactors=FALSE,
            header=TRUE)


# get bit of string after "_" (i.e. iteration number)
distances$i <- as.numeric(substr(distances$lang2, 7, nchar(distances$lang2)))

# generate line plot
line.plot <- ggplot(data=distances, 
    aes(x=i, y=distance, group=1)) + ylim(0,1) + geom_line() + geom_point()

ggsave(file=pdf.file.name)
