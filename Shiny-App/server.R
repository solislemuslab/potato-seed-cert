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
      options = list(scrollY = 500,
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
    upload_df <- myData()
    
    # Disease Prevalence subTab
    updatePickerInput(
      session,
      "dis_pre_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )

    updatePickerInput(
      session,
      "dis_pre_variety",
      choices = unique(upload_df$VARIETY),
      selected = "Atlantic"
    )
    
    # State Comparison subTab
    updatePickerInput(
      session,
      "state_comp_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )
    
    updatePickerInput(
      session,
      "state_comp_year",
      choices = c(sort(unique(upload_df$S_YR)), "All"),
      selected = "All"
    )
    
  })

  ## Disease Prevalence Plot
  output$plot_dis_pre <- renderPlotly({
    plot_disease_prevalence(myData(), input$dis_pre_ins, input$dis_pre_dis,
                            input$dis_pre_state, input$dis_pre_variety)
  })
  
  output$plot_state_comp <- renderPlotly({
    plot_state_comparison(myData(), input$state_comp_ins,
                          input$state_comp_state, input$state_comp_year)
  })
  
  output$dt_state_comp <- renderDataTable({
    datatable(
      generate_temp_sc(myData(), input$state_comp_ins,
                       input$state_comp_state, input$state_comp_year),
      filter = "top",
      rownames = F,
      options = list(scrollY = 150,
                     scrollX = 500,
                     deferRender = TRUE,
                     pageLength = 10,
                     autoWidth = T
      )
    )
  })
}




