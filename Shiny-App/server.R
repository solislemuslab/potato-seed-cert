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
  
  ## Data Table subTab
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
  
  
  ## Error Summary subTab
  
  ## Error Structure subTab
  
  ## Error Analysis subTab
  
  
  ##### Visualization Tab #####
  # Update Choices
  observe({
    upload_df <- myData()
    
    ## Disease Prevalence subTab
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
    
    ## State Comparison subTab
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
    
    ## Acre Rejection subTab
    updatePickerInput(
      session,
      "acre_lot",
      choices = sort(unique(upload_df$LNAME))
    )
    
    updatePickerInput(
      session,
      "acre_variety",
      choices = sort(unique(upload_df$VARIETY))
    )
    
    ## Variety 
    updatePickerInput(
      session,
      "variety_variety",
      choices = sort(unique(upload_df$VARIETY))
    )
    
    updatePickerInput(
      session,
      "variety_year",
      choices = c(sort(unique(upload_df$S_YR)), "All"),
      selected = "All"
    )
  })

  # Update Disease Prevalence Content
  output$plot_dis_pre <- renderPlotly({
    plot_disease_prevalence(myData(), input$dis_pre_ins, input$dis_pre_dis,
                            input$dis_pre_state, input$dis_pre_variety)
  })
  
  # Update State Comparison Content
  output$plot_state_comp <- renderPlotly({
    plot_state_comparison(myData(), input$state_comp_ins,
                          input$state_comp_state, input$state_comp_year)
  })
  
  output$dt_state_comp <- renderDataTable({
    if (is.null(myData())){
      NULL
    }
    else{
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
    }
  })
  
  # Update Acre Rejection Content
  output$plot_acre_lot <- renderPlotly({
    plot_acre_rejection(myData(), input$acre_lot, 
                        input$acre_variety)$lot
  })
  
  output$plot_acre_variety <- renderPlotly({
    plot_acre_rejection(myData(), input$acre_lot,
                        input$acre_variety)$var
  })
  
  # Update Variety Content
  output$plot_var <- renderPlotly(
    plot_variety(myData(), input$variety_ins, input$variety_dis,
                 input$variety_variety, input$variety_year)
  )
}




