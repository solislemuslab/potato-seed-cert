library(tidyverse)
library(DT)
library(DMwR2)
library(GGally)
library(shiny)
library(shinythemes)
library(shinyWidgets)
library(plotly)
library(readxl)
library(patchwork)
source("./visualization/disease_prevalence.R")
source("./visualization/state_comparison.R")
source("./visualization/acre_rejection.R")
source("./visualization/variety.R")
source("./dataimport/miss1.R")
theme_set(theme_minimal())

get_miss_rows = function(mydf, margin = 1){
  miss_r = which(!complete.cases(mydf) |
                   apply(
                     apply(mydf, 
                           MARGIN = c(1,2), 
                           FUN = function(x) grepl("^[ \t]+$", x)), 
                     MARGIN = margin, 
                     any) |
                   apply(
                     apply(mydf, 
                           MARGIN = c(1,2), 
                           FUN = function(x) nchar(x)==0), 
                     MARGIN = margin, 
                     any))
  return(miss_r)
}
