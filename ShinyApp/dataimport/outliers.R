#### Outliers ####
# Boxplot
plot_outliers <- function(mydf, my_vars){
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

# Detailed Data Table
outliers_dt <- function(mydf, my_vars) {
  outlier_rows = mydf %>% 
    select(my_vars) %>% 
    lapply(function(x) which(x %in% boxplot.stats(x)$out)) %>% 
    unlist() %>% 
    unique()
  negative_df_rows = mydf %>% 
    select(my_vars) %>% 
    mutate(neg = if_any(everything(), ~ . < 0))
  negative_rows = which(negative_df_rows$neg)
  outlier_rows = c(outlier_rows, negative_rows) %>% 
    unique()
  return(list(dt = mydf[outlier_rows, c("Index", my_vars)],
              out_row = outlier_rows))
}
