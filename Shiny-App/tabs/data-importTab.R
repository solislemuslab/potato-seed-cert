# Data Import

## Data Table
data_table_subtab <- 
  tabPanel(
    "Data Table",
    dataTableOutput("subtab_data"),
    # numericInput(
    #   inputId = "page",
    #   label = "Go to page",
    #   value = NA
    # )
  )

## Error Summary 
error_sum_subtab <- 
  tabPanel(
    "Errors Summary"
  )

## Error Structure
error_struc_subtab <- 
  tabPanel(
    "Errors Structure"
  )

## Error Analysis
error_analysis_subtab <- 
  tabPanel(
    "Errors Analysis"
  )

data_import_tab <- 
  tabPanel(
    "Data Import",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        helpText(h3("Instruction:")),
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
          tabsetPanel(
            data_table_subtab,
            error_sum_subtab,
            error_struc_subtab,
            error_analysis_subtab
          )
        )
      )
      
    )
  )