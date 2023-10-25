# Dashboard for the WI Potato and Vegetable Growers Association

This is an online dashboard for the data analysis and data visualization of the certification database of the seed potato production.

# Usage

`Potato-Seed-Dashboard` is browser-based (preferably Google Chrome), and thus, no installation is needed. Users simply need to click on the following link: https://potato-seed-dashboard.wid.wisc.edu/.

More details are available in the documentation: [DOCS.md](https://github.com/solislemuslab/potato-seed-cert/blob/master/DOCS.md).

More details on the folder structure can be found on the contributing file: [CONTRIBUTING.md](https://github.com/solislemuslab/potato-seed-cert/blob/master/CONTRIBUTING.md).

While we recommend the use of the dashboard via the online link, we present below the steps to run the dashboard locally.

## Steps to run this website locally
Users with strong programming skills might like to modify the existing code and run a version of the website locally.

1. Clone this repository

```
git clone https://github.com/solislemuslab/potato-seed-cert
```


2. Get inside the potato-seed-cert folder, create and activate an R virtual environment:

```
cd potato-seed-cert
R
```

3. Install the necessary packages with
```
install.packages(readLines("./requirements.txt"))
```
This step can take several minutes.

A list of packages can be found in the requirements.txt file and is listed below:
```
DT
DMwR2
forecast
GGally
mice
maps
plotly
readxl
shiny
shinythemes
shinyWidgets
shinyalert
shinyhelper
tidyverse

```

4. Run the website with
```
runApp("./ShinyApp")
```

# Contributions

Users interested in expanding functionalities in `Potato-Seed-Dashboard` are welcome to do so.
See details on how to contribute in [CONTRIBUTING.md](https://github.com/solislemuslab/potato-seed-cert/blob/master/CONTRIBUTING.md).

# License
`Potato-Seed-Dashboard` is licensed under the [GNU General Public ](https://www.gnu.org/licenses/) licence. &copy; SolisLemus lab projects (2021).

# Feedback, issues and questions

- Issues reports are encouraged through the [GitHub issue tracker](https://github.com/solislemuslab/potato-seed-cert/issuess)
- Feedback is always welcome via the following [google form](https://forms.gle/ijwGLmV5DVFyyqyx9)
