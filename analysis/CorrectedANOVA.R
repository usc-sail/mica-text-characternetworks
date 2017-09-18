##########################################################
# Install missing packages
##########################################################
list.of.packages <- c("car", "readr", "PMCMR")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos="http://cran.stat.ucla.edu/")

##########################################################
# Command line arguments
##########################################################
args <- commandArgs(TRUE)
by <- args[1]
f <- args[2]

setwd(".")

print("CorrectedANOVA.R")
print(paste("CWD: ", getwd()))
print(paste("Analyzing by: ", by))
print(paste("File: ", f))

##########################################################
# Imports
##########################################################
library(car)
library(readr)
library(PMCMR)

if(by == "race"){
	##########################################################
	# By Race
	##########################################################
	aggByRace <- read_csv(f)
	aggByRace$race <- as.factor(aggByRace$race)
	degree <- aggByRace[aggByRace$centrality == "degree_centrality", ]
	betweenness <- aggByRace[aggByRace$centrality == "betweenness_centrality",]

	# Levene's test for homoscedasticity
	print("Levene's test")
	print("Degree: ")
	r <- leveneTest(value ~ race, data = degree)
	print(r)
	print("")
	print("")
	print("Betweenness: ")
	r <- leveneTest(value ~ race, data = betweenness)
	print(r)
	print("")
	print("")

	# Kruskal-Wallis test
	kruskal.test(value ~ race, data = degree)
	kruskal.test(value ~ race, data = betweenness)


	posthoc.kruskal.nemenyi.test(value ~ race, data = degree, method = "Tukey")

	posthoc.kruskal.nemenyi.test(value ~ race, data = betweenness, method = "Tukey")

}else if(by == "age"){

	##########################################################
	# By Age
	##########################################################
	aggByAgeGender <- read_csv(f)

	degree <- aggByAgeGender[aggByAgeGender$centrality == "degree_centrality",]
	betweenness <- aggByAgeGender[aggByAgeGender$centrality == "betweenness_centrality", ]

	mod <- lm(value ~ age, data = degree)
	print(mod)
	summary(mod)

	mod <- lm(value ~ age, data = betweenness)
	summary(mod)

}else{
	print(paste("Argument #1 not understood. Should be either 'race' or 'age'."))
}



