# SERVER
server <- function(input, output, session){
  myData <- reactiveValues(dt = NULL, history = list(NULL))
  # `dt` stores the newest data table, `history` stores old data tables
  # After uploading data
  observeEvent(input$df, {
    #### Read data ####
    if (is.null(input$df)) myData$dt = NULL
    if (grepl("csv", input$df$datapath)){
      mydf <- read.csv(input$df$datapath, header = T)
    }
    if (grepl("xlsx", input$df$datapath)){
      mydf <- read_xlsx(input$df$datapath)
    }
    myData$history[[length(myData$history)+1]] = mydf
    myData$dt = mydf
    
    #### Store missing rows of Summer-Winter paired vars ####
    df_check = reactive({
      myData$dt %>% select(summer_cols, winter_cols)
    })
      
    # miss_rows = which(!complete.cases(df_check))
    miss_rows <- reactive({
      get_miss_rows(df_check())
    })
    # print(miss_rows())
    
    #### Data Tab ####
    ##### Data Table #####
    output$subtab_data <- renderDataTable(
      datatable(
        myData$dt,
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

    ##### Missing Value 1 #####
    # Summary Table
    output$subtab_miss1_summ = renderDataTable(
      datatable(
        miss1_dts(myData$dt, df_check(), miss_rows())$df_error
      )
    )
    
    # Data Table with only missing rows
    output$subtab_miss1_dt = renderDataTable(
      datatable(
        miss1_dts(myData$dt, df_check(), miss_rows())$miss,
        filter = "top",
        rownames = F,
        options = list(scrollY = 500,
                       scrollX = 500,
                       deferRender = TRUE,
                       pageLength = 10,
                       autoWidth = T
        ),
        editable = T
      )
    )
    
    observeEvent(input$subtab_miss1_dt_cell_edit, {
      info <- input$subtab_miss1_dt_cell_edit
      df_check_edit = df_check()
      df_check_edit[miss_rows()[info$row], 
                    info$col+1] <- info$value # IDK why I need "+1", but it works
      myData$history[[length(myData$history)+1]] = df_check_edit[miss_rows(),] 
      myData$dt[miss_rows(),
                colnames(df_check_edit)] = df_check_edit[miss_rows(),]
      # print(df_check_edit[miss_rows(),])
    })
    
    # Fill missing value button
    observeEvent(input$fill_miss1, {
      new_dt <- miss1_fix(myData$dt, df_check(), miss_rows())
      myData$history[[length(myData$history)+1]] = new_dt 
      myData$dt <- new_dt
    })
    
    # Undo button
    observeEvent(input$undo_miss1, {
      if(length(myData$history) > 2) { 
        myData$history <- myData$history[-length(myData$history)]  
        myData$dt <- tail(myData$history, 1)[[1]] 
      }
    })
  })

  # #### Visualization Tab ####
  # # Update Choices after uploading data
  # observe({
  #   upload_df <- myData$dt
  #   
  #   ## Disease Prevalence subTab
  #   updatePickerInput(
  #     session,
  #     "dis_pre_state",
  #     choices = sort(unique(upload_df$S_STATE)),
  #     selected = "WI"
  #   )
  # 
  #   updatePickerInput(
  #     session,
  #     "dis_pre_variety",
  #     choices = unique(upload_df$VARIETY),
  #     selected = "Atlantic"
  #   )
  #   
  #   ## State Comparison subTab
  #   updatePickerInput(
  #     session,
  #     "state_comp_state",
  #     choices = sort(unique(upload_df$S_STATE)),
  #     selected = "WI"
  #   )
  #   
  #   ## Acre Rejection subTab
  #   updatePickerInput(
  #     session,
  #     "acre_lot",
  #     choices = sort(unique(upload_df$LNAME))
  #   )
  #   
  #   updatePickerInput(
  #     session,
  #     "acre_variety",
  #     choices = sort(unique(upload_df$VARIETY))
  #   )
  #   
  #   ## Variety 
  #   updatePickerInput(
  #     session,
  #     "variety_variety",
  #     choices = sort(unique(upload_df$VARIETY))
  #   )
  #   
  #   if (!is.null(upload_df)){
  #     updateSliderInput(
  #       session,
  #       "state_comp_year",
  #       min = min(upload_df$S_YR),
  #       max = max(upload_df$S_YR),
  #       step = 1,
  #       value = c(min(upload_df$S_YR), max(upload_df$S_YR))
  #     )
  #     
  #     updateSliderInput(
  #       session,
  #       "variety_year",
  #       min = min(upload_df$S_YR),
  #       max = max(upload_df$S_YR),
  #       step = 1,
  #       value = c(min(upload_df$S_YR), max(upload_df$S_YR))
  #     )
  #     
  # 
  #   }
  # })
  # 
  # # Update choices of acre rejection tab
  # observeEvent(input$acre_lot, {
  #   req(input$acre_lot)
  #   x = input$acre_lot
  #   updatePickerInput(session, "acre_variety",
  #                     choices = unique(myData() %>%
  #                                        filter(LNAME %in% x) %>% 
  #                                        select(VARIETY))
  #   )
  # })
  # 
  # # Update Disease Prevalence Content
  # output$plot_dis_pre <- renderPlotly({
  #   plot_disease_prevalence(myData(), input$dis_pre_ins, input$dis_pre_dis,
  #                           input$dis_pre_state, input$dis_pre_variety)
  # })
  # 
  # # Update State Comparison Content
  # output$plot_state_comp <- renderPlotly({
  #   plot_state_comparison(myData(), input$state_comp_ins,
  #                         input$state_comp_state, input$state_comp_year[1],
  #                         input$state_comp_year[2])
  # })
  # 
  # # Update Acre Rejection Content
  # output$plot_acre_lot <- renderPlotly({
  #   plot_acre_rejection(myData(), input$acre_lot, 
  #                       input$acre_variety)$lot
  # })
  # 
  # output$plot_acre_variety <- renderPlotly({
  #   plot_acre_rejection(myData(), input$acre_lot,
  #                       input$acre_variety)$var
  # })
  # 
  # # Update Variety Content
  # output$plot_var <- renderPlotly(
  #   plot_variety(myData(), input$variety_ins, input$variety_dis,
  #                input$variety_variety, input$variety_year[1],
  #                input$variety_year[2])
  # )

}



