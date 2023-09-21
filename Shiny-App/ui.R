# UI
source("./styles/custom-styles.R")
source("./tabs/data-importTab.R")
source("./tabs/visualizationTab.R")
source("./tabs/statistical-testTab.R")
ui <- fluidPage(
  shinythemes::themeSelector(),
  custom_styles_text,
  custom_styles,
  navbarPage(
    "Wisconsin Seed Potato Certification Program",
    # theme = shinytheme("lumen"),
    
    data_import_tab,
    visualization_tab,
    stat_test_tab
  )
)


