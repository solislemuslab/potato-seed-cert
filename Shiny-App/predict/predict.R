predict_prevalance = 
  function(mydf, state, diseases, variety, inspections){
    # When data is not uploaded
    if(is.null(mydf)){
      p_pp <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      ggplotly(p_pp)
    }else{
      p_pp = ggplot()
      
      dis_lab = ""
      for (disease in diseases){
        dis_lab = paste0(dis_lab, disease, ", ")
      }
      dis_lab = str_sub(dis_lab, 1, -3)
      
      # Summer
      if ("Summer" %in% inspections){
        temp_1 = mydf %>% 
          filter(S_STATE %in% state,
                 VARIETY == variety) %>% 
          select(c("S_YR", "S_STATE", "SR2_MOS", "SR2_LR", "SR2_MIX", 
                   "SR2_ST", "SR2_BRR"))
        
        colnames(temp_1)[-1:-2] <- paste0("PCT", gsub("^SR2", "", colnames(temp_1)[-1:-2]), "_Summer")
        
        disease_types = c()
        for (disease in diseases){
          disease_types =  c(disease_types, 
                             colnames(temp_1)[which(grepl(disease, colnames(temp_1)))])
        }
        
        temp_1 = temp_1  %>% 
          pivot_longer(-c(S_YR, S_STATE), names_to = "Disease")%>% 
          filter(Disease %in% disease_types)
        
        if (dim(temp_1)[1] == 0){
          p_pp = p_pp +
            labs(x = paste0("Percentage of potato with ", dis_lab), 
                 y = "State")
        }else{
          results = temp_1 %>% 
            group_by(S_STATE, Disease) %>% 
            do(model = auto.arima(.$value))
          
          predicted = sapply(results$model, 
                             function(x) forecast(x, h=1)$mean)
          results$rate_pred = predicted
          
          p_pp = p_pp + 
            geom_col(data = results, 
                     aes(x=rate_pred, y=S_STATE, fill=Disease),
                     position="dodge",
                     alpha = 0.5) + 
            labs(title="Forecasted Values by State and Disease Type",
                 x="Forecasted Value", y="State")
        }
      }
      
      # Winter
      if ("Winter" %in% inspections){
        temp_2 <- mydf %>%
          filter(S_STATE %in% state,
                 VARIETY == variety) %>%
          select(c("S_YR", "S_STATE", "winter_PLANTCT", "winter_MOSN",
                   "winter_LRN", "winter_MXDN")) %>%
          group_by(S_YR, S_STATE) %>%
          summarize_all(sum) %>%
          mutate(across(matches("N$"), function(x) x/winter_PLANTCT))
        
        colnames(temp_2)[6] = "winter_MIXN"
        colnames(temp_2)[-1:-3] <- paste0("PCT_", gsub("^winter_|N$", "", colnames(temp_2)[-1:-3]), "_Winter")
        
        disease_types = c()
        for (disease in diseases){
          disease_types =  c(disease_types,
                             colnames(temp_2)[which(grepl(disease, colnames(temp_2)))])
        }
        
        temp_2 = temp_2 %>%
          pivot_longer(-c(S_YR, winter_PLANTCT, S_STATE), names_to = "Disease") %>% 
          filter(Disease %in% disease_types) 
        
        if (dim(temp_2)[1] == 0){
          p_pp = p_pp +
            labs(x = paste0("Percentage of potato with ", dis_lab), 
                 y = "State")
        }else{
          results = temp_2 %>% 
            group_by(S_STATE, Disease) %>% 
            do(model = auto.arima(.$value))
          
          predicted = sapply(results$model, 
                             function(x) forecast(x, h=1)$mean)
          results$rate_pred = predicted
          
          p_pp = p_pp + 
            geom_col(data = results, 
                     aes(x=rate_pred, y=S_STATE, fill=Disease),
                     position="dodge",
                     alpha = 0.5) + 
            labs(title="Forecasted Values by State and Disease Type",
                 x="Forecasted Value", y="State")
        }
      }
      ggplotly(p_pp)
    }
  }
