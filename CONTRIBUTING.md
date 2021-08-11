# Contributing to Potato-Seed-Dashboard
The following guidelines are designed for contributors to Potato-Seed-Cert. 

## Folder Structure 
```
potato-seed-cert/                    
├── apps/                          
│   ├── acres.py                    
│   ├── data_visualization.py       
│   ├── layout.py                   
│   ├── navbar.py                   
│   ├── prevalent_disease.py        
│   ├── state_comparison.py         
│   ├── statistical_test.py         
│   ├── upload.py                   
│   ├── variety.py                  
│   └── sub-folder/   
├── assets/                  
│   ├── tabs.css                                
│   └── download.png
├── .gitignore
├── Index.py  
├── README.md                                                                  
├── app.py   
├── notes.md 
├── requirements.txt                

```

* ```apps``` which contains the core files for all tabs
    * ```acres.py:``` plot the rejected acre by varieties and growers with bar chart                   
    * ```data_visualization.py:``` collect all plots under tabs      
    * ```layout.py:``` layout template for the sidebar                 
    * ```navbar.py:``` navigation bar on the top of the page                   
    * ```prevalent_disease.py:``` plot the prevalent disease over time with line plot       
    * ```state_comparison.py:``` compare disease rate across various diseases with parallel coordinated plots     
    * ```statistical_test.py:``` implement two statitical tests to check the correlation         
    * ```upload.py:``` upload data, data validation (missing value and string similarity check)             
    * ```variety.py:``` plot the sensitive and tolerant varieity 
* ```assets``` which contains the css files and images
    * ```tabs.css:``` tabs outlook in the data import section
    * ```download.img:``` the image attached to download button
* ```Index.py:``` loads different apps on different urls links
* ```app.py:``` core app definition, CSS loading, import and attach layout
* ```notes.md:``` discussion notes with Renee
* ```requirements.txt:``` requirements to run the code

## Reporting Issues

For reporting a bug or a failed function or requesting a new feature, you can simply open an issue in the [issue tracker](https://github.com/solislemuslab/potato-seed-cert/issues). If you are reporting a bug, please also include a minimal code example or all relevant information for us to replicate the issue.

## Contributing Code

To make contributions to Potato-Seed-Cert, you need to set up your [GitHub](https://github.com) 
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

Your contribution will be checked and merged into the original repository. You will be contacted if there is any problem in your contribution

Make sure to include the following information in your pull request:

* **Code** which you are contributing to this package

* **Documentation** of this code if it provides new functionality. This should be a
  description of new functionality added to the `DOCS.md`

- **Tests** of this code to make sure that the previously failed function or the new functionality now works properly


**WARNING:** When you run the website locally, you will have many changes to `.pyc` local files that you should discard prior to any commit with `git checkout -- <file>` and new untracked files created when running the website locally should be deleted prior to any commit if you intent to contribute to the website. Make sure that your pull request do not include changes to these files.

---

_These Contributing Guidelines have been adapted from the [Contributing Guidelines](https://github.com/atomneb/AtomNeb-py/blob/master/CONTRIBUTING.md) of [The Turing Way](https://github.com/atomneb/AtomNeb-py)! (License: GNU GENERAL PUBLIC)_