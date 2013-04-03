#!/usr/bin/RScript

# This generates a 3D plot with the positions of the means for each colour label

library(lattice)
args <- commandArgs(TRUE)

all.data <- read.delim("stdin", sep=",", stringsAsFactors=TRUE, header=TRUE,
                        na.strings="")

for(lang in levels(all.data$lang.name)) {
    relevant.rows <- subset(all.data, all.data$lang.name == lang)

    attach(relevant.rows)
    my.cols <- c("black", "darkblue", "green", "red", "cyan", "yellow", "magenta", "gray")
    my.labels <- c("black", "darkblue", "green", "red", "cyan", "yellow", "magenta", "gray")
    axis.lim <- c(0, 255)
    axis.scales <- list(tick.number=10)

    graph.name <- paste("means for ", lang, sep="")

    graph <- cloud(b~r*g, main=graph.name, col=my.cols, pch=20, cex=2.5, shade=TRUE,
        xlim=axis.lim, ylim=axis.lim, zlim=axis.lim)
    print(graph)
}
