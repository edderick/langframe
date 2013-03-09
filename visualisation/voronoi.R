#!/usr/bin/RScript

library(tripack)
library(ggplot2)

# read colour data from STDIN into appropriate matrix form
colours <- read.delim("stdin", 
            sep=",", 
            stringsAsFactors=TRUE,
            header=TRUE)
colours

# scale 0-255 colour values to 0-1 range, so they can be displayed
colours[c('r', 'g', 'b')] <- colours[c('r', 'g', 'b')] / 255

# calculate average of each colour label for display purposes
avg.r.for <- tapply(colours$r, colours$word, mean)
avg.g.for <- tapply(colours$g, colours$word, mean)
avg.b.for <- tapply(colours$b, colours$word, mean)

avg.r <- lapply(colours$word, function(word) avg.r.for[word])
avg.g <- lapply(colours$word, function(word) avg.g.for[word])
avg.b <- lapply(colours$word, function(word) avg.b.for[word])

# generate & display Voronoi (nearest neighbour polygon
# visualisation) and display on top
twodcolour.vm <- voronoi.mosaic(colours$x, colours$y,
                        duplicate="remove" )
plot(twodcolour.vm,
            main="Voronoi plot",
            sub=paste("Language: ", colours$lang.name[1]),
            col="gray",
            xlab="x",
            ylab="y" 
            )

# plot known colour points (with colour of the average for its word)
points(colours[c("x","y")], 
        pch=21, 
        cex=1.8,
        col="gray",
        bg=rgb(avg.r, avg.g, avg.b))
