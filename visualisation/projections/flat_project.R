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
lang.name <- args[1]
projection.type <- args[2]

all.data <- read.delim("stdin",
                sep=",",
                stringsAsFactors=TRUE,
                header=TRUE,
                na.strings="")

new.name.test <- paste(lang.name, "_", projection.type, sep="")
new.name.def <- paste(lang.name, "_", projection.type, ".def", sep="")

def.subset.log <- grepl("def$", all.data$lang.name)
test.subset.log <- !def.subset.log

def.subset <- all.data[def.subset.log,]
test.subset<- all.data[test.subset.log,]

def.subset$lang.name <- new.name.def
test.subset$lang.name <- new.name.test

all.data <- rbind(def.subset, test.subset)

# project onto RG subspace

if (projection.type == "RG") {
    all.data$z <- rep(0, nrow(all.data))
} else if (projection.type == "GB") {
    all.data$x <- rep(0, nrow(all.data))
} else if (projection.type == "RB") {
    all.data$y <- rep(0, nrow(all.data))
}

write.table(all.data, quote=FALSE, sep=",", row.names=FALSE)
