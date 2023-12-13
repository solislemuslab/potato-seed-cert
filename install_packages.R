packages <- readLines("./requirements.txt")

# Function to install and load packages
install_and_load <- function(package) {
  if (!require(package, character.only = TRUE)) {
    install.packages(package)
    library(package, character.only = TRUE)
  }
}

for (p in packages){
  install_and_load(p)
}

