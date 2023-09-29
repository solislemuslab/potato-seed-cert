
Mismatch = function(mydf){
  inconsistency = c()
  for (i in 1:n_vars){
    Diff = df_check %>% 
      select(all_of(i), all_of(i+n_vars)) %>% 
      na.omit() %>% 
      mutate(diff = ifelse(.[[1]] != .[[2]], TRUE, FALSE))
    inconsistency = c(inconsistency, sum(Diff$diff))
  }
}