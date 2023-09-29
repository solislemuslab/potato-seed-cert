##### Variety Comparison #####
plot_variety <- 
  function(mydf, inspections, disease, varieties, year_min, year_max){
    # When data is not uploaded
    if(is.null(mydf)){
      p_v <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      ggplotly(p_v)
    }
    
    # When data is uploaded
    else{
      # mydf[is.na(mydf)] = 0 # TBD
      
      temp = data.frame(matrix(ncol = 3, nrow = 0))
      colnames(temp) = c("VARIETY", "Disease", "value")
      # p_v = ggplot()
    
      # Summer
      if ("Summer" %in% inspections){
        temp_1 <- mydf %>% 
          filter(VARIETY %in% varieties,
                 S_YR <= year_max,
                 S_YR >= year_min) %>% 
          select(c("VARIETY", "PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", 
                   "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND")) %>% 
          group_by(VARIETY) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_2))

        
        colnames(temp_1)[-1:-2] <- 
          paste0("PCT_", gsub("^NO_|2ND", "", 
                              colnames(temp_1)[-1:-2]), "Summer")
        disease_type_1 = colnames(temp_1)[which(grepl(disease, colnames(temp_1)))]
      
        temp_1 = temp_1  %>% 
          pivot_longer(-c(VARIETY, PLTCT_2), names_to = "Disease")%>% 
          filter(Disease == disease_type_1) %>% 
          select(-PLTCT_2)
        
        temp = rbind(temp, temp_1)
      }
      # Winter
      if ("Winter" %in% inspections){
        temp_2 <- mydf %>%
          filter(VARIETY %in% varieties,
                 S_YR <= year_max,
                 S_YR >= year_min) %>%
          select(c("VARIETY", "winter_PLANTCT", "winter_MOSN",
                   "winter_LRN", "winter_MXDN")) %>%
          group_by(VARIETY) %>%
          summarize_all(sum) %>%
          mutate(across(matches("N$"), function(x) x/winter_PLANTCT))
        
        colnames(temp_2)[5] <- "winter_MIXN"
        
        
        colnames(temp_2)[-1:-2] <- 
          paste0("PCT_", gsub("^winter_|N$", "", 
                              colnames(temp_2)[-1:-2]), "_Winter")
        
        
        disease_type_2 = colnames(temp_2)[which(grepl(disease, colnames(temp_2)))]
        
        if (disease != "ST" & disease != "BRR"){
          temp_2 = temp_2 %>%
            pivot_longer(-c(VARIETY, winter_PLANTCT), names_to = "Disease") %>% 
            filter(Disease == disease_type_2) %>% 
            select(-winter_PLANTCT)
          
          temp = rbind(temp, temp_2)
        }
      }

      if (dim(temp)[1] == 0){
        p_v = ggplot() + 
          labs(x = "Potato Variety", 
               y = paste0("Percentage of potato with ", disease)) +
          ggtitle("Comparison between Varieties")
      }else{
        p_v = ggplot(temp) + 
          geom_col(aes(x = VARIETY, y = value, fill = Disease),
                   position = "dodge") + 
          labs(x = "Potato Variety", 
               y = paste0("Percentage of potato with ", disease)) + 
          theme(axis.text.x = element_text(angle = 45)) +
          ggtitle("Comparison between Varieties")
      }
      ggplotly(p_v)
    }
  }


# # 
# dff = read.csv("/Users/fhawk/Downloads/data/data_ex.csv")
# dff[is.na(dff)] = 0
# temp_1 <- dff %>%
#   filter(S_YR >= 2010,
#          S_YR <= 2016) %>%
#   select(c("VARIETY", "PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND",
#            "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND")) %>%
#   group_by(VARIETY) %>%
#   summarize_all(sum) %>%
#   mutate(across(matches("NO"), function(x) x/PLTCT_2))
# 
# colnames(temp_1)[-1:-2] <- paste0("PCT_", gsub("^NO_|2ND", "", colnames(temp_1)[-1:-2]), "Summer")
# 
# 
# disease_type = colnames(temp_1)[which(grepl("MOS", colnames(temp_1)))]
# 
# temp_1 = temp_1  %>%
#   pivot_longer(-c(VARIETY, PLTCT_2), names_to = "Disease")%>%
#   filter(Disease == disease_type)
# p_v = ggplot()
# if (dim(temp_1)[1] == 0){
#   p_v = p_v +
#     labs(x = "Year",
#          y = paste0("Percentage of potato with ", "MOS"))
# }else{
#   p_v =  p_v +
#     geom_col(data = temp_1,
#              aes(x = VARIETY, y = value, fill = Disease)) +
#     labs(x = "Potato Variety",
#          y = paste0("Percentage of potato with ", "MOS"))
# }
# 
# # 
# # 
# # 
