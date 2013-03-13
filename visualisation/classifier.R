#!/usr/bin/RScript


args <- commandArgs(TRUE)
chosen.lang.name <- args[1]
k.nearest <- args[2]

all.data <- read.delim("stdin", sep=",", stringsAsFactors=TRUE, header=TRUE,
                        na.strings="")

# partition into training & test sets (training has ".def" at end)
data.train <- all.data[all.data$lang.name == paste(chosen.lang.name,".def",sep=""),]
data.test <- all.data[all.data$lang.name == chosen.lang.name,]

# KNN classification algorithm for a single element of the test set
knn.classify <- function(element) {
    train <- data.train

    elem.x <- as.numeric(element[['x']])
    elem.y <- as.numeric(element[['y']])
    elem.z <- as.numeric(element[['z']])

    square.errors <- (train$x - elem.x)^2 + (train$y - elem.y)^2 + (train$z - elem.z)^2
    k.nearest.indices <- order(square.errors, decreasing=FALSE)[1:k.nearest]
    k.nearest.words <- data.train$word[k.nearest.indices]

    unique.words <- unique(k.nearest.words)
    mode.avg.word <- unique.words[which.max(tabulate(match(k.nearest.words, unique.words)))]

    return (mode.avg.word)
}

# perform KNN classification on new data points to get colour labels
new.colours <- apply(data.test, 1, knn.classify)
data.test$word <- new.colours

new.data <- rbind(data.train, data.test)

write.table(new.data, quote=FALSE, sep=",", row.names=FALSE)
