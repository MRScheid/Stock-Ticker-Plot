from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show
from bokeh.models import Range1d
from bokeh.embed import components
from bokeh.resources import INLINE
import pandas as pd 
import quandl
import os

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def not_index():
    # If resetting to homepage, delete previous query entry
    app.vars={}  
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():

    if request.method == 'GET':
        # If resetting to homepage, delete previous query entry
        app.vars={}
        return render_template('index.html')

    else:
        # request was a POST
        app.vars['ticker'] = request.form['ticker']
        
        # Check if feature1 was selected, if so extract the value
        if 'feature1' in request.form.keys():
            app.vars['feature1'] = request.form['feature1']
            
            # Lines used for debugging
            # f = open('%s.txt'%(app.vars['ticker']),'w')
            # f.write('Feature 1: %s\n'%(len(app.vars['feature1'])))
            # f.close()
        if 'feature2' in request.form.keys():
            app.vars['feature2'] = request.form['feature2']

        return redirect('/graph')

@app.route('/graph')
def graph():

    # Pull the user input from the last page to input for Quandl API data lookup
    tick = app.vars['ticker']
    
    # select the tools we want
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"

    # build our figures
    p = figure(tools=TOOLS, x_axis_type='datetime')
    
    # Check if feature1 was selected, if so query Quandl API and plot
    # With more features, this snippet could be refactored into a dedicated function
    if 'feature1' in app.vars.keys():
        # If feature exists pull it from app object
        feature1 = app.vars['feature1']
        
        # Now pull the appropriate data from Quandl API using this feature label
        data1 = quandl.get_table('WIKI/PRICES', 
                        qopts = { 'columns': ['date', '%s' %feature1] },
                        ticker = ['%s' % tick],
                        date = { 'gte': '2018-02-01', 'lte': '2018-02-29' },
                        api_key="DpZmHcsuom4huTFTtTZw")
        
        # Coerce extracted data to pandas datetime format      
        data1['date'] = pd.to_datetime(data1['date'])
        
        # Create figure glyph 
        p.line(data1['date'], data1['close'], 
               color="red", 
               alpha=0.5, 
               legend_label='%s: Closing price'% tick)
        
        del app.vars['feature1']
               
    # Check if feature2 was selected, if so query Quandl API and plot   
    if 'feature2' in app.vars.keys():
        # If feature exists pull it from app object
        feature2 = app.vars['feature2']
        
        # Now pull the appropriate data from Quandl API using this feature label
        data2 = quandl.get_table('WIKI/PRICES', 
                        qopts = { 'columns': ['date', '%s' %feature2] },
                        ticker = ['%s' % tick],
                        date = { 'gte': '2018-02-01', 'lte': '2018-02-29' },
                        api_key="DpZmHcsuom4huTFTtTZw")
        
        # Coerce extracted data to pandas datetime format 
        data2['date'] = pd.to_datetime(data2['date'])
        
        # Create figure glyph 
        p.line(data2['date'], data2['adj_close'], 
               color="blue", 
               alpha=0.5, 
               legend_label='%s: Adj Closing price'% tick)
               
        del app.vars['feature2']
    
    # Create the HTML script to pass and embed in the graph.html page
    script, div = components(p)
    resources = INLINE.render()

    # Now render the graph.html and pass scripts
    return render_template('graph.html',tick=tick,GenBokehPlot=script,GenBokehDiv=div,resources=resources)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)