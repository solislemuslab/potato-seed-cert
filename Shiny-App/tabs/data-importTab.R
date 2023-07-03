# Data Import
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
            tabPanel(
              "Data Table",
              dataTableOutput("subtab_data")
            ),
            
            tabPanel(
              "Errors Summary"
            ),
            
            tabPanel(
              "Errors Structure"
            ),
            
            tabPanel(
              "Errors Analysis"
            )
          )
        )
      )
      
    )
  )