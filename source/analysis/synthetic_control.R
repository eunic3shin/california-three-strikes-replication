# Recovered from the historical California synthetic-control notebooks.
# Usage: Rscript source/analysis/synthetic_control.R PANEL NASBO_XLSM OUTPUT_DIR
library(Synth)
library(readxl)
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==3)
out <- args[3]; dir.create(out,recursive=TRUE,showWarnings=FALSE)
df <- read.csv(args[1])
# Historical filled panel used zeros for missing incarceration and spending.
for (v in c("Corrections.Normalized","Incarcerated.Normalized",
            "Total.Corrections.Spending","Total.People.Incarcerated"))
  df[[v]][is.na(df[[v]])] <- 0
df$state_id <- as.numeric(as.factor(df$State))
ca <- unique(df$state_id[df$State=="California"])
# The initial path notebook used any zero-policy observation, not never-treated states.
donors <- unique(df$state_id[df$X3.Strikes.Law.==0 & df$State!="California"])
fit <- function(d,treated,controls,dependent,predictors,years,yearcol="Year",special=NULL) {
  dp <- dataprep(foo=as.data.frame(d), predictors=predictors,predictors.op="mean",
                 special.predictors=special,dependent=dependent,unit.variable="state_id",
                 time.variable=yearcol,treatment.identifier=treated,controls.identifier=controls,
                 time.predictors.prior=1991:1993,time.optimize.ssr=1991:1993,time.plot=years)
  model <- synth(dp)
  list(actual=as.numeric(dp$Y1plot),synthetic=as.numeric(dp$Y0plot %*% model$solution.w),
       weights=as.numeric(model$solution.w))
}
png_path <- function(name,years,actual,synthetic,ylabel) {
  png(file.path(out,name),width=1800,height=1200,res=200)
  plot(years,actual,type="l",lwd=2,col="black",ylim=range(c(actual,synthetic)),
       xlab="Year",ylab=ylabel)
  lines(years,synthetic,col="steelblue",lty=2,lwd=2); abline(v=1994,lty=3)
  legend("topright",c("California","Synthetic California"),col=c("black","steelblue"),lty=c(1,2),bty="n")
  dev.off()
}
years <- 1991:1999
a <- fit(df,ca,donors,"Arrest.Rate.per.100.000",c("Corrections.Normalized","Incarcerated.Normalized"),years)
png_path("ArrestsCAvsSynth.png",years,a$actual,a$synthetic,"Historical arrest rate per 100,000")
write.csv(data.frame(year=years,actual=a$actual,synthetic=a$synthetic),file.path(out,"arrests_synthetic.csv"),row.names=FALSE)
# Spending path and placebo: original workbook, original pre-period predictors.
s <- as.data.frame(read_excel(args[2],sheet="STATE EXP REPORT DATA"))
names(s)[2] <- "State"
s <- s[!is.na(s$State) & s$YEAR %in% 1991:2024,]
s$state_id <- as.numeric(as.factor(s$State))
ca_s <- unique(s$state_id[s$State=="California"])
donor_names <- unique(df$State[df$X3.Strikes.Law.==0 & df$State!="California"])
sdon <- unique(s$state_id[s$State %in% donor_names])
special <- lapply(1991:1993,function(y) list("CORR_TOT",y,"mean"))
sp <- fit(s,ca_s,sdon,"CORR_TOT","TOTAL_CAPI",1991:2024,"YEAR",special)
png_path("corrections.png",1991:2024,sp$actual,sp$synthetic,"Corrections spending ($ millions)")
png(file.path(out,"TotalCorrSpend.png"),width=1800,height=1200,res=200)
plot(1991:2024,sp$actual,type="b",pch=16,xlab="Year",ylab="Corrections spending ($ millions)")
abline(v=1994,lty=2); dev.off()
write.csv(data.frame(year=1991:2024,actual=sp$actual,synthetic=sp$synthetic),file.path(out,"spending_synthetic.csv"),row.names=FALSE)
b <- s[s$YEAR %in% 1991:2000,]
valid <- names(which(table(b$state_id)==10))
b <- b[b$state_id %in% as.numeric(valid),]
ids <- setdiff(unique(b$state_id),ca_s)
base <- fit(b,ca_s,ids,"CORR_TOT","TOTAL_CAPI",1991:2000,"YEAR",special)
gaps <- lapply(ids,function(id) tryCatch({
  f <- fit(b,id,setdiff(ids,id),"CORR_TOT","TOTAL_CAPI",1991:2000,"YEAR",special)
  f$actual-f$synthetic
},error=function(e) {message("Placebo failed: ",id,": ",conditionMessage(e)); NULL}))
gaps <- Filter(Negate(is.null),gaps)
if (!length(gaps)) stop("No successful placebo fits")
g <- do.call(cbind,gaps); treated <- base$actual-base$synthetic
png(file.path(out,"Placebo.png"),width=1800,height=1200,res=200)
matplot(1991:2000,g,type="l",lty=1,col="grey",ylim=range(c(g,treated)),xlab="Year",ylab="Gap in corrections spending")
lines(1991:2000,treated,col="red",lwd=2); abline(v=1994,lty=2); dev.off()
write.csv(data.frame(year=1991:2000,california=treated,g),file.path(out,"placebo_gaps.csv"),row.names=FALSE)
