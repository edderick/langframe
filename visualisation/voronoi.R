#!/usr/bin/RScript

library(tripack)
library(ggplot2)

# read colour data from STDIN into appropriate matrix form
colours <- read.delim("stdin", 
            sep=",", 
            stringsAsFactors=TRUE,
            header=FALSE, 
            na.strings="")
names(colours) <- c("label", "r", "g", "b", "word")
col.values <- colours[c('r', 'g', 'b')] / 255

colours
col.values

avg.r <- tapply(col.values$r, colours$word, mean)
avg.g <- tapply(col.values$g, colours$word, mean)
avg.b <- tapply(col.values$b, colours$word, mean)

avg.for.r <- lapply(colours$word, function(word) avg.r[word])
avg.for.g <- lapply(colours$word, function(word) avg.g[word])
avg.for.b <- lapply(colours$word, function(word) avg.b[word])

# generate & display Voronoi (nearest neighbour polygon
# visualisation) and display on top
twodcolour.vm <- voronoi.mosaic(colours$r, colours$g,
                        duplicate="remove" )
plot(twodcolour.vm,
            sub="for sample 2D colour data",
            col="gray",
            xlab="r",
            ylab="g" 
            )

# plot known colour points (R,G values)
points(colours[c("r","g")], 
        pch=21, 
        cex=1.8,
        col="gray",
        bg=rgb(avg.for.r, avg.for.g, avg.for.b))

warnings()
