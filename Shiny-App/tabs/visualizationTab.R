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
        )
      ),
      mainPanel(
        plotlyOutput("plot_dis_pre")
      )
    )
  )

# State comparison
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
          options = list(`action-box` = T,
                         `live-search` = T)
        ),
        pickerInput(
          inputId = "state_comp_ins",
          label = "Inspection",
          choices = c("1st", "2nd"),
          multiple = F
        ),
        pickerInput(
          inputId = "state_comp_year",
          label = "Year",
          choices = c(2000:2016, "All"),
          multiple = F,
          options = list(`action-box` = T,
                         `live-search` = T)
        )
      ),
      mainPanel(
        plotlyOutput("plot_state_comp"),
        dataTableOutput("dt_state_comp")
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
          options = list(`action-box` = T,
                         `live-search` = T)
        ),
        pickerInput(
          inputId = "acre_variety",
          label = "Potato Variety",
          choices = c(""),
          multiple = T,
          options = list(`action-box` = T,
                         `live-search` = T)
        )
      ),
      mainPanel(
        plotlyOutput("plot_acre_lot"),
        plotlyOutput("plot_acre_variety")
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
          inputId = "variety_vatiety",
          label = "Variety",
          choices = c(""),
          multiple = T,
          options = list(`live-search` = T,
                         `action-box` = T)
        ),
        pickerInput(
          inputId = "variety_year",
          label = "Year",
          choices = c(2000:2016, "All"),
          multiple = F,
          options = list(`live-search` = T)
        )
      ),
      mainPanel(
        plotlyOutput("plot_variety")
      )
    )
  )

## Aggregation
visualization_tab <- 
  tabPanel(
    "Visualization",
    tabsetPanel(
      disease_prevalence_subtab,
      state_comparison_subtab,
      acre_rejection_subtab,
      variety_subtab
    )
  )


