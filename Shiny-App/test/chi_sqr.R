chi_square_test = 
  function(mydf, state, year_min, year_max, 
           disease, var_comp, significance){
    if (is.null(mydf)){
      error = data.frame(
        Remind = "Please upload valid data."
      )
      return(list(Table = error,
                  Result = error))
    }else if (length(state) == 0){
      error = data.frame(
        Remind = "Please select at least one state."
      )
      return(list(Table = error,
                  Result = error))
    }else{
      temp = mydf %>% 
        filter(S_STATE %in% state,
               S_YR %in% year_min:year_max)
      if (dim(temp)[1] == 0){
        error = data.frame(
          Info = "Not enough data. Please try other combinations."
        )
        return(list(Table = error,
                    Result = error))
      }else{
        significance = as.double(significance)
        temp_table = table(temp[[disease]], temp[[var_comp]]) %>% 
          as.data.frame.matrix()
        
        if (dim(temp_table)[1] >= 2){
          # print(temp_table)
          chi2_result = chisq.test(temp_table)
          chi_data = data.frame(
            "Null_Hypothesis" = "Independent",
            "Alternative_Hypothesis" = "Associated",
            "Chi-Square-score" = round(chi2_result$statistic, 4),
            "df" = chi2_result$parameter,
            "p-value" = round(chi2_result$p.value, 4),
            "Conclusion" = ifelse(chi2_result$p.value > significance,
                                  "Independent", "Associated")
          )

        }else{
          chi_data = data.frame(
            Info = "Not enough degree of freedom to do the test. Please try other combinations."
          )
        }
        temp_table = temp_table %>% 
          mutate(DIS = rownames(temp_table)) %>% 
          select(DIS, everything())
        colnames(temp_table)[1] = disease
        
        return(list(Table = temp_table,
                    Result = chi_data))
      }


    }
    
  }
