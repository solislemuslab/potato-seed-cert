# Styles of bars
custom_styles <- 
  tags$head(
    tags$style(HTML("
                    .navbar-brand {
                      font-size: 30px;
                      font-weight: bold;
                      padding-top: 15px;
                      padding-bottom: 15px;
                    }
                    .navbar {
                      font-size: 18px;
                    }
                    .sidebar-panel {
                      background-color: #f8f9fa;
                      color: black;
                    }
                  "))
  )

# Styles of code
custom_styles_code <- 
  tags$style(HTML("
    code {
      background-color: white;
      color: deepskyblue;
      padding: 2px 4px;          /* Padding around the text */
      border: 1px solid #e1e1e8; /* Border around the code */
      border-radius: 4px;        /* Rounded corners */
    }
  "))