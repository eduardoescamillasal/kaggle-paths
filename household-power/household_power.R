install.packages("forecast")
install.packages("dygraphs")
install.packages("lubridate")

library("forecast")
library(plyr)
library(lubridate)


setwd("~/Github/kaggle-paths/household-power")
powerdata = read.csv("data/household_power_consumption.txt", sep=';')
head(powerdata["Global_active_power"])
tail(powerdata["Global_active_power"])



reframedpowerdata = powerdata
reframedpowerdata$Global_active_power <- revalue(reframedpowerdata$Global_active_power, c("?"="0"))

ndiffs(reframedpowerdata$Global_active_power)

#decimal_date(as.Date("2006-12-16:17:24:00"))
#timeDate <- as.POSIXct("2006-12-17 17:24")
#str(timeDate)
#starttime <- timeDate

starttime <- c(2006, 12, 16, 17, 24)
endtime <- c(2010, 11, 26, 21, 02)
global_active_power <- ts(reframedpowerdata$Global_active_power, start = starttime, end=endtime, frequency = 24*60*365)
plot(global_active_power, ylab = "Global active power")


ndiffs(global_active_power)
nsdiffs(global_active_power)

cbind("Global active power" = global_active_power,
      "Log Global active power" = log(global_active_power),
      "Annual change in log" = diff(log(global_active_power),12)) %>%
  autoplot(facets=TRUE) +
  xlab("Year") + ylab("") +
  ggtitle("Global active power")


head(global_active_power)

