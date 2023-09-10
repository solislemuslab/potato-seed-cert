##### State Comparison #####
plot_state_comparison <- 
  function(mydf, inspection, states, year){
    # When data is not uploaded
    if(is.null(mydf)){
      p_sc <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      ggplotly(p_sc)
    }
    
    # When data is uploaded
    else{
      mydf[is.na(mydf)] <- 0 # TBD
      
      # When selected less than 2 states
      if (length(states) < 2){
        p_sc <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
          annotate("text",x=0.5,y=0.5,label="Please select at least two states") + 
          labs(x = "", y = "") + 
          theme(plot.caption = element_text(size = 10)) +
          ggtitle("Comparison between States")
        ggplotly(p_sc)
      }
      
      else{
        # 1st
        # if ("Summer_1st" %in% inspection){
        #   temp <- generate_temp_sc(mydf, inspection, states, year)
        #   if (dim(temp)[1] < 2){
        #     p_sc = ggplot() +
        #       labs(x = "Disease", 
        #            y = "Percentage of potato")
        #     p_sc = ggplotly(p_sc)
        #   }else{
        #     p_sc = ggparcoord(temp,
        #                       columns = 3:dim(temp)[2],
        #                       # scale = "center",
        #                       groupColumn = "S_STATE") +
        #       labs(x = "Disease", y = "Percentage of Potato") +
        #       ggtitle("Comparison between States")
        #     # p_sc = with(temp, plot_ly(type = "parcoords",
        #     #                           line = list(color = ~PCT_colvar,
        #     #                                       colorscale = color_scale),
        #     #                           dimensions = list(
        #     #                             list(range = c(min(PCT_LR_1ST), max(PCT_LR_1ST)),
        #     #                                  label = "LR", values = ~PCT_LR_1ST),
        #     #                             list(range = c(min(PCT_MOS_1ST), max(PCT_MOS_1ST)),
        #     #                                  label = "MOS", values = ~PCT_MOS_1ST),
        #     #                             list(range = c(min(PCT_ST_1ST), max(PCT_ST_1ST)),
        #     #                                  label = "ST", values = ~PCT_ST_1ST),
        #     #                             list(range = c(min(PCT_MIX_1ST), max(PCT_MIX_1ST)),
        #     #                                  label = "MIX", values = ~PCT_MIX_1ST)
        #     #                           )))
        #   }
        # } else if ("Summer_2nd" %in% inspection){
        #   temp <- generate_temp_sc(mydf, inspection, states, year)
        #   if (dim(temp)[1] < 2){
        #     p_sc = ggplot() +
        #       labs(x = "Disease", 
        #            y = "Percentage of Potato")
        #     p_sc = ggplotly(p_sc)
        #   }else{
        #     p_sc = ggparcoord(temp,
        #                       columns = 3:dim(temp)[2],
        #                       # scale = "center",
        #                       groupColumn = "S_STATE") +
        #       labs(x = "Disease", y = "Percentage of Potato") +
        #       ggtitle("Comparison between States")
        #     # p_sc = with(temp, plot_ly(type = "parcoords",
        #     #                           line = list(color = ~PCT_colvar,
        #     #                                       colorscale = color_scale),
        #     #                           dimensions = list(
        #     #                             list(range = c(min(PCT_LR_2ND), max(PCT_LR_2ND)),
        #     #                                  label = "LR", values = ~PCT_LR_2ND),
        #     #                             list(range = c(min(PCT_MOS_2ND), max(PCT_MOS_2ND)),
        #     #                                  label = "MOS", values = ~PCT_MOS_2ND),
        #     #                             list(range = c(min(PCT_ST_2ND), max(PCT_ST_2ND)),
        #     #                                  label = "ST", values = ~PCT_ST_2ND),
        #     #                             list(range = c(min(PCT_MIX_2ND), max(PCT_MIX_2ND)),
        #     #                                  label = "MIX", values = ~PCT_MIX_2ND),
        #     #                             list(range = c(min(PCT_BRR_2ND), max(PCT_BRR_2ND)),
        #     #                                  label = "BRR", values = ~PCT_BRR_2ND),
        #     #                             list(range = c(min(PCT_TOTV_2ND), max(PCT_TOTV_2ND)),
        #     #                                  label = "TOTV", values = ~PCT_TOTV_2ND)
        #     #                           )))
        #   }
        # }
        # else{
        #   
        # }
                  temp <- generate_temp_sc(mydf, inspection, states, year)
          if (dim(temp)[1] < 2){
            p_sc = ggplot() +
              labs(x = "Disease", 
                   y = "Percentage of potato")
            p_sc = ggplotly(p_sc)
          }else{
            p_sc = ggparcoord(temp,
                              columns = 3:dim(temp)[2],
                              # scale = "center",
                              groupColumn = "S_STATE") +
              labs(x = "Disease", y = "Percentage of Potato") +
              ggtitle("Comparison between States")
            # p_sc = with(temp, plot_ly(type = "parcoords",
            #                           line = list(color = ~PCT_colvar,
            #                                       colorscale = color_scale),
            #                           dimensions = list(
            #                             list(range = c(min(PCT_LR_1ST), max(PCT_LR_1ST)),
            #                                  label = "LR", values = ~PCT_LR_1ST),
            #                             list(range = c(min(PCT_MOS_1ST), max(PCT_MOS_1ST)),
            #                                  label = "MOS", values = ~PCT_MOS_1ST),
            #                             list(range = c(min(PCT_ST_1ST), max(PCT_ST_1ST)),
            #                                  label = "ST", values = ~PCT_ST_1ST),
            #                             list(range = c(min(PCT_MIX_1ST), max(PCT_MIX_1ST)),
            #                                  label = "MIX", values = ~PCT_MIX_1ST)
            #                           )))
          }
        p_sc
      }
    }
  }


generate_temp_sc <- 
  function(mydf, inspection, states, year){
    mydf[is.na(mydf)] <- 0 # TBD
    # Specific year
    if (year != "All"){
      # 1st
      if ("Summer_1st" %in% inspection){
        temp <- mydf %>% 
          filter(S_STATE %in% states,
                 S_YR == year) %>% 
          select(c("PLTCT_1", "S_STATE",
                   colnames(mydf)[grepl("^NO.*_1ST$", colnames(mydf))])) %>% 
          group_by(S_STATE) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_1))
        
        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
      } else if ("Summer_2nd" %in% inspection){ # 2nd
        temp <- mydf %>% 
          filter(S_STATE %in% states,
                 S_YR == year) %>% 
          select(c("PLTCT_2", "S_STATE",
                   colnames(mydf)[grepl("^NO.*_2ND$", colnames(mydf))])) %>% 
          group_by(S_STATE) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_2))
        
        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
      } 
      else{
        temp_winter <- mydf %>%
          filter(S_STATE %in% states,
                 S_YR == year) %>%
          select(c("winter_PLANTCT", "S_STATE", "winter_MOSN",
                   "winter_LRN", "winter_MXDN")) %>%
          group_by(S_STATE) %>%
          summarize_all(sum) %>%
          mutate(across(matches("N$"), function(x) x/winter_PLANTCT))

        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^winter_|N$", "", colnames(temp)[-1:-2]), "_Winter")
      }
    }
    # All years
    else{
      # 1st
      if ("Summer_1st" %in% inspection){
        temp <- mydf %>% 
          filter(S_STATE %in% states) %>% 
          select(c("PLTCT_1", "S_STATE",
                   colnames(mydf)[grepl("^NO.*_1ST$", colnames(mydf))])) %>% 
          group_by(S_STATE) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_1)) 
        
        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
      } else if ("Summer_2nd" %in% inspection){ # 2nd
        temp <- mydf %>% 
          filter(S_STATE %in% states) %>% 
          select(c("PLTCT_2", "S_STATE",
                   colnames(mydf)[grepl("^NO.*_2ND$", colnames(mydf))])) %>% 
          group_by(S_STATE) %>% 
          summarize_all(sum) %>% 
          mutate(across(matches("NO"), function(x) x/PLTCT_2))
        
        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
      } 
      else{
        temp <- mydf %>%
          filter(S_STATE %in% states) %>%
          select(c("winter_PLANTCT", "S_STATE", "winter_MOSN",
                   "winter_LRN", "winter_MXDN")) %>%
          group_by(S_STATE) %>%
          summarize_all(sum) %>%
          mutate(across(matches("N$"), function(x) x/winter_PLANTCT))
        
        colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^winter_|N$", "", colnames(temp)[-1:-2]), "_Winter")
      }
    }
    return(temp)
  }
  

generate_color_scale <- function(mydf){
  colors = c("blue", "green", "red", "cyan", "magenta", "yellow", "black", "orange",
             "darkviolet", "royalblue", "pink", "purple", "maroon", "silver", "lime")
  color_scale = list()
  num_state = length(unique(mydf$S_STATE))
  for (i in 1:num_state){
    color_scale[[i]] = c(i/num_state, colors[i])
  }
}

# temp_1 <- dff %>% 
#   filter(S_STATE %in% c("CO", "WI"),
#          S_YR == 2005) %>% 
#   select(c("PLTCT_1", "S_STATE",
#            colnames(dff)[grepl("^NO.*_1ST$", colnames(dff))])) %>% 
#   group_by(S_STATE) %>% 
#   summarize_all(sum) %>% 
#   mutate(across(matches("NO"), function(x) x/PLTCT_1))
# 
# colnames(temp_1)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp_1)[-1:-2]))
# 
# if (dim(temp_1)[1] == 0){
#   p_sc = ggplot() +
#     labs(x = "Disease", 
#          y = "Percentage of potato")
#   p_sc = ggplotly(p_sc)
# }else{
#   p_sc = with(temp_1, plot_ly(type = "parcoords",
#                             line = list(color = ~S_STATE,
#                                         colorscale = list(c(0,'red'),c(0.5,'green'),c(1,'blue'))),
#                             dimensions = list(
#                               list(range = c(min(PCT_LR_1ST), max(PCT_LR_1ST)),
#                                    label = "LR", values = ~PCT_LR_1ST),
#                               list(range = c(min(PCT_MOS_1ST), max(PCT_MOS_1ST)),
#                                    label = "MOS", values = ~PCT_MOS_1ST),
#                               list(range = c(min(PCT_ST_1ST), max(PCT_ST_1ST)),
#                                    label = "ST", values = ~PCT_ST_1ST),
#                               list(range = c(min(PCT_MIX_1ST), max(PCT_MIX_1ST)),
#                                    label = "MIX", values = ~PCT_MIX_1ST)
#                             )))
# }
#   
  






