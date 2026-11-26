# Recovered historical nonnegative, no-intercept synthetic incarceration fit.
# nnls solves the same least-squares objective as the notebook's positive regression.
library(nnls)
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==2)
d <- read.csv(args[1]); out <- args[2]; dir.create(out,recursive=TRUE,showWarnings=FALSE)
d <- d[d$Year %in% 1991:2005,]
# The historical notebook pivoted observed record counts and dropped incomplete states.
# The balanced DID input encodes absent records as zero; restore missingness here.
d$Total.People.Incarcerated[d$Total.People.Incarcerated == 0] <- NA_real_
wide <- reshape(d,idvar="Year",timevar="STATE",direction="wide")
wide <- wide[order(wide$Year),]
names(wide) <- sub("^Total.People.Incarcerated\\.","",names(wide))
excluded <- c("Year","California","Florida","Georgia","Indiana","Louisiana","Nevada","New Mexico","North Carolina","South Carolina","Texas","Washington","Wisconsin")
donors <- setdiff(names(wide)[colSums(is.na(wide))==0],excluded)
pre <- wide$Year %in% 1991:1993
w <- coef(nnls(as.matrix(wide[pre,donors,drop=FALSE]),wide$California[pre]))
syn <- as.numeric(as.matrix(wide[,donors,drop=FALSE]) %*% w)
keep <- wide$Year %in% 1991:1999
png(file.path(out,"Incarcerated.png"),width=1800,height=1200,res=200)
plot(wide$Year[keep],wide$California[keep],type="l",lwd=2,ylim=range(c(wide$California[keep],syn[keep])),xlab="Year",ylab="Incarceration records")
lines(wide$Year[keep],syn[keep],col="darkorange",lty=2,lwd=2); abline(v=1994,lty=3); dev.off()
post <- wide$Year %in% 1995:1999
png(file.path(out,"TreatIncarcerated.png"),width=1800,height=1200,res=200)
plot(wide$Year[post],wide$California[post]-syn[post],type="b",xlab="Year",ylab="California minus synthetic")
abline(h=0,lty=2); dev.off()
write.csv(data.frame(year=wide$Year,actual=wide$California,synthetic=syn),file.path(out,"incarceration_synthetic.csv"),row.names=FALSE)
