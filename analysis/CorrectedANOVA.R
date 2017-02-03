library(car)
library(readr)
library(PMCMR)
##########################################################
# By Race
##########################################################
aggByRace <- read_csv("~/Workspace/MICA/data/R/aggByRace.csv")
aggByRace$race <- as.factor(aggByRace$race)

degree <- aggByRace[aggByRace$centrality == "degree_cent", ]
betweenness <- aggByRace[aggByRace$centrality == "betweenness_cent",]

# Levene's test for homoscedasticity
leveneTest(value ~ race, data = degree)
leveneTest(value ~ race, data = betweenness)

# Kruskal-Wallis test
kruskal.test(value ~ race, data = degree)
kruskal.test(value ~ race, data = betweenness)


posthoc.kruskal.nemenyi.test(value ~ race, data = degree, method = "Tukey")

posthoc.kruskal.nemenyi.test(value ~ race, data = betweenness, method = "Tukey")


##########################################################
# By Age
##########################################################
aggByAgeGender <- read_csv("~/Workspace/MICA/data/R/aggByAgeGender.csv")

degree <- aggByAgeGender[aggByAgeGender$centrality == "degree_cent",]
betweenness <- aggByAgeGender[aggByAgeGender$centrality == "betweenness_cent", ]

mod <- lm(value ~ age, data = degree)
mod
summary(mod)

mod <- lm(value ~ age, data = betweenness)
summary(mod)

