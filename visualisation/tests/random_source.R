#!/usr/bin/RScript

# Generates a random distribution of colour points and labels with some geographical
# similarity. May be representative of some final value.

# Splits RGB cube into 8 subcubes with name label, then randomly generates points
# in these subcubes

names.list <- c("black", "darkblue", "green", "red", "cyan", "yellow", 
                    "magenta", "white") # binary encoding of colour names 

# subcube.bounds contains a class label & a binary encoding of which subcube it
# is in. This is repeated n times.
subcube.bounds <- matrix(c(0,0,0,0,0,1,0,1,0,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1),
                            nrow=8, ncol=3, byrow=TRUE)
subcube.bounds <- as.data.frame(subcube.bounds)
subcube.bounds$labels <- names.list
names(subcube.bounds) <- c("r","g","b", "labels")

n <- 4 #TODO: get this via commandline
subcube.bounds <- do.call("rbind", replicate(n, subcube.bounds, simplify=FALSE))

# randomly generate a point for some subcube
row.random.point <- function(rgb) {
    mins <- rgb*127
    maxs <- mins + 128
    random.r <- sample(mins[1]:maxs[1],1)
    random.g <- sample(mins[2]:maxs[2],1)
    random.b <- sample(mins[3]:maxs[3],1)
    return (c(random.r, random.g, random.b))
}

# subcube.points contains random points and section labels
subcube.points <- t(apply(subcube.bounds[c("r","g","b")], 1, row.random.point))
subcube.points <- as.data.frame(subcube.points)
subcube.points$labels <- names.list
names(subcube.points) <- c("r","g","b", "labels")
