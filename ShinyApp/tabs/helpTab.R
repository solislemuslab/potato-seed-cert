# Help Tab
help_tab <- 
  tabPanel(
    "Get Help",
    h3("FAQ"),
    h4("Q: How can I learn to use the dashboard?"),
    
    "A: You can checkout the ",
    a("document", href = "https://github.com/solislemuslab/potato-seed-cert/blob/master/DOCS.md"),
    ".",
    tags$hr(),
    h4("Q: How can I get help?"),
    "A: Make sure to check out the ",
    a("document", href = "https://github.com/solislemuslab/potato-seed-cert/blob/master/DOCS.md"),
    "Also, check out the Potato Seed Dashboard Google User Group where people post questions and \
    answers. You can join ",
    a("here", href = "https://groups.google.com/access-error?continue=https://groups.google.com/g/potato-seed-dashboard"),
    " to post questions.",
    tags$hr(),
    h4("Q: Is the Potato Seed Dashboard open-source? Where can I find the code?"),
    "A: Yes, the Potato Seed Dashboard is open source, \
    and you can find all the code in the GitHub repository ",
    a("here", href = "https://github.com/solislemuslab/potato-seed-cert"),
    ".",
    tags$hr(),
    h4("Q: I found a bug or error in the dashboard, how can I report it?"),
    "A: You should file an issue in the ",
    a("github repo", href = "https://github.com/solislemuslab/potato-seed-cert/issues"),
    ".",
    tags$hr(),
    h4("Q: How can I provide positive (or constructive) feedback?"),
    "A: Users feedback is very important to us! Please use the form ",
    a("here", href = "https://docs.google.com/forms/d/e/1FAIpQLSficG2nYBjuAoIuetYC-5CRm339ZEZ_-uewd_d_3nVeGFMXUA/viewform?pli=1"),
    "."
  )
