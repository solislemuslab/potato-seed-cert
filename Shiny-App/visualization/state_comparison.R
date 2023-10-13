##### State Comparison #####
plot_state_comparison <- 
  function(mydf, inspection, states, year_min, year_max){
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
      # When selected less than 2 states
      if (length(states) < 2){
        p_sc <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
          annotate("text",x=0.5,y=0.5,label="Please select at least two states") + 
          labs(x = "", y = "") + 
          theme(plot.caption = element_text(size = 10)) +
          ggtitle("Comparison between States")
        ggplotly(p_sc)
      }
      
      # When states are selected properly
      else{
        temp <- generate_temp_sc(mydf, inspection, states, year_min, year_max)
        if (dim(temp)[1] < 2){
          p_sc = ggplot() +
            labs(x = "Disease", 
                 y = "Percentage of potato")
          p_sc = ggplotly(p_sc)
        }else{
          p_sc = ggparcoord(temp,
                            columns = 3:dim(temp)[2],
                            scale = "globalminmax",
                            groupColumn = "S_STATE") +
            labs(x = "Disease", y = "Percentage of Potato (%)") +
            ggtitle("Comparison between States")
          }
        p_sc
      }
    }
  }


generate_temp_sc <- 
  function(mydf, inspection, states, year_min, year_max){
    # Summer 1st
    if ("Summer_1st" %in% inspection){
      temp <- mydf %>% 
        filter(S_STATE %in% states,
               S_YR <= year_max,
               S_YR >= year_min) %>% 
        select(c("PLTCT_1", "S_STATE",
                 colnames(mydf)[grepl("^NO.*_1ST$", colnames(mydf))])) %>% 
        group_by(S_STATE) %>% 
        summarize_all(sum) %>% 
        mutate(across(matches("NO"), function(x) x/PLTCT_1*100))
      
      colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
    } else if ("Summer_2nd" %in% inspection){ # Summer 2nd
      temp <- mydf %>% 
        filter(S_STATE %in% states,
               S_YR <= year_max,
               S_YR >= year_min) %>% 
        select(c("PLTCT_2", "S_STATE",
                 colnames(mydf)[grepl("^NO.*_2ND$", colnames(mydf))])) %>% 
        group_by(S_STATE) %>% 
        summarize_all(sum) %>% 
        mutate(across(matches("NO"), function(x) x/PLTCT_2*100))
      
      colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^NO_", "", colnames(temp)[-1:-2]))
    } 
    else{ # Winter
      temp <- mydf %>%
        filter(S_STATE %in% states,
               S_YR <= year_max,
               S_YR >= year_min) %>%
        select(c("winter_PLANTCT", "S_STATE", "winter_MOSN",
                 "winter_LRN", "winter_MXDN")) %>%
        group_by(S_STATE) %>%
        summarize_all(sum) %>%
        mutate(across(matches("N$"), function(x) x/winter_PLANTCT*100))

      colnames(temp)[-1:-2] <- paste0("PCT_", gsub("^winter_|N$", "", colnames(temp)[-1:-2]), "_Winter")
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


map_plot_sc <- function(mydf, inspection, states, year_min, year_max, disease){
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
    # When selected less than 2 states
    if (length(states) < 2){
      p_sc <- ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please select at least two states") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10)) +
        ggtitle("Comparison between States")
      ggplotly(p_sc)
    }
    
    # When states are selected properly
    else{
      temp = generate_temp_sc(mydf, inspection, states, year_min, year_max)
      us_map = map_data("state")
      colnames(us_map)[5] = "S_STATE"
      
      state_mapping = data.frame(
        abb = state.abb,
        S_STATE = tolower(state.name)
      )
      
      target_col = grep(paste0("_",disease,"_"), colnames(temp), value = TRUE)
      
      temp_full = temp %>% 
        left_join(state_mapping, by = c("S_STATE" = "abb")) %>% 
        mutate(S_STATE_org = S_STATE,
               S_STATE = S_STATE.y)
      temp_full$value = temp_full[[target_col]]
      temp_full = temp_full %>% 
        select(S_STATE, value)
      merged_data = left_join(us_map, temp_full, by = "S_STATE")
      # print(merged_data)
      
      p = ggplot(data = merged_data, aes(x = long, y = lat, fill = value, group = group)) +
        geom_polygon(color = "grey") +
        scale_fill_gradient(na.value = "white") +
        # coord_fixed(1.3) +
        labs(title = "Comparison between States in map", fill = "Acre Rejection Rate")
      ggplotly(p)
    }
  }
  
  
  
  
}
