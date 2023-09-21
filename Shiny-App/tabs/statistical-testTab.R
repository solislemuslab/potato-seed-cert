# Statistical Test

chi2_subtab <- 
  tabPanel(
    "Chi-square Test",
    dataTableOutput("chi2_dt", height = "700px")
  )

anova_subtab <- 
  tabPanel(
    "ANOVA",
    dataTableOutput("anova_dt", height = "700px")
  )


## Aggregation

stat_test_tab <- 
  tabPanel(
    "Statistical Test",
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
        
        pickerInput(
          inputId = "test_grower",
          label = "Grower",
          choices = c(0),
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
        
        fluidRow(
          column(
            6,
            pickerInput(
              inputId = "test_disease_disc",
              label = "Disease (Discrete)",
              choices = c("BLEG_PCT_C", "RHIZOC", "VERT_C",
                          "ASTRYELOS", "EBLIGHT"	, "LBLIGHT", "WILT_PCT_C"),
              multiple = F,
              options = list(`live-search` = T)
            )
          ),

          column(
            6,
            pickerInput(
              inputId = "test_disease_cont",
              label = "Disease (Continuous)",
              choices = c("SR1_MOS", "SR2_MOS", "SR1_LR"),
              multiple = F,
              options = list(`live-search` = T)
            )
          )

        ),
        
        pickerInput(
          inputId = "test_var",
          label = "Source Variable",
          choices = c("SNAME",
                      "GCODE",
                      "VARIETY",
                      "S_GRW",
                      "S_G",
                      "S_YR",
                      "S_GCODE",
                      "S_STATE"),
          multiple = F,
          options = list(`live-search` = T)
        ),
        
        radioButtons(
          inputId = "test_alpha",
          label = "Significance Level",
          choices = c(0.01, 0.05, 0.1),
          selected = 0.05
        )
      ),
      mainPanel(
        fluidRow(
          tabsetPanel(
            chi2_subtab,
            anova_subtab
          )
        )
      )
      
    )
  )
