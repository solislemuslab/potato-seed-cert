##### Acre Rejection #####
plot_acre_rejection <- 
  function(mydf, lots, varieties){
    # If data not valid
    if (is.null(mydf)){
      p_ar_lots = ggplot(mydf, aes(x = c(0,1), y = c(0,1))) + 
        annotate("text",x=0.5,y=0.5,label="Please upload data") + 
        labs(x = "", y = "") + 
        theme(plot.caption = element_text(size = 10))
      
      p_ar_var = ggplot()
    }
    else{
      # By Lot of potatoes
      temp_lots = mydf %>% 
        filter(LNAME %in% lots) %>% 
        group_by(LNAME) %>% 
        select(c("LNAME", "ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ")) %>% 
        summarise_all(sum) %>% 
        mutate("Summer" = AC_REJ / ACRES,
               "Winter"  = winter_AC_REJ / winter_ACRES) %>%
        select(-c("ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ")) %>% 
        pivot_longer(-LNAME, names_to = "season", values_to = "Rej_pct")
      
      p_ar_lots = temp_lots %>% 
        ggplot(aes(x = factor(LNAME), y = Rej_pct)) + 
        geom_col(aes(fill = season), position = "dodge") + 
        labs(x = "Potato Lot Name", 
             y = "Rejection Percentage") +
        ggtitle("Acre Rejection Percentage by Lot")
      
      # By Variety of potatoes
      temp_var = mydf %>% 
        filter(VARIETY %in% varieties) %>% 
        group_by(VARIETY) %>% 
        select(c("VARIETY", "ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ")) %>% 
        summarise_all(sum) %>% 
        mutate("Summer" = AC_REJ / ACRES,
               "Winter"  = winter_AC_REJ / winter_ACRES) %>%
        select(-c("ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ")) %>% 
        pivot_longer(-VARIETY, names_to = "season", values_to = "Rej_pct")
      
      p_ar_var = temp_var %>% 
        ggplot(aes(x = VARIETY, y = Rej_pct)) + 
        geom_col(aes(fill = season), position = "dodge") + 
        labs(x = "Potato Variety Name",
             y = "Rejection Percentage") + 
        theme(axis.text.x = element_text(angle = 45)) +
        ggtitle("Acre Rejection Percentage by Variety")
    }
    return(list("lot" = ggplotly(p_ar_lots),
                "var" = ggplotly(p_ar_var)))
  }
