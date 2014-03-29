require(tm)

tokenized <- read.csv("~/cy_learn/textmining/tokenized.csv", stringsAsFactors= FALSE, header=FALSE)
training.corpus <- Corpus(VectorSource(tokenized[,2], encoding = "UTF-8"))
tdm <- TermDocumentMatrix(training.corpus, control=list(wordLengths = c(2, 20), tolower=FALSE, weighting = function(x) weightTfIdf(x, normalize = FALSE)))

spar.min <- (422 - 3) / 422

cleantdm <- removeSparseTerms(tdm, spar.min) 
stopwords <- readLines("~/cy_terms/hk_stopwords.txt")
tdm_m <- as.matrix(cleantdm)[!dimnames(cleantdm)[[1]] %in% stopwords,]
tdm_m <- tdm_m[grep("[[:punct:]]", row.names(tdm_m), invert=TRUE), ]
tdm_m <- tdm_m[grep("^[0-9]+$", row.names(tdm_m), invert=TRUE), ]


approve <- read.csv("approve.csv", stringsAsFactors=FALSE)
require(lubridate)
approve$date <- dmy(approve[,2], tz="")

smooth <- function(index, approve) {
  cat(index)
  d1 <- approve[index,2]
  d2 <- approve[index+1,2]
  #cat("hello")
  datewithin <- seq(d2 + days(1), d1 - days(1), by = "day")
  r1 <- approve[index,1]
  r2 <- approve[index+1,1]
  diff <- r1 - r2
  aveJump <- diff / (length(datewithin) - 1)
  sm <- r2 + aveJump * 1:length(datewithin)
  tobereturn <- rbind(data.frame(approval = sm,  date = datewithin), approve[index,])
  return(tobereturn[order(tobereturn$date, decreasing=TRUE),])
}

require(plyr)
approvalsm <- ldply(seq(1,41, 1), smooth, approve = approve)
### hack
approvalsm[397,1] <- mean(approvalsm[398,1] ,approvalsm[396,1])
approvalsm <- rbind(approvalsm, approve[nrow(approve), ])

target <- approvalsm$approval[match(dmy(tokenized[,1], tz="") + days(8), approvalsm$date)]

allcor <- sapply(1:dim(tdm_m)[1],  function(i) { cor(target, tdm_m[i,]) } )

featureselect <- data.frame(terms = rownames(tdm_m), corImp = allcor)

top400 <- featureselect[order(featureselect$corImp, decreasing=FALSE),][1:280,]
top400$corImp <- -top400$corImp

js_array <- c()
for (i in 1:nrow(top400)) {
  js_array[i] <- paste0('["', top400[i,1], '", "', round(top400[i,2] * 200 ,3), '"]')
}

cat(readLines("~/cy_learn/textmining/header.txt"), paste(js_array, collapse=" , " ), readLines("~/cy_learn/textmining/footer.txt"), file="~/cy_learn/cy_learn/hkupop.html")
