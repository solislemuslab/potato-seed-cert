# Visualization
## Disease Prevalence
disease_prevalence_subtab <- 
  tabPanel(
    "Disease Prevalence",
    sidebarLayout(
      sidebarPanel(
        h3("Data Selection"),
        pickerInput(
          inputId = "dis_pre_ins",
          label = "Inspection",
          choices = c("Summer", "Winter"),
          multiple = T,
          selected = "Summer",
          options = list(`actions-box` = T)
        ),
        pickerInput(
          inputId = "dis_pre_dis",
          label = "Disease",
          choices = c("MOS", "LR", "MIX", "ST", "BRR"),
          multiple = T,
          selected = c("LR", "ST"),
          options = list(`actions-box` = T)
        ),
        pickerInput(
          inputId = "dis_pre_state",
          label = "State",
          choices = c("WI"),
          multiple = F,
          options = list(`live-search` = T)
        ),
        pickerInput(
          inputId = "dis_pre_variety",
          label = "Variety",
          choices = c("Atlantic"),
          multiple = F,
          selected = "",
          options = list(`live-search` = T)
        ),
        helpText("The x-axis is Year, and y-axis is Percentage of potato \
                 with the chosen disease types.")
      ),
      mainPanel(
        plotlyOutput("plot_dis_pre", height = "700px")
      )
    )
  )

## State comparison
state_comparison_subtab <-
  tabPanel(
    "State Comparison",
    sidebarLayout(
      sidebarPanel(
        h3("Data Selection"),
        pickerInput(
          inputId = "state_comp_state",
          label = "State",
          choices = c("WI"),
          multiple = T,
          options = list(`actions-box` = T,
                         `live-search` = T)
        ),
        pickerInput(
          inputId = "state_comp_ins",
          label = "Inspection",
          choices = c("Summer_1st", "Summer_2nd", "Winter"),
          multiple = F
        ),
        sliderInput(
          inputId = "state_comp_year",
          label = "Year",
          min = 0,
          max = as.numeric(format(Sys.Date(), "%Y")),
          value = c(0, as.numeric(format(Sys.Date(), "%Y")))
        ),
        pickerInput(
          "state_comp_dis",
          "Disease",
          choices = c(),
          multiple = F
        ),
        helpText("The plot on top compares the average susceptibility in selected range \
                 of years of potato to different diseases in different states."),
        helpText("Each line corresponds to a state, x-axis corresponds to disease types, \
                 and y-axis corresponds to percentage of infection."),
        helpText("The map below compares certain disease infection rate between states.")
      ),
      mainPanel(
        plotlyOutput("plot_state_comp"),
        plotlyOutput("map_plot_state_comp")
      )
    )
  )

## ACRE Rejection
acre_rejection_subtab <- 
  tabPanel(
    "Acre Rejection",
    sidebarLayout(
      sidebarPanel(
        h3("Data Selection"),
        pickerInput(
          inputId = "acre_lot",
          label = "Lot Name",
          choices = c(""),
          multiple = T,
          options = list(`actions-box` = T,
                         `live-search` = T)
        ),
        pickerInput(
          inputId = "acre_variety",
          label = "Potato Variety",
          choices = c(""),
          multiple = T,
          options = list(`actions-box` = T,
                         `live-search` = T)
        ),
        helpText("The y-axis of each bar plot is Rejection Percentage (ACRE_REJ/ACRE_TOTAL)."),
        helpText("The x-axis is different potato lot name (plot on top) or potato variety (plot on bottom)."),
        helpText("For each potato lot name/potato variety, it shows two bars \
                 -- one for summer and one for winter.")
      ),
      mainPanel(
        plotlyOutput("plot_acre_lot", height = "350px"),
        plotlyOutput("plot_acre_variety", height = "350px")
      )
    )
  )

## Variety
variety_subtab <- 
  tabPanel(
    "Variety",
    sidebarLayout(
      sidebarPanel(
        h3("Data Selection"),
        pickerInput(
          inputId = "variety_ins",
          label = "Inspection",
          choices = c("Summer", "Winter"),
          multiple = T,
          selected = "Summer",
          options = list(`actions-box` = T)
        ),
        pickerInput(
          inputId = "variety_dis",
          label = "Disease",
          choices = c("MOS", "LR", "MIX", "ST", "BRR"),
          multiple = F,
          selected = c("LR")
        ),
        pickerInput(
          inputId = "variety_variety",
          label = "Variety",
          choices = c(""),
          multiple = T,
          options = list(`live-search` = T,
                         `actions-box` = T)
        ),
        sliderInput(
          inputId = "variety_year",
          label = "Year",
          min = 0,
          max = as.numeric(format(Sys.Date(), "%Y")),
          value = c(0, as.numeric(format(Sys.Date(), "%Y")))
        ),
        helpText("The x-axis is different kinds of potato variety, \
                 and the y-axis is the average percentage of potato in the selected range of \
                 year with the selected disease type.")
      ),
      mainPanel(
        plotlyOutput("plot_var", height = "700px")
      )
    )
  )

## Combination
visualization_tab <- 
  tabPanel("Visualization", conditionalPanel(
    condition = "output.noMissingValues",
    tabsetPanel(
      disease_prevalence_subtab,
      state_comparison_subtab,
      acre_rejection_subtab,
      variety_subtab
    )
  ))

