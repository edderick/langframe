#!/usr/bin/RScript

# Projects input points to (R,G) or (G,B) or (R,B) onto 2D subspaces (flat/parallel
# projection... this is used to prove how unrealistic it is for visualisation 
# purposes)
#
# USAGE: ./flat_project.R [subspace]
#                           where [subspace] = RG or GB or RB
# INPUT: standard language format
# OUTPUT: standard language format + x,y for 2D projected co-ordinates

args <- commandArgs(TRUE)

# assume RG subspace for now

all.data <- read.delim("stdin",
                sep=",",
                stringsAsFactors=TRUE,
                header=TRUE,
                na.strings="")

# project onto RG subspace
all.data$x <- switch(args[1],
    "RG"=all.data$g,
    "GB"=all.data$g,
    "RB"=all.data$r,
    {print("no subspace arg")}
)

all.data$y <- switch(args[1],
    "RG"=all.data$r,
    "GB"=all.data$b,
    "RB"=all.data$b,
    {print("no subspace arg")}
)

write.table(all.data, quote=FALSE, sep=",", row.names=FALSE)
