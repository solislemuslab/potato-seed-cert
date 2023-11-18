# Data Tab
#### Data Table #### 
data_table_subtab <- 
  tabPanel(
    "Data Table",
    sidebarLayout(
      sidebarPanel(
        width = 4,
        h3("Instructions:"),
        helpText("Please choose a csv/xlsx file from your device."),
        helpText("After data is loaded, four tabs will appear on the right with a summary of the database \
                 and potential errors to address prior to data analysis and visualization."), 
        helpText("Note that clicking on a given tab might take a couple of seconds to load."),
        helpText("Moreover, after making changes to the data, the revised data can be downloaded by clicking ", 
                 tags$b("Download CSV"), 
                 " button on the top. And by clicking the ", 
                 tags$b("Undo"), 
                 " button, the most recent change made on the data set within the dashboard will be cancelled."),
        helpText("The dashboard needs to be refreshed every time a data set is uploaded."),
        helpText("It is recommended to upload a ", 
                 tags$b(tags$em("high quality")), 
                 " data set, which means that there is little missing and wrong values. \
                 Also, please go through all the subtabs under Data Tab before moving forward."),
        wellPanel(
          fileInput(
            inputId = "df",
            label = "User Data (csv/xlsx/txt format)",
            accept = c(
              ".csv",
              ".xlsx"
              # ".tsv"
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
        helpText("By clicking ", tags$b("Fill Missing Values"), " button, the missing values will be imputed automatically.") %>% 
          helper(type = "inline",
                 title = "Further Illustration",
                 content = c("If the corresponding value in the other season is not missing, \
                             the missing value is imputed with that value.",
                             "",
                             "Or if there are paired missing continuous values, \
                             it will be solved in `Missing Values` Tab. \
                             For the paried missing discrete values, they will be deleted. \
                             Thus, make sure the data quality is high enough.",
                             "",
                             "Moreover, the button can be pressed multiple times."),
                 buttonLabel = "Got it!",
                 fade = TRUE,
                 size = "m",
                 colour = "royalblue"),
        helpText("By clicking ", tags$b("Fix Mismatches"), " button, the mismatch error in each variable will be fixed.") %>% 
          helper(type = "inline",
                 title = "Further Illustration",
                 content = c("For this button, it will change the mismatched values \
                             in winter variables (columns) into those is summer variables (columns).",
                             "",
                             "So, please make sure the values in summer variables (columns) are correct if you are using this button."),
                 buttonLabel = "Got it!",
                 fade = TRUE,
                 size = "m",
                 colour = "royalblue"),
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
        helpText("This tab will detect missing values within the important variables.\
                 Note that it is recommened to first go through the ", tags$code("Paired Errors"), "tab \
                 and ", tags$code("Outliers"), " tab before this one."),
        helpText("Detailed information about missing values is displayed on the right, both in data table and plot.") %>% 
          helper(type = "inline",
                 title = "Further Illustration",
                 content = c("The blue box indicates that the value for the variable \
                             (column) is present (i.e., not missing) for the given pattern (row).",
                             "",
                             "While the red box indicates that the value for the variable \
                             (column) is missing for the given pattern (row).",
                             "",
                             "The numbers in the rightmost column show how many variables \
                             (column) have missing values for each pattern (row).",
                             "",
                             "The numbers in the bottom represent the total count of missing \
                             values for each variable (column).",
                             "",
                             "And the numbers on the left represent how many missing values are there \
                             for each pattern (row)."),
                 buttonLabel = "Got it!",
                 fade = TRUE,
                 size = "m",
                 colour = "royalblue"),
        helpText("In the data table below, columns with red background have missing values."),
        helpText("By clicking ", tags$b("Fill Missing Values"), " button, all the missing values will be imputed automatically.") %>% 
          helper(type = "inline",
                 title = "Further Illustration",
                 content = c("By clicking the button, the missing values are \
                             imputed with the corresponding means."),
                 buttonLabel = "Got it!",
                 fade = TRUE,
                 size = "m",
                 colour = "royalblue"),
        helpText("By double clicking the elements of the data table, changes can be made. Still, change with cautious."),
        actionButton("fill_other_miss", "Fill Missing Values")
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
