# UI
source("./custom-styles.R")
source("./tabs/dataTab.R")
source("./tabs/visualizationTab.R")
source("./tabs/testTab.R")
source("./tabs/predictionTab.R")
source("./tabs/helpTab.R")

ui <- fluidPage(
  theme = shinytheme("cerulean"),
  useShinyjs(),
  custom_styles,
  custom_styles_code,
  navbarPage(
    "Wisconsin Seed Potato Certification Program",
    data_tab,
    visualization_tab,
    test_tab,
    predict_tab,
    help_tab
  )
)


