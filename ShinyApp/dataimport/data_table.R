#### Check Column Names ####
check_col_names <- function(mydf){
  return(which(colnames(mydf)[-1] != correct_names))
}

#### Check Column Class ####
check_col_class<-function(mydf){
  vars_chr = c("S_STATE", "VARIETY")
  vars_num = setdiff(vars_need, vars_chr)
  
  Check_chr = sapply(mydf[, vars_chr], is.character)
  Check_num = sapply(mydf[vars_num], is.numeric)
  
  Check = c(Check_chr, Check_num)
  Which_col = which(!Check)
  return(list("Check" = all(Check),
              "Which_col" = names(Which_col)))
}
