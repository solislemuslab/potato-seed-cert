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
        helpText("Moreover, after making changes to the data, it can be downloaded by clicking `Download csv` button on the top."),
        helpText("And by clicking the `Undo` button, the most recent change made on the data set within the dashboard will be cancelled."),
        helpText("The dashboard needs to be refreshed every time a data set is uploaded."),
        helpText("It is recommended to go through all the subtabs under Data Tab before moving forward."),
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
          h3("Latest Data"),
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
        helpText("This tab will give error summary for the variables that are supposed to be the same in Summer and Winter."),
        helpText("By clicking `Fill Missing Values` button, the missing values will be imputed automatically."),
        helpText("By clicking `Fix Mismatches` button, the mismatch error in each variable will be fixed."),
        helpText("By double clicking elements in data tables below, changes can be done. Make sure to change with cautious."),
        selectInput("paired_mismatch", "Select Mismatch Variable",
                    choices = c()),
        actionButton("fill_pair_miss", "Fill Missing Values"),
        actionButton("fix_pair_mm", "Fix Mismatches"),
      ),
      mainPanel(
        fluidRow(
          h3("Paired Error Summary"),
          dataTableOutput("paired_error_summ")
        )
      )
    ),
    column(6,
           h4("Paired Missing Values"),
           dataTableOutput("paired_miss_dt")),
    column(6,
           h4("Paired Mismatch"),
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
        helpText("This tab will give information about possible outliers in some important variables."),
        helpText("After selecting variables in the below box, the boxplot and data table will be updated.\
                 Note that all elements in these variables should not be negative. Elements with red background are \
                 those that are negative. Please double check that and make proper changes."),
        helpText("By double clicking the elements of the data table, changes can be made. Still, change with cautious."),

        pickerInput("outliers_var", "Select Variable",
                    choices = c(),
                    multiple = T,
                    options = list(
                      `actions-box` = T,
                      `live-search` = T
                    )),
      ),
      mainPanel(
        fluidRow(
          h3("Outliers Box-Plot"),
          plotlyOutput("outliers_plot"),
          # dataTableOutput("outliers_summ")
        )
      )
    ),
    h3("Detailed Data Table"),
    dataTableOutput("outliers_dt")
  )

## Missing Value in other Vars
error_analysis_subtab <- 
  tabPanel(
    "Missing Values",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instruction:"),
        helpText("This tab will detect missing values within the important variables. Note that it is recommened to first go through the `Paired Errors` tab before this one."),
        helpText("Detailed information about missing values is displayed on the right, both in data table and plot."),
        helpText("In the data table below, columns with red background have missing values."),
        helpText("By clicking `Fill Missing Values` button, all the missing values will be imputed automatically."),
        helpText("By double clicking the elements of the data table, changes can be made. Still, change with cautious."),
        actionButton("fill_other_miss", "Fill Missing Values"),
      ),
      mainPanel(
        fluidRow(
          column(4,
                 h3("Missing Summary"),
                 dataTableOutput("other_miss_summ_dt")),
          column(8,
                 plotOutput("other_miss_summ"))
        )
      )
    ),
    h3("Missing Data Table"),
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

