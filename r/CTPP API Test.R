library(httr)
#key<-'1287jsfi$$$'
key<-readline(prompt = 'Enter your API key: ')

url<-"https://ctpp.macrosysrt.com/api/data/2016"
#query for tract data in state of california
q<-list('get'='group(A101101)','in'='state:06','for'='tract:*','size'=1000,'page'=1)

#query for tract data of the whole country
#q<-list('get'='group(A101101)','for'='tract:*','size'=1000,'page'=1)

x <- GET(url, add_headers('x-api-key' = key),query=q)
c <- rawToChar(x$content)
r <- jsonlite::fromJSON(c)
d1st<-r$data

no_pages=ceiling(r$total/r$size)

library(doParallel)
cl <- parallel::makeCluster(4)
doParallel::registerDoParallel(cl)
drest=foreach(x=2:no_pages, .combine='rbind') %dopar% {
  library(httr)
  q$page=x
  x <- GET(url, add_headers('x-api-key' = key),query=q)
  c <- rawToChar(x$content)
  r <- jsonlite::fromJSON(c)
  d<-r$data
}

stopCluster(cl)

result <- rbind(d1st,drest)
