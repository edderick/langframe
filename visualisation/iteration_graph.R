#!/usr/bin/RScript

library(ggplot2)

# read colour data from STDIN into appropriate matrix form
distances <- read.delim("stdin", 
            sep=",", 
            allowEscapes=TRUE,
            stringsAsFactors=TRUE,
            header=TRUE)

distances$i <- seq(0,nrow(distances)-1)

# generate line plot
line.plot <- ggplot(data=distances, aes(x=i, y=distance, group=1)) + geom_line() + geom_point()

ggsave(file="line-output.pdf")
