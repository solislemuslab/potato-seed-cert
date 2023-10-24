# Potato-Seed-Dashboard Documentation
`Potato-Seed-Dashboard` is an online bioinformatics tool for visualizing and analyzing the potato seed certification database. It contains five sections: 1) "Data" for data uploading validation, 2) "Visualization" for descriptive analysis, 3) "Test" for statistical test between variables, 4) "Prediction" for predicting possible infection rate in the future, and 5) "Get Help" for frequently asked questions.
We classify the data based on state, disease type, season and potato.


The following shows the hierarchy of the website:
- [Potato-Seed-Dashboard Documentation](#potato-seed-dashboard-documentation)
    - [Data Section](#data-import-section)
      - [Data Table](#data-table)
      - [Paired Errors](#paired-errors)
      - [Outliers](#outliers)
      - [Missing Values](#missing-values)
    - [Visualization Section](#data-visualization-section)
      - [Disease Prevalence](#disease-prevalence)
      - [State Comparison](#state-comparison)
      - [Acre Rejection](#acre-rejection)
      - [Variety](#variety)
    - [Test Section](#statistical-test)
      - [Chi-square Test](#chi-square-test)
      - [ANOVA](#anova)
    - [Predictioon Section](#prediction-section)
    - [Get Help](#get-help)
- [Feedback](#feedback)


## Data Section
* There are four subtabs within this tab:
  * Data Table
  * Paired Errors
  * Outliers
  * Missing Values
* There are two buttons:
  * Download CSV: Enables users to download the latest data set.
  * Undo: Cancel the last change users made to the data.
  
### Data Table
* It enables users to upload the data and to check the latest data table.
* There is only one file required, which should be a csv/xlsx file that contains seed potato certification data. It should have high quality, which means that there should be little missing or wrong values.
* If there are wrong column names or data type, a warning box will appear. Users can make changes to their data according to the information.

### Paired Errors
* This subtab will give error summary for the variables that are supposed to be the same in Summer and Winter.
* Users can first check "Paired Error Summary" table, which contains missing value and mismatch information.
* For the below two data tables, users can check detailed data table with "Paired Missing Values" or "Paired Mismatch" (which will change according to the selected variable). Values can be changed by double clicking elements in both data tables.
* The "Fill Missing Values" button can deal with missing values:
  * If a variable (column) have missing values and they are not paired, i.e. the corresponding values in the other season are not missing, they will be imputed by those values.
  * If there are paired continuous missing values, users can solve them in **Missing Values** subtab. If there are paired discrete missing values, the corresponding samples (rows) will be deleted.
* For the "Fix Mismatches" button, it will change the values in winter variables (columns) into the corresponding values in summer variables (columns).

### Outliers
* The **Outliers** subtab explores the possible outliers in the variables (columns) that are used in the later analysis, possibly caused by miss typing. 
 
## Visualization Section
* There are 4 kinds of visualization plots implemented in this section: 
    * Disease Prevalence
    * State Comparison
    * Acre Rejection
    * Variety
* Each analysis contains bar plot/line plots showing potato health condition based on different classification criteria.
    
                                                             
### Disease Prevalence
* The disease prevalence page contains 4 drop down choices:
  * Inspection Season: Summer/Winter
  * Disease Type
  * State
  * Potato Variety
* After choosing the 4 elements above, it will generate a line plot. The x-axis is Year, and y-axis is Percentage of potato with the disease type you chose before.

![Website Home Page](assets/Website-Disease_Prevalence.png)

### State Comparison
* The state comparison page contains 3 drop down choices:
  * State
  * Inspection: 1ST/2ND
  * Year
* After choosing the 3 elements above, it will generate a line plot. It compares the susceptibility of potato to different diseases in different states. Each line corresponds to a state, and each axis corresponds to a disease type.


![Website Home Page](assets/Website-State_Comparasion.png)

### Acre Rejection
* The acre rejection page contains two bar plots based on different classification criterias:
  * Potato Lot Name
  * Potato Variety
* The y-axis of each bar plot is Rejection Percentage (ACRE_REJ/ACRE_TOTAL). The x-axis is different potato lot name or potato variety. For each potato lot name/potato variety, it shows two bars -- one for summer and one for winter.

![Website Home Page](assets/Website-Acre_Rejection.png)

### Variety
* The variety page contains 4 drop down choices:
  * Season: Summer/Winter
  * Disease 
  * Variety
  * Year
* After choosing the 4 elements above, it will generate a bar plot. The x-axis is different kinds of potato variety, and y-axis is Percentage of potato with the disease type you chose before.

![Website Home Page](assets/Website-Variety.png)

## Test Section
### Chi-square Test
* The statistical test page contains two types of methods:
  * Pearson's Chi-Squared Test
  * Anova Test
* You need to filter the data first based on State, Year and Grower.
* For each test section, there are 3 drop down choices:
  * Disease
  * Source variable
  * Significant level: From 0 to 1
* After choosing the 3 elements above, it will generate a result table.

### ANOVA
* asdf

![Website Home Page](assets/Website-Stastical_Test.png)

## Prediction Section
* adf

## Get help
The FAQ Page contains questions and answers to common problems and doubts.

![Website FAQ Page](assets/Website-FAQ-Page.png)

# Feedback
* Issues reports are encouraged through the [GitHub Issue Tracker](https://github.com/solislemuslab/bioklustering/issues).
* Feedback is always welcome via the following [Google Form](https://forms.gle/SUYQ6X3WNotpQphj6).

