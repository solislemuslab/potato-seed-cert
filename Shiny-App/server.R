# SERVER
server <- function(input, output, session){
  myData <- reactive({
    inFile <- input$df
    if (is.null(inFile)) return(NULL)
    if (grepl("csv", inFile$datapath)){
      mydf <- read.csv(inFile$datapath, header = T)
    }
    if (grepl("xlsx", inFile$datapath)){
      mydf <- read_xlsx(inFile$datapath)
    }
    
    mydf
  })
  
  ##### Data Import Tab #####
  
  # Data Table subTab
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
  
  observe({
    mydf <- myData()
    
    updatePickerInput(
      session,
      "dis_pre_state",
      choices = sort(unique(mydf$S_STATE)),
      selected = "WI"
    )
    
    updatePickerInput(
      session,
      "dis_pre_variety",
      choices = unique(mydf$VARIETY),
      selected = "Atlantic"
    )
  })
  
  ## Disease Prevalence Plot
  output$plot_dis_pre <- renderPlotly({
    plot_disease_prevalence(myData(), input$dis_pre_ins, input$dis_pre_dis,
                            input$dis_pre_state, input$dis_pre_variety)
  })
  # Disease Prevalence subTab
}




