# potato-seed-cert
Data analysis and visualization code for the potato seed certification database


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
 

## Steps to run this website locally
Users with strong programming skills might like to modify the existing code and run a version of the website locally.

1. Clone this repository

```
git clone https://github.com/solislemuslab/potato-seed-cert
```


2. Get inside the BioKlustering-Website folder, create and activate a python virtual environment:

```
cd potato-seed-cert
python3 -m venv virtual-env
source virtual-env/bin/activate
```
Note that Mac users could need the whole path to `python3`: `/usr/local/bin/python3`.

3. Install the necessary packages with
```
pip3 install -r requirements.txt
```
This step can take several minutes.

A list of packages can be found in the requirements.txt file and is listed below:
```
Brotli==1.0.9
certifi==2020.12.5
chardet==4.0.0
chart-studio==1.1.0
click==7.1.2
cycler==0.10.0
dash==1.20.0
dash-auth==1.4.1
dash-bootstrap-components==0.12.0
dash-core-components==1.16.0
dash-html-components==1.1.3
dash-renderer==1.9.1
dash-table==4.11.3
et-xmlfile==1.0.1
Flask==1.1.2
Flask-Compress==1.9.0
Flask-SeaSurf==0.3.0
future==0.18.2
gunicorn==20.0.4
idna==2.10
itsdangerous==1.1.0
jellyfish==0.8.2
Jinja2==2.11.3
kiwisolver==1.3.1
MarkupSafe==1.1.1
matplotlib==3.4.1
numpy==1.20.2
openpyxl==3.0.7
pandas==1.2.4
patsy==0.5.1
Pillow==8.2.0
plotly==4.14.3
pyparsing==2.4.7
python-dateutil==2.8.1
pytz==2021.1
requests==2.25.1
retrying==1.3.3
scipy==1.6.2
seaborn==0.11.1
six==1.15.0
statsmodels==0.12.2
ua-parser==0.10.0
urllib3==1.26.4
Werkzeug==1.0.1
xlrd==2.0.1

```

4. Run the website with
```
python3 Index.py
```


