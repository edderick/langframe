#!/usr/bin/RScript

# Projects input points to (R,G) or (G,B) or (R,B) onto 2D subspaces (flat/parallel
# projection... this is used to prove how unrealistic it is for visualisation 
# purposes)
#
# USAGE: ./flat_project.R [subspace]
#                           where [subspace] = RG or GB or RB
# INPUT: standard language format
# OUTPUT: standard language format

args <- commandArgs(TRUE)
projection.type <- args[1]

all.data <- read.delim("stdin",
                sep=",",
                stringsAsFactors=TRUE,
                header=TRUE,
                na.strings="")
all.data$lang.name <- paste(all.data$lang.name, "_", projection.type, sep="")

# project onto RG subspace
all.data$x <- switch(args[1],
    "GB"=rep(0, len(all.data),
    {print("no subspace arg")}
)

all.data$y <- switch(args[1],
    "RB"=rep(0, len(all.data),
    {print("no subspace arg")}
)

all.data$z <- switch(args[1],
    "RG"=rep(0, len(all.data),
    {print("no subspace arg")}
)

write.table(all.data, quote=FALSE, sep=",", row.names=FALSE)
