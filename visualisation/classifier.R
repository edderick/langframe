#!/usr/bin/RScript


library(kknn)

args <- commandArgs(TRUE)
chosen.lang.name <- args[1]
k.nearest <- args[2]

all.data <- read.delim("stdin", sep=",", stringsAsFactors=TRUE, header=TRUE,
                        na.strings="")

# partition into training & test sets
data.train <- all.data[all.data$lang.name == paste(chosen.lang.name,".def",sep=""),]
data.test <- all.data[all.data$lang.name == chosen.lang.name,]

data.train[c("x","y","z")]
data.test[c("x","y","z")]

as.factor(data.train$word)~.

result <- kknn(formula=as.factor(data.train$word)~., 
                train=data.train[c("x","y","z")],
                test=data.test[c("x","y","z")], 
                k=1,
                distance=2, #minkowski distance 2 = euclidean
                kernel="rectangular")
data.test$word <- result$fitted.values

new.data <- rbind(data.train, data.test)
new.data
