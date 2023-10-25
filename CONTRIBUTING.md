# Contributing to Potato-Seed-Dashboard
The following guidelines are designed for contributors to Potato-Seed-Cert. 

## Folder Structure 
```
potato-seed-cert/                    
├── ShinyApp/                          
│   ├── server.R       
│   ├── ui.R                   
│   ├── global.R
│   ├── custom-styles.R  
│   ├── tabs/
│   │   ├── dataTab.R
│   │   ├── visualizationTab.R
│   │   ├── testTab.R
│   │   ├── predictionTab.R
│   │   └── helpTab.R
│   ├── dataimport/
│   │   ├── data_table.R
│   │   ├── paired.R
│   │   ├── outliers.R
│   │   └── other_miss.R
│   ├── visualization/
│   │   ├── acre_rejection.R
│   │   ├── disease_prevalence.R
│   │   ├── state_comparison.R
│   │   └── variety.R
│   ├── test/
│   │   ├── anova.R
│   │   └── chi_sqr.R
│   ├── predict/
│   │   └── predict.R
├── assets/   
├── .gitignore
├── CONTRIBUTING.md
├── DOCS.md
├── Data-Format.md
├── LICENSE 
├── README.md 
├── requirements.txt
├── unused/

```

* ```ShinyApp/:``` Contains the core files for all tabs of the website:
    * ```server.R:``` Contains the server logic that handles the input from the UI and produces the corresponding outputs.        
    * ```ui.R:``` Defines the user interface.
    * ```global.R:``` Defines global variables and load libraries.
    * ```custom-styles.R:``` Customizes the text styles of the dashboard.
    * ```tabs/:``` Contains the layout and appearance files of each tab:, Data Tab, Visualiaztion Tab, Test Tab, Prediction Tab, and Get Help Tab.
    * ```dataimport/:``` Contains files with functions used for Data Tab.
    * ```visualization/:``` Contains files with functions used for Visualization Tab.        
    * ```test/:``` Contains files with functions used for Test Tab.
    * ```predict/:``` Contains the file with functions used for Prediction Tab.
* ```assets/:``` Contains the images used for `DOCS.md`.
* ```.gitignore:``` Contains a list of files and folders that should be ignored by Git.
* ```CONTRIBUTING.md:``` Guidelines for contributors.
* ```DOCS.md:``` Instructions on how to use the dashboard.
* ```Data-Format.md:``` The required variable (column) names for the data set.
* ```LICENSE:``` The license of using the code.
* ```README.md:``` Information about the dashboard, how to run it, and any other pertinent information for users or contributors.
* ```requirements.txt:``` Required packages to run the dashboard code.

## Reporting Issues

For reporting a bug or a failed function or requesting a new feature, you can simply open an issue in the [issue tracker](https://github.com/solislemuslab/potato-seed-cert/issues). If you are reporting a bug, please also include a minimal code example or all relevant information for us to replicate the issue.

## Contributing Code

To make contributions to Potato-Seed-Dashboard, you need to set up your [GitHub](https://github.com) 
account if you do not have and sign in, and request your change(s) or contribution(s) via 
a pull request against the ``development``
branch of the [Potato-Seed-Cert repository](https://github.com/solislemuslab/potato-seed-cert). 

Please use the following steps:

1. Open a new issue for new feature or failed function in the [Issue tracker](https://github.com/solislemuslab/potato-seed-cert/issues)
2. Fork the [Potato-Seed-Cert repository](https://github.com/solislemuslab/potato-seed-cert)to your GitHub account
3. Clone your fork locally:
```
$ git clone https://github.com/your-username/potato-seed-cert.git
```   
4. Make your change(s) in the `master` (or `development`) branch of your cloned fork
5. Make sure that all tests are passed without any errors (upcoming automatic testing available in Potato-seed-cert)
6. Push your change(s) to your fork in your GitHub account
7. [Submit a pull request](https://github.com/solislemuslab/potato-seed-cert/pulls) describing what problem has been solved and linking to the issue you had opened in step 1

Your contribution will be checked and merged into the original repository. You will be contacted if there is any problem in your contribution.

Make sure to include the following information in your pull request:

* **Code** which you are contributing to this package.

* **Documentation** of this code if it provides new functionality. This should be a
  description of new functionality added to the `DOCS.md`.

- **Tests** of this code to make sure that the previously failed function or the new functionality now works properly.


**WARNING:** When you run the website locally, you will have many changes to `.pyc` local files that you should discard prior to any commit with `git checkout -- <file>` and new untracked files created when running the website locally should be deleted prior to any commit if you intent to contribute to the website. Make sure that your pull request do not include changes to these files.

---

_These Contributing Guidelines have been adapted from the [Contributing Guidelines](https://github.com/atomneb/AtomNeb-py/blob/master/CONTRIBUTING.md) of [The Turing Way](https://github.com/atomneb/AtomNeb-py)! (License: GNU GENERAL PUBLIC)_