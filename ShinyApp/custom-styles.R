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


custom_styles_text <-
  tags$div(
    style = "padding: 20px;",
    tags$style(type = 'text/css', "
                            .custom-h1 {
                              font-size: 28px;
                              font-weight: bold;
                              margin-bottom: 20px;
                            }
                            .custom-h2 {
                              font-size: 24px;
                              font-weight: bold;
                              margin-top: 30px;
                              margin-bottom: 10px;
                            }
                            .custom-p {
                              font-size: 16px;
                              line-height: 1.5;
                            }")
  )

custom_styles_code = 
  tags$style(HTML("
    code {
      background-color: white;
      color: deepskyblue;
      padding: 2px 4px;          /* Padding around the text */
      border: 1px solid #e1e1e8; /* Border around the code */
      border-radius: 4px;        /* Rounded corners */
    }
  "))