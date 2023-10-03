#### Variables that should be paired ####
summer_cols = c("CERT_N",
                "SNAME",
                "GCODE",
                "VARIETY",
                "S_G",
                "S_YR",
                "S_STATE",
                "LNAME")
n_vars = length(summer_cols)
winter_cols = paste0("winter_", summer_cols)

#### Return Summary Table and Data Table with only missing rows ####
miss1_dts <- function(mydf, df_check, miss_rows){
  # df_check = mydf %>% select(summer_cols, winter_cols)
  # miss_rows = which(!complete.cases(df_check))
  # miss_col = df_check %>% 
  #   (is.na() | nchar()==0) %>% 
  #   colSums()
  miss_col = df_check %>% 
    mutate_all(~ ifelse(is.na(.) | 
                        nchar(as.character(.)) == 0 |
                        grepl("^[ \t]+$", as.character(.)), 1, 0)) %>% 
    colSums()
  
  df_error = data.frame(
    Variable = rep(summer_cols, 2),
    Season = rep(c("Summer", "Winter"), each = n_vars),
    Missing = miss_col
  ) %>% 
    pivot_wider(names_from = Season, values_from = Missing)
  
  df_check_miss = df_check[miss_rows,]
  # print(miss_rows)
  return(list("df_error" = df_error,
              "miss" = df_check_miss))
}

#### Fill missing values ####
miss1_fix = function(mydf, df_check, miss_rows){
  # df_check = mydf %>% select(summer_cols, winter_cols)
  df_error = miss1_dts(mydf, df_check, miss_rows)$df_error
  df_error = df_error %>% 
    mutate(isna = Summer + Winter,
           both = (Summer == Winter))
  # Miss only one season
  ## Q: Do we need it if we use kNN?
  for (i in 1:dim(df_error)[1]){
    if (df_error$isna[i] != 0 & !df_error$both[i]){
      miss_rows_sep = get_miss_rows(df_check[,c(i, i+n_vars)])
        # which(!complete.cases(df_check[,c(i, i+n_vars)]))
      # print(mydf[miss_rows_sep, winter_cols[i]])
      if (df_error$Summer[i] > df_error$Winter[i]){
        mydf[miss_rows_sep, summer_cols[i]] = mydf[miss_rows_sep, winter_cols[i]]
      }
      else{
        mydf[miss_rows_sep, winter_cols[i]] = mydf[miss_rows_sep, summer_cols[i]]
      }
    }
  }
  # Miss both seasons
  ## Categorical Variables: annoying
  # miss_rows = which(!complete.cases(df_check))
  # num_vars = setdiff(colnames(df_check), c("S_STATE", "VARIETY", "S_G",
  #                                          "winter_S_STATE", "winter_VARIETY", "winter_S_G"))
  # df_KNN = knnImputation(df_check[,num_vars], 
  #                        k=10, meth="weighAvg")
  # mydf[miss_rows, colnames(df_KNN)] = df_KNN[miss_rows,]
  
  return(mydf)
}



