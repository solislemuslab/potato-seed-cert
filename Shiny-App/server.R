# SERVER

server <- function(input, output, session){
  ##### Data Import Tab #####
  
  # Data Table subTab
  myData <- reactive({
    inFile <- input$df
    if (is.null(inFile)) return(NULL)
    if (grepl("csv", inFile$datapath)){
      df <- read.csv(inFile$datapath, header = T)
    }
    if (grepl("xlsx", inFile$datapath)){
      df <- read_xlsx(inFile$datapath)
    }
    # df <- read.csv(inFile$datapath, header = TRUE)
    df
  })
  
  output$subtab_data <- renderDataTable(
    datatable(
      myData(),
      filter = "top",
      rownames = F,
      options = list(scrollY = 600,
                     scrollX = 500,
                     deferRender = TRUE,
                     pageLength = 10,
                     autoWidth = T
      )
    )
  )
  
  
  # Error Summary subTab
  
  # Error Structure subTab
  
  # Error Analysis subTab
  
  
  ##### Visualization Tab #####
  
}