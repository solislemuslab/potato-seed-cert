# Test Tab
chi2_subtab <- 
  tabPanel(
    value = "chi2",
    "Chi-square Test",
    h3("Observation Table"),
    dataTableOutput("observe_dt"),
    h3("Chi-Square Test Result"),
    dataTableOutput("chi2_dt")
  )

anova_subtab <- 
  tabPanel(
    value = "anova",
    "ANOVA",
    h3("Data Table"),
    dataTableOutput("anova_dt"),
    h3("ANOVA Test Result"),
    dataTableOutput("anova_res_dt")
  )


## Aggregation
test_tab <- 
  tabPanel(
    "Test",
    conditionalPanel(
      condition = "output.noMissingValues",
      sidebarLayout(
        sidebarPanel(
          h3("Data Selection"),
          pickerInput(
            inputId = "test_state",
            label = "State",
            choices = c("WI"),
            multiple = T,
            options = list(`actions-box` = T,
                           `live-search` = T)
          ),
          
          sliderInput(
            inputId = "test_year",
            label = "Year",
            min = 0,
            max = as.numeric(format(Sys.Date(), "%Y")),
            value = c(0, as.numeric(format(Sys.Date(), "%Y")))
          ),
          
          pickerInput(
            inputId = "test_disease",
            label = "Disease",
            choices = c("BLEG_PCT_C", "RHIZOC", "VERT_C",
                        "ASTRYELOS", "EBLIGHT"	, "LBLIGHT", "WILT_PCT_C"),
            multiple = F,
            options = list(`live-search` = T)
          
            ),
          
          pickerInput(
            inputId = "test_var",
            label = "Source Variable",
            choices = c("SNAME",
                        "GCODE",
                        "VARIETY",
                        "S_G"),
            multiple = F,
            options = list(`live-search` = T)
          ),
          
          radioButtons(
            inputId = "test_alpha",
            label = "Significance Level",
            choices = c(0.01, 0.05, 0.1),
            selected = 0.05
          ),
          helpText("The null hypothesis is that the infection rate of selected disease type is \
                   independent with the selected source variable, \
                   and the alternative hypothesis is that they are associated."),
        ),
        mainPanel(
          fluidRow(
            tabsetPanel(
              id = "test_subtabs",
              chi2_subtab,
              anova_subtab
            )
          )
        )
        
      ))
  )
