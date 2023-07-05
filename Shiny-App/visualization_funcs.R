##### Disease Prevalence #####

plot_disease_prevalence <- 
  function(mydf, inspections, diseases, state, variety){
    if(is.null(mydf)){
      p_dp <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      ggplotly(p_dp)
    }
    else{
      dis_lab = ""
      for (disease in diseases){
        dis_lab = paste0(dis_lab, disease, ", ")
      }
      dis_lab = str_sub(dis_lab, 1, -3)
      
      if ("Summer" %in% inspections){
        mydf[is.na(mydf)] <- 0 # TBD
        temp <- mydf %>% 
          filter(S_STATE == state,
                 VARIETY == variety) %>% 
          select(c("CY", "PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", 
                   "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND")) %>% 
          group_by(CY) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_2)) %>% 
          pivot_longer(-c(CY, PLTCT_2), names_to = "Disease")
        
        temp$Disease <- gsub("^NO_", "PCT_", temp$Disease)
        
        disease_types = c()
        for (disease in diseases){
          disease_types =  c(disease_types, 
                             temp$Disease[which(grepl(disease, unique(temp$Disease)))])
        }
        
        p_dp = temp %>% 
          filter(Disease %in% disease_types) %>% 
          ggplot(aes(x = CY, y = value, col = Disease)) + 
          geom_line() + 
          geom_point(shape = 1) +
          labs(x = "Year", 
               y = paste0("Percentage of potato with ", dis_lab))
        ggplotly(p_dp)
      }
    }

  }
# 
# mutate(across(starts_with('n_'), .names = 'res_{col}') * 
#          pick(starts_with('score_')) * pick(starts_with('loc_')))
# 
# # dff[is.na(dff)] = 0
# tt = dff %>% 
#   filter(S_STATE == "WI",
#          VARIETY == "Atlantic") %>% 
#   select(c("CY", "PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", 
#            "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND")) %>% 
#   group_by(CY) %>% 
#   summarise_all(sum) %>% 
#   mutate(across(matches("NO"), function(x) x/PLTCT_2)) %>% 
#   pivot_longer(-c(CY, PLTCT_2), names_to = "Disease")
# 
# tt$Disease <- gsub("^NO_", "PCT_", tt$Disease)
# dt = c()
# for (disease in c("LR", "ST")){
#   dt = c(dt, tt$Disease[which(grepl(disease, unique(tt$Disease)))])
# }
