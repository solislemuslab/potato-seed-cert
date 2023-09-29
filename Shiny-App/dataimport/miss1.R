#### Variables that should be paired ####
summer_cols = c("CERT_N",
                "SNAME",
                "GCODE",
                "VARIETY",
                # "S_G",
                "S_YR",
                "S_STATE")
n_vars = length(summer_cols)
winter_cols = paste0("winter_", summer_cols)

#### Return Summary Table and Data Table with only missing rows ####
miss1_dts <- function(mydf){
  df_check = mydf %>% select(summer_cols, winter_cols)
  # miss_rows = which(!complete.cases(df_check))
  miss_col = df_check %>% 
    is.na() %>% 
    colSums()
  
  df_error = data.frame(
    Variable = rep(summer_cols, 2),
    Season = rep(c("Summer", "Winter"), each = n_vars),
    Missing = miss_col
  ) %>% 
    pivot_wider(names_from = Season, values_from = Missing)
  
  df_check_miss = df_check[miss_rows,]
  return(list("df_error" = df_error,
              "miss" = df_check_miss))
}

#### Fill missing values ####
miss1_fix = function(mydf){
  # df_check = mydf %>% select(summer_cols, winter_cols)
  df_error = miss1_dts(mydf)$df_error
  df_error = df_error %>% 
    mutate(isna = Summer + Winter,
           both = Summer * Winter)
  
  for (i in 1:dim(df_error)[1]){
    if (df_error$isna[i] != 0 & df_error$both[i] == 0){
      miss_rows = which(!complete.cases(df_check[,c(i, i+n_vars)]))
      if (df_error$Summer[i] != 0){
        mydf[miss_rows, summer_cols[i]] = mydf[miss_rows, winter_cols[i]]
      }
      else{
        mydf[miss_rows, winter_cols[i]] = mydf[miss_rows, summer_cols[i]]
      }
    }
    # else{
    #   miss_rows = which(!complete.cases(df_check[,c(i, i+n_vars)]))
    #   response_var <- summer_cols[i]
    #   predictor_vars <- summer_cols[-i]
    #   
    #   formula_str <- paste(response_var, "~", 
    #                        paste(predictor_vars, collapse = " + "))
    #   formula_obj <- as.formula(formula_str)
    #   
    #   fit <- lm(formula_obj, data = df_check[complete.cases(df_check),])
    #   
    #   pred = predict(fit, newdata=df_check[miss_rows,i])
    #   mydf[,summer_cols[i]] = as.vector(pred)
    #   mydf[,winter_cols[i]] = as.vector(pred)
    # }
  }
  
  return(mydf)
}



