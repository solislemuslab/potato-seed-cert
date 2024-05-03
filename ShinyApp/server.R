# SERVER
server <- function(input, output, session){
  myData = reactiveValues(dt = NULL, history = list(NULL))
  # `dt` stores the newest data table, `history` stores old data tables
  
  observe_helpers(withMathJax = TRUE)
  
  #### After uploading data ####
  observeEvent(input$df, {
    #### Read data and check basics ####
    if (is.null(input$df)) myData$dt = NULL
    if (grepl("csv", input$df$datapath)){
      mydf = read.csv(input$df$datapath, header = T)
    }
    if (grepl("xlsx", input$df$datapath)){
      mydf = read_xlsx(input$df$datapath)
    }
    if (length(check_col_names(mydf))!=0){ # Check Column Names
      shinyalert("Warning", 
                 paste0("The data uploaded has wrong column names: ",
                        paste(colnames(mydf)[check_col_names(mydf)+1], collapse = ", "),
                        ". Please check and upload again."), 
                 type = "info",
                 callbackR = function(x) {
                   # Refresh the page after the alert is closed
                   runjs("location.reload();")
                   })
      myData$dt = NULL
      
    }else if (!check_col_class(mydf)$Check){ # Check Important Variable Classes
      shinyalert("Warning", 
                 paste0("The data uploaded has wrong column classes: ",
                        paste(check_col_class(mydf)$Which, collapse = ", "),
                        ". They should be ", 
                        c("characters", "numbers")[if_else(check_col_class(mydf)$Which > 2, 2, 1)],
                        ". Please check and upload again."), 
                 type = "info",
                 callbackR = function(x) {
                   # Refresh the page after the alert is closed
                   runjs("location.reload();")
                 })
      # output$subtab_data = renderDataTable(
      #   mydf[,check_col_class(mydf)$Which_col]
      # )
    }
    else{
      mydf = mydf %>%
        mutate(Index = as.numeric(rownames(mydf))) %>% 
        select(Index, everything())
      myData$history[[length(myData$history)+1]] = mydf
      myData$dt = mydf
    }
    
    #### When data is proper ####
    if (!is.null(myData$dt)){
      #### Store reactive values ####
      df_check_paired = reactive({
        myData$dt %>% select(Index, summer_cols, winter_cols)
      })
      
      miss_rows_paired = reactive({
        get_miss_info(df_check_paired())$miss_rows
      })

      mm_rows = reactive({
        get_mm_info(df_check_paired())$mm_rows[[input$paired_mismatch]]
      })
      
      df_check_other = reactive({
        myData$dt %>% select(Index, vars_need)
      })
      
      miss_rows_other = reactive({
        get_miss_info(df_check_other())$miss_rows
      })
      
      #### Data Tab ####
      ##### Undo button #####
      observeEvent(input$undo, {
        if(length(myData$history) > 2) {
          myData$history = myData$history[-length(myData$history)]
          myData$dt = tail(myData$history, 1)[[1]]
        }
      })
      
      ##### Download button #####
      output$downloadData = downloadHandler(
        filename <- function() {
          paste("data-", Sys.Date(), ".csv", sep="")
        },
        content <- function(file) {
          write.csv(myData$dt[,-1], file, row.names = F)
        }
      )
      
      ##### Data Table #####
      output$subtab_data = renderDataTable(
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
      
      ##### Paired Vars #####
      ###### Summary Table ######
      output$paired_error_summ = renderDataTable(
        datatable(
          paired_error_dt(df_check_paired())
        )
      )
      
      ###### Missing Part ######
      ## Data Table with only missing rows
      output$paired_miss_dt = renderDataTable(
        datatable(
          paired_miss_dt(df_check_paired(), miss_rows_paired()),
          filter = "top",
          rownames = F,
          options = list(scrollY = 300,
                         scrollX = 500,
                         deferRender = TRUE,
                         pageLength = 10,
                         autoWidth = T
          ),
          editable = T
        )
      )
      
      ###### Mismatch Part ######
      ## Update selections
      updateSelectInput(
        session,
        "paired_mismatch",
        choices = get_mm_info(df_check_paired())$mm_cols,
        selected = get_mm_info(df_check_paired())$mm_cols[1]
      )
      
      ## Update Data Table with only mismatch rows
      # If there are mismatches
      if (length(get_mm_info(df_check_paired())$mm_cols) != 0){
        output$paired_mm_dt = renderDataTable(
          datatable(
            paired_mm_dt(df_check_paired(), input$paired_mismatch),
            filter = "top",
            rownames = F,
            options = list(scrollY = 300,
                           scrollX = 500,
                           deferRender = TRUE,
                           pageLength = 10,
                           autoWidth = T
            ),
            editable = T
          )
        )
      }else{
        output$paired_mm_dt = renderDataTable({
          empty_df = data.frame(matrix(ncol = ncol(df_check_paired()), nrow = 0))
          colnames(empty_df) = colnames(df_check_paired())
          datatable(
            empty_df,
            filter = "top",
            rownames = F,
            options = list(scrollY = 300,
                           scrollX = 500,
                           deferRender = TRUE,
                           pageLength = 10,
                           autoWidth = T
            )
          )
        })
      }

      ###### Fix Part ######
      ## Missing
      ### Edit DT function
      observeEvent(input$paired_miss_dt_cell_edit, {
        info = input$paired_miss_dt_cell_edit
        df_check_edit = df_check_paired()
        df_check_edit[miss_rows_paired()[info$row],
                      info$col+1] = info$value
        
        myData$dt[miss_rows_paired(),
                  colnames(df_check_edit)] = df_check_edit[miss_rows_paired(),]
        myData$history[[length(myData$history)+1]] = myData$dt
      })
      
      ### Fill missing value button
      observeEvent(input$fill_pair_miss, {
        # print("Click Fill")
        new_dt = miss1_fix(myData$dt, df_check_paired())
        if (!identical(new_dt, myData$dt)){
          myData$history[[length(myData$history)+1]] = new_dt
          myData$dt = new_dt
        }
      })
      
      ## MisMatch
      ### Edit DT function
      observeEvent(input$paired_mm_dt_cell_edit, {
        info_mm = input$paired_mm_dt_cell_edit
        df_mm_edit = paired_mm_dt(df_check_paired(), input$paired_mismatch)
        df_mm_edit[info_mm$row,
                      info_mm$col+1] = info_mm$value
        myData$dt[mm_rows()[info_mm$row],
                  colnames(df_mm_edit)] = df_mm_edit[info_mm$row,]
        myData$history[[length(myData$history)+1]] = myData$dt
      })
      
      ### Fix mismatch button
      observeEvent(input$fix_pair_mm, {
        new_dt = mm_fix(myData$dt, df_check_paired())
        if (!identical(new_dt, myData$dt)){
          myData$history[[length(myData$history)+1]] = new_dt
          myData$dt = new_dt
        }
      })
      
      ##### Outliers #####
      updatePickerInput(
        session,
        "outliers_var",
        choices = colnames(df_check_other())[-c(1,
                                             which(colnames(df_check_other()) %in% c("VARIETY", "S_STATE")))],
        selected = colnames(df_check_other())[-c(1,
                                                 which(colnames(df_check_other()) %in% c("VARIETY", "S_STATE")))][1]
      )
      
      
      ## Box plot
      output$outliers_plot = renderPlotly({
        plot_outliers(df_check_other()[,-1], input$outliers_var)
      })
      
      ## Data Table
      output$outliers_dt = renderDataTable(
        if(length(input$outliers_var) == 0){
          datatable(NULL)
        }else{
          datatable(
            outliers_dt(df_check_other(), input$outliers_var)$dt,
            rownames = F,
            filter = "top",
            options = list(scrollY = 300,
                           scrollX = 500,
                           deferRender = TRUE,
                           pageLength = 10,
                           autoWidth = F),
            editable = T
          ) %>% 
            formatStyle(columns = 1:ncol(outliers_dt(df_check_other(), input$outliers_var)$dt),
                        backgroundColor = styleInterval(cuts = -1e-100, 
                                                        values = c("palevioletred", "white"))
            )
        }

      )
      
      ## Edit function
      observeEvent(input$outliers_dt_cell_edit, {
        info = input$outliers_dt_cell_edit
        # print(info)
        df_check_edit = outliers_dt(df_check_other(), input$outliers_var)$dt
        df_check_edit[info$row,
                      info$col+1] = info$value # IDK why I need "+1", but it works
        
        myData$dt[outliers_dt(df_check_other(), input$outliers_var)$out_row,
                  colnames(df_check_edit)] = df_check_edit
        myData$history[[length(myData$history)+1]] = myData$dt
      })
      
      ##### Other missing #####
      ## Summary
      output$other_miss_summ_dt = renderDataTable(
        datatable(
          other_miss_summ_dt(df_check_other()),
          rownames = F,
          filter = "top",
          options = list(pageLength = 5)
        )
        
      )
      
      output$other_miss_summ = renderPlot(
        other_miss_summ(df_check_other())
      )
      ## Data table
      output$other_miss_dt = renderDataTable(
        datatable(
          other_miss_dt(df_check_other(), miss_rows_other()),
          filter = "top",
          rownames = F,
          options = list(scrollY = 300,
                         scrollX = 500,
                         deferRender = TRUE,
                         pageLength = 10,
                         autoWidth = T
          ),
          editable = T
        ) %>% 
          formatStyle(columns = which(get_miss_info(df_check_other())$miss_cols != 0) + 1,
                      backgroundColor = "palevioletred",
                      color = "black")
      )
      
      ## Edit function
      observeEvent(input$other_miss_dt_cell_edit, {
        info = input$other_miss_dt_cell_edit
        # print(info)
        df_check_edit = df_check_other()
        df_check_edit[miss_rows_other()[info$row],
                      info$col+1] = info$value # IDK why I need "+1", but it works
        
        myData$dt[miss_rows_other(),
                  colnames(df_check_edit)] = df_check_edit[miss_rows_other(),]
        myData$history[[length(myData$history)+1]] = myData$dt
      })
      
      ## Fill button
      observeEvent(input$fill_other_miss, {
        new_dt = miss2_fix(myData$dt, df_check_other())
        if (!identical(new_dt, myData$dt)){
          myData$history[[length(myData$history)+1]] = new_dt
          myData$dt = new_dt
        }
      })
      

    }
  })
  
  #### Check Data ####
  # Check for missing values
  df_check_other = reactive({
    if (is.null(myData$dt)){
      NULL
    } else{
      myData$dt %>% select(Index, vars_need)
    }
  })

  noError <- reactive({
    if (is.null(myData$dt)){
      FALSE
    } else{
      check_col_class(myData$dt)$Check & 
        all(complete.cases(df_check_other()))
    }
  })
  
  # Observe clicking on the Analysis tab
  observeEvent(input$mainTab, {
    if ((input$mainTab == "Visualization" |
        input$mainTab == "Test" |
        input$mainTab == "Prediction") && !noError()) {
      shinyalert(title = "Warning", 
                 text = "The data is not uploaded or still have missing values, which will affect the content in this tab. \
                 Please upload data or go through the Data Tab first.", 
                 type = "info")
    }
  })
  
  #### Visualization Tab ####
  output$noMissingValues <- reactive({
    if (is.null(myData$dt)){
      FALSE
    } else{
      check_col_class(myData$dt)$Check & 
        all(complete.cases(df_check_other()))
    }
  })
  outputOptions(output, 'noMissingValues', suspendWhenHidden = FALSE)

  observe({
    upload_df = myData$dt
    # Update Choices after uploading data
    ## Disease Prevalence subTab
    updatePickerInput(
      session,
      "dis_pre_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )
    
    observeEvent(input$dis_pre_state, {
      req(input$dis_pre_state)
      x = input$dis_pre_state
      updatePickerInput(
        session,
        "dis_pre_variety",
        choices = unique(upload_df$VARIETY[upload_df$S_STATE == x]),
        selected = unique(upload_df$VARIETY[upload_df$S_STATE == x])[1]
      )
    })
    
    ## State Comparison subTab
    updatePickerInput(
      session,
      "state_comp_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )
    
    # Update disease choices
    observeEvent(input$state_comp_ins, {
      req(input$state_comp_ins)
      x = input$state_comp_ins
      if (x == "Winter"){
        updatePickerInput(
          session,
          "state_comp_dis",
          choices = c("MOS", "LR", "MXD")
        )
      }else if (x == "Summer_2nd"){
        updatePickerInput(
          session,
          "state_comp_dis",
          choices =  gsub("^NO_|_2ND$", "", 
                          colnames(upload_df)[grepl("^NO.*_2ND$", colnames(upload_df))])
        )
      }else{
        updatePickerInput(
          session,
          "state_comp_dis",
          choices =  gsub("^NO_|_1ST$", "", 
                          colnames(upload_df)[grepl("^NO.*_1ST$", colnames(upload_df))])
        )
      }
    })      
    
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
    
    if (!is.null(upload_df)){
      updateSliderInput(
        session,
        "state_comp_year",
        min = min(upload_df$S_YR),
        max = max(upload_df$S_YR),
        step = 1,
        value = c(min(upload_df$S_YR), max(upload_df$S_YR))
      )
      
      updateSliderInput(
        session,
        "variety_year",
        min = min(upload_df$S_YR),
        max = max(upload_df$S_YR),
        step = 1,
        value = c(min(upload_df$S_YR), max(upload_df$S_YR))
      )
      
      
    }
    
    # Update choices of acre rejection tab
    observeEvent(input$acre_lot, {
      req(input$acre_lot)
      x = input$acre_lot
      updatePickerInput(session, "acre_variety",
                        choices = unique(myData$dt %>%
                                           filter(LNAME %in% x) %>%
                                           select(VARIETY))
      )
    })
    
    # Update Disease Prevalence Content
    output$plot_dis_pre = renderPlotly({
      plot_disease_prevalence(myData$dt, input$dis_pre_ins, input$dis_pre_dis,
                              input$dis_pre_state, input$dis_pre_variety)
    })
    
    # Update State Comparison Content
    output$plot_state_comp = renderPlotly({
      plot_state_comparison(myData$dt, input$state_comp_ins,
                            input$state_comp_state, input$state_comp_year[1],
                            input$state_comp_year[2])
    })
    
    output$map_plot_state_comp = renderPlotly({
      map_plot_sc(myData$dt, input$state_comp_ins,
                  input$state_comp_state, input$state_comp_year[1],
                  input$state_comp_year[2],
                  input$state_comp_dis)
    })
    # Update Acre Rejection Content
    output$plot_acre_lot = renderPlotly({
      plot_acre_rejection(myData$dt, input$acre_lot,
                          input$acre_variety)$lot
    })
    
    output$plot_acre_variety = renderPlotly({
      plot_acre_rejection(myData$dt, input$acre_lot,
                          input$acre_variety)$var
    })
    
    # Update Variety Content
    output$plot_var = renderPlotly(
      plot_variety(myData$dt, input$variety_ins, input$variety_dis,
                   input$variety_variety, input$variety_year[1],
                   input$variety_year[2])
    )
  })
  
  #### Test Tab ####
  observe({
    upload_df = myData$dt
    # Update Choices
    updatePickerInput(
      session,
      "test_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )
    
    if (!is.null(upload_df)){
      updateSliderInput(
        session,
        "test_year",
        min = min(upload_df$S_YR),
        max = max(upload_df$S_YR),
        step = 1,
        value = c(min(upload_df$S_YR), max(upload_df$S_YR))
      )
    }
    
    observeEvent(input$test_subtabs, {
      if (input$test_subtabs == "anova"){
        updatePickerInput(
          session,
          "test_disease",
          choices = c("SR1_MOS", "SR2_MOS", 
                      "SR1_ST", "SR2_ST",
                      "SR1_LR", "SR2_LR",
                      "SR1_MIX", "SR2_MIX",
                      "SR2_BRR")
        )
      }
    })
    
    # Update Chi-Square subtab
    output$observe_dt = renderDataTable(
      datatable(
        chi_square_test(upload_df, input$test_state,
                        input$test_year[1], input$test_year[2],
                        input$test_disease,
                        input$test_var,
                        input$test_alpha)$Table,
        rownames = F,
        options = list(scrollX = 500,
                       deferRender = TRUE,
                       pageLength = 10
        )
      )
    )
    
    output$chi2_dt = renderDataTable(
      datatable(
        chi_square_test(upload_df, input$test_state,
                        input$test_year[1], input$test_year[2],
                        input$test_disease,
                        input$test_var,
                        input$test_alpha)$Result,
        rownames = F,
        options = list(searching = FALSE, 
                       paging = FALSE
        )
      ) %>% 
        formatStyle(columns = 6,
                    backgroundColor = "royalblue",
                    color = "white")
    )
    
    # Update ANOVA subtab
    output$anova_dt = renderDataTable(
      datatable(
        anova_test(upload_df, input$test_state,
                   input$test_year[1], input$test_year[2],
                   input$test_disease,
                   input$test_var,
                   input$test_alpha)$Table,
        rownames = F,
        options = list(scrollX = 500,
                       # scrollY = 300,
                       deferRender = TRUE,
                       pageLength = 5
        )
      )
    )
    
    output$anova_res_dt = renderDataTable(
      datatable(
        anova_test(upload_df, input$test_state,
                   input$test_year[1], input$test_year[2],
                   input$test_disease,
                   input$test_var,
                   input$test_alpha)$Result,
        rownames = F,
        options = list(searching = FALSE, 
                       paging = FALSE
        )
      ) %>% 
        formatStyle(columns = 6,
                    backgroundColor = "royalblue",
                    color = "white")
    )
  })
  
  #### Prediction Tab ####
  observe({
    upload_df = myData$dt
    # Update Choices after uploading data
    updatePickerInput(
      session,
      "pred_state",
      choices = sort(unique(upload_df$S_STATE)),
      selected = "WI"
    )
    
    updatePickerInput(
      session,
      "pred_variety",
      choices = unique(upload_df$VARIETY),
      selected = "Atlantic"
    )
    
    # Update Content
    output$pred_plot = renderPlotly({
      predict_prevalance(upload_df, input$pred_state,
                         input$pred_disease,
                         input$pred_variety,
                         input$pred_ins)
    })
  })
}
