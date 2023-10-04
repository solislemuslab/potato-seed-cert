#### Missing Values in other vars ####
other_miss_summ = function(mydf){
  miss_part = mydf[!complete.cases(mydf),]
  md.pattern(miss_part, rotate.names = T)
}

other_miss_dt = function(mydf, miss_rows){
  return(mydf[miss_rows,])
}



miss2_fix = function(){
  
}