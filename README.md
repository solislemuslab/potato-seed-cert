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

# Contributions

Users interested in expanding functionalities in `Potato-Seed-Dashboard` are welcome to do so.
See details on how to contribute in [CONTRIBUTING.md](https://github.com/solislemuslab/potato-seed-cert/blob/master/CONTRIBUTING.md).

# License
`Potato-Seed-Dashboard` is licensed under the [GNU General Public ](https://www.gnu.org/licenses/) licence. &copy; SolisLemus lab projects (2021).

# Feedback, issues and questions

- Issues reports are encouraged through the [GitHub issue tracker](https://github.com/solislemuslab/potato-seed-cert/issuess)
- Feedback is always welcome via the following [google form](https://forms.gle/ijwGLmV5DVFyyqyx9)
