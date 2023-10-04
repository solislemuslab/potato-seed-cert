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

#### Errors in Paired Vars #### 
paired_subtab <- 
  tabPanel(
    "Paired Errors",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        # helpText("Please choose a csv/xlsx/txt file from your device."),
        # helpText("The four tabs on the right will show a summary of the database and potential errors to address prior to data analysis and visualization."), 
        # helpText("Note that clicking on a given tab might take a couple of seconds to load."),

        actionButton("fill_pair_miss", "Fill Missing Values"),
        actionButton("fix_pair_mm", "Fix Mismatches"),
        
        selectInput("paired_mismatch", "Select Mismatch Variable",
                    choices = c()),
        
      ),
      mainPanel(
        fluidRow(
          "Paired Error Summary",
          dataTableOutput("paired_error_summ")
        )
      )
    ),
    column(6,
           "Paired Missing Values",
           dataTableOutput("paired_miss_dt")),
    column(6,
           "Paired Mismatch",
           dataTableOutput("paired_mm_dt"))
  )

## Outliers
outliers_subtab <- 
  tabPanel(
    "Outliers",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        # helpText("Please choose a csv/xlsx/txt file from your device."),
        # helpText("The four tabs on the right will show a summary of the database and potential errors to address prior to data analysis and visualization."), 
        # helpText("Note that clicking on a given tab might take a couple of seconds to load."),
        
        selectInput("outliers_var", "Select Variable",
                    choices = c()),
      ),
      mainPanel(
        fluidRow(
          "Outliers Plot",
          plotlyOutput("outliers_plot")
        )
      )
    )
  )

## Missing Value in other Vars
error_analysis_subtab <- 
  tabPanel(
    "Missing Values",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        # helpText("Please choose a csv/xlsx/txt file from your device."),
        # helpText("The four tabs on the right will show a summary of the database and potential errors to address prior to data analysis and visualization."), 
        # helpText("Note that clicking on a given tab might take a couple of seconds to load."),

      ),
      mainPanel(
        fluidRow(
          "Missing Summary",
          plotOutput("other_miss_summ")
        )
      )
    ),
    "Missing Data Table",
    dataTableOutput("other_miss_dt")
  )

## Combination
data_tab <-
  tabPanel(
    "Data",
    downloadButton("downloadData", "Download CSV"),
    actionButton("undo", "Undo"),
    tabsetPanel(
      data_table_subtab,
      paired_subtab,
      outliers_subtab,
      error_analysis_subtab
    ),
  )

