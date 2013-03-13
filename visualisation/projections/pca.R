#!/usr/bin/RScript

# Projects 3D points to 2D in more intelligent way than simple flat projections,
# maintaining more concept of distance.
#
# USAGE: ./pca.R [langname]
# INPUT: standard language format
# OUTPUT: standard language format

args <- commandArgs(TRUE)
lang.name <- args[1]

all.data <- read.delim("stdin",
                sep=",",
                stringsAsFactors=TRUE,
                header=TRUE,
                na.strings="")

# Add projection type to end of language name but make sure ".def" stays at 
# end of language name for training examples
new.name.test <- paste(lang.name, "_PCA", sep="")
new.name.def <- paste(lang.name, "_PCA.def", sep="")

def.subset.log <- grepl("def$", all.data$lang.name)
test.subset.log <- !def.subset.log

def.subset <- all.data[def.subset.log,]
test.subset<- all.data[test.subset.log,]

def.subset$lang.name <- new.name.def
test.subset$lang.name <- new.name.test

all.data <- rbind(def.subset, test.subset)

# project onto basis of two principal components
pc <- princomp(~x+y+z, all.data)
all.data$x <- round(pc$scores[,1])
all.data$y <- round(pc$scores[,2])
all.data$z <- rep(0, nrow(all.data))

write.table(all.data, quote=FALSE, sep=",", row.names=FALSE)
