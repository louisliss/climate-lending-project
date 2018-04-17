install.packages("acs", dependencies = TRUE)
install.packages("stringr", dependencies = TRUE)

library(acs)
api.key.install(key = "59ef174adf6578015696e7157c5ca14172805a61")

bostontracts <- geo.make(state=25, county = "Suffolk", tract = "*")

pop2016.data <- acs.fetch(geography=bostontracts, table.number = "B01003", endyear = 2016, col.names = "pretty")
pop2016 = data.frame(estimate(pop2016.data))
names(pop2016) = c("2016_pop")



rm(pop2016)
