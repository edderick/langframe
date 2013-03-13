#!/usr/bin/Rscript

# "Sampler" + "Amplifier"
# Using a language definition on stdin (lang.name + ".def"), this will generate n 
# random samples with (r,g,b) and (x,y,z) values
# USAGE: ./samplifier [langname] [num.samples]

args <- commandArgs(TRUE)
lang.name <- args[1]
n.samples <- args[2]

all.data <- read.delim("stdin",
                 sep=",",
                 stringsAsFactors=TRUE,
                 header=TRUE,
                 na.strings="")

col.lang.name <- rep(lang.name, n.samples)
col.r <- sample(0:255, n.samples, replace=TRUE)
col.g <- sample(0:255, n.samples, replace=TRUE)
col.b <- sample(0:255, n.samples, replace=TRUE)
col.colour.name <- rep(NA, n.samples)

new.points <- data.frame(lang.name=col.lang.name, r=col.r, g=col.g, b=col.b,
                            word=col.colour.name)

new.data <- rbind(all.data, new.points)

new.data$x <- new.data$r
new.data$y <- new.data$g
new.data$z <- new.data$b

write.table(new.data, quote=FALSE, sep=",", row.names=FALSE)
