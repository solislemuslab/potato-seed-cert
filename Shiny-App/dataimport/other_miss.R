#### Missing Values in other vars ####
other_miss_summ = function(mydf){
  miss_part = mydf[!complete.cases(mydf),]
  if (dim(miss_part)[1] == 0){
    p_om = ggplot(NULL, aes(x = c(0,1), y = c(0,1))) + 
      annotate("text",x=0.5,y=0.5,label="The data set is completely observed.") + 
      labs(x = "", y = "") + 
      theme(plot.caption = element_text(size = 10))
    return(p_om)
  }else{
    md.pattern(miss_part, rotate.names = T)
  }
}

other_miss_summ_dt <- function(mydf){
  miss_col = get_miss_info(mydf)$miss_cols
  df_error = data.frame(
    Variable = names(miss_col),
    Missing = miss_col
  )
  return(df_error)
}

other_miss_dt = function(mydf, miss_rows){
  return(mydf[miss_rows,])
}


miss2_fix = function(mydf, df_check){
  imp = mice(df_check, method="pmm",m=1,maxit=1,seed=1)
  imputed_data = complete(imp)
  # imputed_data[imputed_data < 0] = 0
  imputed_data = imputed_data[-which(imputed_data < 0)] # TBD
  problem = imp$loggedEvents
  # print(problem)
  if (!is.null(problem)){
    for (i in 1:dim(problem)[1]){
      #if (problem$meth[i] == "constant"){}
      target = imputed_data[,problem$out[i]]
      mean_tar = mean(target, na.rm=T)
      target[is.na(target)] = mean_tar
      imputed_data[,problem$out[i]] = target
      
    }
  }
  
  mydf[,colnames(imputed_data)] = imputed_data
  
  var_mapping = list(
    "SR1_MOS" = c("NO_MOS_1ST", "PLTCT_1"),
    "SR2_MOS" = c("NO_MOS_2ND", "PLTCT_2"),
    "SR1_ST"  = c("NO_ST_1ST", "PLTCT_1"),
    "SR2_ST"  = c("NO_ST_2ND", "PLTCT_2"),
    "SR1_LR"  = c("NO_LR_1ST", "PLTCT_1"),
    "SR2_LR"  = c("NO_LR_2ND", "PLTCT_2"),
    "SR1_MIX" = c("NO_MIX_1ST", "PLTCT_1"),
    "SR2_MIX" = c("NO_MIX_2ND", "PLTCT_2"),
    "SR2_BRR" = c("NO_BRR_2ND", "PLTCT_2")
  )
  
  for (var in names(var_mapping)) {
    var2 <- var_mapping[[var]][1]
    var3 <- var_mapping[[var]][2]
    mydf[[var]] = mydf[[var2]] / mydf[[var3]] * 100
  }
  return(mydf)
}

