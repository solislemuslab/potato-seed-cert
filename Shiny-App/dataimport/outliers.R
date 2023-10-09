#### Outliers ####

plot_outliers = function(mydf, my_vars){
  if (length(my_vars) == 0){
    p_out = ggplot(NULL, aes(x = c(0,1), y = c(0,1))) + 
      annotate("text",x=0.5,y=0.5,label="Please select at least one variable.") + 
      labs(x = "", y = "") + 
      theme(plot.caption = element_text(size = 10))
    return(p_out)
  }else{
    mydf = mydf[complete.cases(mydf),]
    p_out = mydf %>% 
      select(my_vars) %>% 
      pivot_longer(everything(), names_to = "Variable") %>% 
      ggplot() + 
      geom_boxplot(aes(x = Variable,
                       y = value,
                       fill = Variable))
    
    ggplotly(p_out)
  }
}



outliers_dt <- function(mydf, my_vars) {
  outlier_rows = mydf %>% 
    select(my_vars) %>% 
    lapply(function(x) which(x %in% boxplot.stats(x)$out)) %>% 
    unlist() %>% 
    unique()
  
  return(list(dt = mydf[outlier_rows, c("Index", my_vars)],
              out_row = outlier_rows))
}
# 
# lapply(mydf %>% 
#          select(my_vars),
#        function(x) return(list(number = boxplot.stats(x)$out,
#                                where = which(x %in% boxplot.stats(x)$out))))
# dt_outlier = data.frame("Variable" = NA,
#                         "Possible_Outliers" = NA,
#                         "Value" = NA)
# for (i in 1:dim(mydf)[2]){
#   dt_outlier[i,] = c(colnames(mydf)[i],
#                      boxplot.stats(mydf[,i])$out,
#                      paste(which(mydf[,i] %in% boxplot.stats(mydf[,i])$out),
#                            collapse = ", "))
# }
# return(dt_outlier)

# 
# outliers_list_boxplot <- lapply(df, detect_outliers_boxplot)
# 
# for (col in names(df)) {
#   outliers <- outliers_list_boxplot[[col]]$num
#   where_out <- outliers_list_boxplot[[col]]$where
#   if (length(outliers) > 0) {
#     cat(paste("Outliers for", col, ":"))
#     cat(paste(outliers, collapse=", "))
#     cat(". \n")
#     
#     cat("At row: ")
#     cat(paste(where_out, collapse = ", "))
#     cat(". \n")
#   } else {
#     print(paste("No outliers detected for", col))
#   }
# }