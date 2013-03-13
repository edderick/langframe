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

if (projection.type == "RG") {
    all.data$z <- rep(0, nrow(all.data))
} else if (projection.type == "GB") {
    all.data$x <- rep(0, nrow(all.data))
} else if (projection.type == "RB") {
    all.data$y <- rep(0, nrow(all.data))
}

write.table(all.data, quote=FALSE, sep=",", row.names=FALSE)
