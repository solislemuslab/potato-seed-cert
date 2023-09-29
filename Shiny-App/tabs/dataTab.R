# Data Tab

#### Data Table #### 
data_table_subtab <- 
  tabPanel(
    "Data Table",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        helpText("Please choose a csv/xlsx/txt file from your device."),
        helpText("The four tabs on the right will show a summary of the database and potential errors to address prior to data analysis and visualization."), 
        helpText("Note that clicking on a given tab might take a couple of seconds to load."),
        wellPanel(
          fileInput(
            inputId = "df",
            label = "User Data (csv/xlsx/txt format)",
            accept = c(
              "text/csv",
              "text/comma-separated-values",
              "text/tab-separated-values",
              "text/plain",
              ".csv",
              ".xlsx",
              ".tsv"
            ),
            placeholder = "No file selected",
            width = "100%"
          )
        )
      ),
      mainPanel(
        fluidRow(
          dataTableOutput("subtab_data")
        )
      )
      
    )
    
  )

#### Missing Value 1 #### 
miss1_subtab <- 
  tabPanel(
    "Missing Value1",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        # helpText("Please choose a csv/xlsx/txt file from your device."),
        # helpText("The four tabs on the right will show a summary of the database and potential errors to address prior to data analysis and visualization."), 
        # helpText("Note that clicking on a given tab might take a couple of seconds to load."),
        wellPanel(
          actionButton("fill_miss1", "Fill Missing Values"),
          actionButton("undo_miss1", "Undo")
        )
      ),
      mainPanel(
        fluidRow(
          dataTableOutput("subtab_miss1_summ")
        )
      )
    ),
    dataTableOutput("subtab_miss1_dt")
  )

## Missing Value
error_struc_subtab <- 
  tabPanel(
    "Missing Value"
  )

## Inconsistency
error_analysis_subtab <- 
  tabPanel(
    "Inconsistency"
  )

## Combination
data_tab <- 
  tabPanel(
    "Data",
    tabsetPanel(
      data_table_subtab,
      miss1_subtab,
      error_struc_subtab,
      error_analysis_subtab
    )
  )