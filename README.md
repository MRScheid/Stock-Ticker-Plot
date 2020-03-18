# Bokeh visualizations embedded in Flask, deployed on Heroku.

This project plots stock data from the WIKI Quandl database for February 2018 using Git, Flask, Pandas, Heroku, and Bokeh for visualization:

https://www.quandl.com/databases/WIKIP/data

File Organization and Function

├── app.py                  - Main application that handles URL routing, plot generation and dynamic Bokeh scripts
├── requirements.txt        - Handles all necessary packages for running app.py
├── templates
│   ├── index.html          - Landing page
│   ├── graph.html          - Page where embedded Bokeh visualization is shown
├── conda-requirements.txt  - Handles all packages available within conda
├── Procfile.txt            - Declares what command should be executed to start the app
└── runtime.txt             - Specifies what version of Python to run with this app
