#!/usr/bin/RScript

library(tripack)
library(ggplot2)

# read colour data from STDIN into appropriate matrix form
colours <- read.delim("stdin", 
            sep=",", 
            stringsAsFactors=TRUE,
            header=FALSE, 
            na.strings="")
names(colours) <- c("r", "g", "b", "word")
col.values <- colours[c('r', 'g')] / 255

colours
col.values

# plot known colour points (R,G values)
plot(colours[c("r","g")], pch=21, bg=rgb(col.values$r,col.values$g,1))

# generate & display Voronoi (nearest neighbour polygon
# visualisation) and display on top
twodcolour.voronoi <- voronoi.mosaic(colours$r, colours$g,
                        duplicate="remove" )
plot(twodcolour.voronoi,
            main="Voronoi Plot",
            sub="for sample 2D colour data",
            xlim=c(0,255),
            ylim=c(0,255),
            add=TRUE)
