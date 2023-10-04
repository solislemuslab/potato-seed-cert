#### Variables that should be paired ####
summer_cols = c("CERT_N",
                "VARIETY",
                # "S_G",
                "S_YR",
                "S_STATE",
                "LNAME")
n_vars = length(summer_cols)
winter_cols = paste0("winter_", summer_cols)

#### Return Summary Table and Data Table with only missing rows ####
# Error Table
paired_error_dt <- function(mydf){
  miss_col = get_miss_info(mydf)$miss_cols
  df_error = data.frame(
    Variable = rep(summer_cols, 2),
    Season = rep(c("Summer", "Winter"), each = n_vars),
    Missing = miss_col
  ) %>% 
    pivot_wider(names_from = Season, values_from = Missing)
  
  inconsistency = get_mm_info(mydf)$inconsis
  df_error$MisMatch = inconsistency
  
  return(df_error)
}

# Missing Table
paired_miss_dt = function(mydf, miss_rows){
  df_paired_miss = mydf[miss_rows,]
  return(df_paired_miss)
}

# Mismatch Table
paired_mm_dt = function(mydf, mm_var) {
  info = get_mm_info(mydf)
  # print(info$mm_rows[[mm_var]])
  
  first_cols = mydf[info$mm_rows[[mm_var]], c(mm_var, paste0("winter_", mm_var))]

  other_cols = mydf[info$mm_rows[[mm_var]], 
                    setdiff(names(mydf), 
                            c(mm_var, 
                              paste0("winter_", mm_var), 
                              "Index"))]
  
  result_df = cbind(mydf[info$mm_rows[[mm_var]], "Index"], first_cols, other_cols)
  
  return(result_df)
}



#### Fill missing values ####
miss1_fix = function(mydf, df_check){
  # df_check = mydf %>% select(summer_cols, winter_cols)
  df_error = paired_error_dt(df_check)

  df_error = df_error %>%
    mutate(isna = Summer + Winter,
           both = (Summer == Winter))
  # Miss only one season
  ## Q: Do we need it if we use kNN?
  for (i in 1:dim(df_error)[1]){
    if (df_error$isna[i] != 0 & !df_error$both[i]){
      miss_rows_sep = get_miss_info(df_check[,c(i+1, i+n_vars+1)])$miss_rows # To exclude Index
      # print(miss_rows_sep)
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


#### Fix mismatch values ####
# How to do this properly?
mm_fix = function(mydf, df_check){
  info_mm = get_mm_info(df_check)
  for (Col in info_mm$mm_cols){
    mydf[info_mm$mm_rows[[Col]], paste0("winter_", Col)] = mydf[info_mm$mm_rows[[Col]], Col]
  }
  return(mydf)
}




##### Missing Rows #####
get_miss_info = function(mydf){
  miss_r = which(!complete.cases(mydf) |
                   apply(
                     apply(mydf, 
                           MARGIN = c(1,2), 
                           FUN = function(x) grepl("^[ \t]+$", x)), 
                     MARGIN = 1, 
                     any) |
                   apply(
                     apply(mydf, 
                           MARGIN = c(1,2), 
                           FUN = function(x) nchar(x)==0), 
                     MARGIN = 1, 
                     any))
  
  miss_col = mydf %>% 
    mutate_all(~ ifelse(is.na(.) | 
                          nchar(as.character(.)) == 0 |
                          grepl("^[ \t]+$", as.character(.)), 1, 0)) %>% 
    colSums()
  
  return(list("miss_rows" = miss_r,
              "miss_cols" = miss_col[-1]))
}

get_mm_info = function(mydf){
  mydf = mydf[,-1] # To exclude Index
  inconsistency = c()
  mismatch_rows = list()
  for (i in 1:n_vars){
    Diff = mydf %>% select(i, i+n_vars) %>% 
      na.omit() %>% 
      mutate(diff = ifelse(.[[1]] != .[[2]], TRUE, FALSE))
    inconsistency = c(inconsistency, sum(Diff$diff))
    if(sum(Diff$diff) != 0){
      mismatch_rows[[summer_cols[i]]] = which(Diff$diff)
    } 
  }
  
  return(list("mm_rows" = mismatch_rows,
              "mm_cols" = names(mismatch_rows),
              "inconsis" = inconsistency))
}
