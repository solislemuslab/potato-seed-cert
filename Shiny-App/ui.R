# UI
source("./styles/custom-styles.R")
source("./tabs/dataTab.R")
source("./tabs/visualizationTab.R")
source("./tabs/testTab.R")
ui <- fluidPage(
  # useShinyalert(),
  shinythemes::themeSelector(),
  custom_styles_text,
  custom_styles,
  navbarPage(
    "Wisconsin Seed Potato Certification Program",
    # theme = shinytheme("lumen"),
    
    data_tab,
    visualization_tab,
    test_tab
  )
)


