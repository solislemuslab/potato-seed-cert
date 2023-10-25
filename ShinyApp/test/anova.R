anova_test = 
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
      significance = as.double(significance)
      temp = mydf %>% 
        filter(S_STATE %in% state,
               S_YR %in% year_min:year_max) %>% 
        select(Index, disease, var_comp, S_STATE, S_YR)
      
      if (dim(temp)[1] == 0){
        error = data.frame(
          Info = "Not enough data. Please try other combinations."
        )
        return(list(Table = error,
                    Result = error))
      }else{
        dof1 = length(unique(temp[[disease]]))
        dof2 = length(unique(temp[[var_comp]]))
        # print(dof1)
        # if (dof1 == 2){print(unique(temp[[disease]]))}
        # print(dof2)
        # print("")
        if (dof1 < 2 | dof2 < 2){
          anova_result = data.frame(
            Info = "Not enough degree of freedom to do the test. Please try other combinations."
          )
        }else{
          aov_model = aov(as.formula(paste0(disease, " ~ ", var_comp)), temp)
          aov_summ = summary(aov_model)[[1]]
          anova_result = data.frame(
            Null_Hypothesis = "Independent",
            Alternative_Hypothesis = "Associated",
            F_value = round(aov_summ$`F value`[1], 4),
            df = aov_summ$Df[1],
            p_value = round(aov_summ$`Pr(>F)`[1], 4),
            Conclusion = ifelse(round(aov_summ$`Pr(>F)`[1], 4) > significance,
                                "Independent", "Associated")
          )
        }
        return(list(Table = temp,
                    Result = anova_result))
      }
    }
  }




