##### Disease Prevalence #####
plot_disease_prevalence <- 
  function(mydf, inspections, diseases, state, variety){
    # If data is not valid
    if(is.null(mydf)){
      p_dp = ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      ggplotly(p_dp)
    }
    else{
      p_dp = ggplot()
      
      # Store disease name
      dis_lab = ""
      for (disease in diseases){
        dis_lab = paste0(dis_lab, disease, ", ")
      }
      dis_lab = str_sub(dis_lab, 1, -3)
      
      # Summer
      if ("Summer" %in% inspections){
        temp_1 = mydf %>% 
          filter(S_STATE == state,
                 VARIETY == variety) %>% 
          select(c("S_YR", "PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", 
                   "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND")) %>% 
          group_by(S_YR) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_2))
        
        colnames(temp_1)[-1:-2] = paste0("PCT_", gsub("^NO_|2ND", "", colnames(temp_1)[-1:-2]), "Summer")
        
        disease_types = c()
        for (disease in diseases){
          disease_types =  c(disease_types, 
                             colnames(temp_1)[which(grepl(disease, colnames(temp_1)))])
        }
        
        temp_1 = temp_1  %>% 
          pivot_longer(-c(S_YR, PLTCT_2), names_to = "Disease")%>% 
          filter(Disease %in% disease_types)
        
        if (dim(temp_1)[1] == 0){
          p_dp = p_dp +
            labs(x = "Year", 
                 y = paste0("Percentage of potato with ", dis_lab)) +
            ggtitle("Disease Prevalenve")
        }else{
          p_dp = p_dp +
            geom_line(data = temp_1, 
                      aes(x = S_YR, y = value, col = Disease)) + 
            geom_point(data = temp_1,
                       aes(x = S_YR, y = value, col = Disease),
                       shape = 19) +
            labs(x = "Year", 
                 y = paste0("Percentage of potato with ", dis_lab)) +
            ggtitle("Disease Prevalenve")
        }
      }
      
      # Winter
      if ("Winter" %in% inspections){
        temp_2 = mydf %>%
          filter(S_STATE == state,
                 VARIETY == variety) %>%
          select(c("S_YR", "winter_PLANTCT", "winter_MOSN",
                   "winter_LRN", "winter_MXDN")) %>%
          group_by(S_YR) %>%
          summarize_all(sum) %>%
          mutate(across(matches("N$"), function(x) x/winter_PLANTCT))
        
        colnames(temp_2)[5] = "winter_MIXN"
        colnames(temp_2)[-1:-2] = paste0("PCT_", gsub("^winter_|N$", "", colnames(temp_2)[-1:-2]), "_Winter")
        
        disease_types = c()
        for (disease in diseases){
          disease_types =  c(disease_types,
                             colnames(temp_2)[which(grepl(disease, colnames(temp_2)))])
        }
        
        temp_2 = temp_2 %>%
          pivot_longer(-c(S_YR, winter_PLANTCT), names_to = "Disease") %>% 
          filter(Disease %in% disease_types) 
        
        if (dim(temp_2)[1] == 0){
          p_dp = p_dp +
            labs(x = "Year", 
                 y = paste0("Percentage of potato with ", dis_lab)) +
            ggtitle("Disease Prevalenve")
        }else{
          p_dp = p_dp +
            geom_line(data = temp_2, 
                      aes(x = S_YR, y = value, col = Disease)) + 
            geom_point(data = temp_2,
                       aes(x = S_YR, y = value, col = Disease),
                       shape = 19) +
            labs(x = "Year", 
                 y = paste0("Percentage of potato with ", dis_lab)) +
            ggtitle("Disease Prevalenve")
        }
      }
      
      ggplotly(p_dp)
    }
  }
