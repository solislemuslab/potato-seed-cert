# Prediction Tab
predict_tab <- 
  tabPanel(
    "Prediction",
    conditionalPanel(
      condition = "output.noMissingValues",
      sidebarLayout(
        sidebarPanel(
          h3("Data Selection"),
          pickerInput(
            inputId = "pred_ins",
            label = "Inspection",
            choices = c("Summer", "Winter"),
            multiple = T,
            selected = "Summer",
            options = list(`actions-box` = T)
          ),
          
          pickerInput(
            inputId = "pred_state",
            label = "State",
            choices = c("WI"),
            multiple = T,
            options = list(`actions-box` = T,
                           `live-search` = T)
          ),
          
          pickerInput(
            inputId = "pred_disease",
            label = "Disease",
            choices = c("MOS", "LR", "MIX", "ST", "BRR"),
            multiple = T,
            selected = c("LR", "ST"),
            options = list(`actions-box` = T,
                           `live-search` = T)
          ),
          
          pickerInput(
            inputId = "pred_variety",
            label = "Variety",
            choices = c("Atlantic"),
            multiple = F,
            options = list(`live-search` = T)
          ),
          helpText("The x-axis represents the predicted disease prevalence for the year \
                   following the last year in the dataset, \
                   and the y-axis lists the selected states.")
        ),
        mainPanel(
          h3("Predicted Result"),
          plotlyOutput("pred_plot", height = "700px")
        )
        
      )
    )
  )
