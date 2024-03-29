library(tidyverse)
library(DT)
library(DMwR2)
library(GGally)
library(shiny)
library(shinythemes)
library(shinyWidgets)
library(plotly)
library(readxl)
library(shinyalert)
library(mice)
library(maps)
library(forecast)
library(shinyhelper)
library(shinyjs)

source("./visualization/disease_prevalence.R")
source("./visualization/state_comparison.R")
source("./visualization/acre_rejection.R")
source("./visualization/variety.R")
source("./dataimport/data_table.R")
source("./dataimport/paired.R")
source("./dataimport/outliers.R")
source("./dataimport/other_miss.R")
source("./test/chi_sqr.R")
source("./test/anova.R")
source("./predict/predict.R")

# Maximum upload size
options(shiny.maxRequestSize = 10 * 1024^3)

# Set theme for ggplot2
theme_set(theme_minimal())

# Correct Column Names
correct_names = c('SummerID', 'CY', 'CERT_N', 'LNAME', 'SNAME', 
                  'GCODE', 'VARIETY', 'VAR', 'V2', 'V3AR', 'S_GRW', 'S_G', 'S_YR', 'S_GCODE', 
                  'S_STATE', 'ACRES', 'I_CLASS', 'I_GEN', 'START_PLTG', 'DONE_PLTG', 'DATE_1ST', 
                  'INSPECTOR', 'INS_TITL', 'DAPS1', 'PLTCT_1', 'NO_LR_1ST', 'SR1_LR', 'NO_MOS_1ST', 
                  'SR1_MOS', 'NO_ST_1ST', 'SR1_ST', 'SR1_TOTV', 'NO_MIX_1ST', 'AC_MIX_1ST', 'SR1_MIX', 
                  'DATE_2ND', 'DAPS2', 'PLTCT_2', 'SR2_LR', 'SR2_MOS', 'SR2_ST', 'SR2_TOTV', 'NO_BRR_2ND', 
                  'SR2_BRR', 'NO_MIX_2ND', 'AC_MIX_2ND', 'SR2_MIX', 'PPA_MIX', 'SRF_LR', 'SRF_MOS', 
                  'SRF_ST', 'SRF_MIX', 'TOTVIR', 'BLEG_PCT_C', 'BLEG_PCT_N', 'RHIZOC', 'VERT_C', 
                  'VERT_N', 'ASTRYELOS', 'EBLIGHT', 'EBLIGHT_N', 'LBLIGHT', 'SCLEROTIN', 'WILT_PCT_C', 
                  'WILT_PCT_N', 'G_AND_VIG', 'INS_CONT', 'WEED_CONT', 'ISOLATION', 'STAND', 'COMMMENTS', 
                  'AC_PASSD', 'AC_REJ', 'S_CLASS', 'S_GEN', 'DN_CLASS', 'PRN_F', 'BR_F', 'PSTV_F', 
                  'LB_F', 'LAST_MOD', 'LAST_TIM', 'STOP', 'SF_HCNOT1', 'SF_HCNOT2', 'SF_HCNOT3', 
                  'SF_HCNOT4', 'SF_HCNOT5', 'SF_HCNOT6', 'SF_HCNOT7', 'ADDRESS', 'CITY', 'STATE', 
                  'ZIP', 'SF_HCNOT8', 'SF_HCNOT9', 'SF_HCNOT10', 'SF_HCNOT11', 'WinterID', 
                  'winter_CERT_N', 'winter_SNAME', 'winter_VAR', 'winter_TYPE', 'winter_ACRES', 
                  'winter_AD_SAMPS', 'winter_AC_PASSD', 'winter_WT_SAMP', 'winter_WT_A', 'winter_LNAME', 
                  'winter_GCODE', 'winter_VARIETY', 'winter_S_GRW', 'winter_S_G', 'winter_S_YR', 
                  'winter_S_GCODE', 'winter_S_STATE', 'winter_I_CLASS', 'winter_I_GEN', 'winter_S_CLASS', 
                  'winter_S_GEN', 'winter_DN_CLASS', 'winter_NS', 'winter_WT_LOC', 'winter_PLANTCT', 
                  'winter_LRN', 'winter_MOSN', 'winter_MXDN', 'winter_LR', 'winter_MOS', 'winter_MIX', 
                  'winter_PSTV', 'winter_BRR', 'winter_ELI_PLTS', 'winter_ELI_PPW', 'winter_ELI_POS', 
                  'winter_ELI_PVY', 'winter_LVS', 'winter_TBR', 'winter_TOTV', 'winter_CLASS', 
                  'winter_GEN', 'winter_PAYING', 'winter_SF_PROG', 'winter_FY', 'winter_DIP', 
                  'winter_AC_REJ', 'winter_CY', 'DAPS1_binned', 'DAPS2_binned', 'NO_LR_2ND', 'NO_MOS_2ND',
                  'NO_ST_2ND', 'NO_TOTV_2ND')

# Variables needed for visualization
vars_need = c("S_STATE","VARIETY",
              "PLTCT_1", correct_names[grepl("^NO.*_1ST$", correct_names)],
              "PLTCT_2", correct_names[grepl("^NO.*_2ND$", correct_names)],
              "S_YR", "winter_PLANTCT", "winter_MOSN",
              "winter_LRN", "winter_MXDN","LNAME", "ACRES", "AC_REJ", 
              "winter_ACRES", "winter_AC_REJ")

# Variables that should be paired
summer_cols = c("CERT_N",
                "VARIETY",
                # "S_G",
                "S_YR",
                "S_STATE",
                "LNAME")
n_vars = length(summer_cols)
winter_cols = paste0("winter_", summer_cols)