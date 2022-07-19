# Importing modules
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import findspark
findspark.init()
from pyspark.sql import SparkSession 
from pyspark.ml import PipelineModel
from pyspark.sql.functions import *

# Configure spark session
spark = SparkSession\
    .builder\
    .master('local[2]')\
    .appName('quake_etl')\
    .config('spark.jars.package', 'org.mongodb.spark:mongo-spark-connector 2.12:2.4.1')\
    .getOrCreate()
from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models.tools import HoverTool
import math
from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
from bokeh.tile_providers import CARTODBPOSITRON, get_provider, Vendors
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
import warnings
warnings.filterwarnings('ignore') 
from pyspark.sql.functions import desc
    
df=joblib.load('df.joblib')
data=spark.createDataFrame(df)
df_quake_freq=joblib.load('vis/df_quake_freq.joblib')
df_pred=joblib.load('vis/rffpred.joblib')
def svm(a):
    clf=joblib.load('C:\\Users\\Ramz\\Jupyter ML\\1st Review\\svmModel.joblib')
    a=np.array([a])
    y_pred_svm=clf.predict(a)
    return y_pred_svm[0]/10
def dt(a):
    a=np.array([a])
    dc=joblib.load('C:\\Users\\Ramz\\Jupyter ML\\1st Review\\dtModel.joblib')
    y_pred_dc=dc.predict(a)
    return y_pred_dc[0]
def rf(a):
    pipe=PipelineModel.load("C:\\Users\\Ramz\\Jupyter ML\\1st Review\\rfmodel.model_v0")
    ip = pd.DataFrame(np.array([a]))
    ip.columns=['Latitude','Longitude','Depth']
    dip=spark.createDataFrame(ip)
    pred_results_RF = pipe.transform(dip)
    return pred_results_RF.collect()[0][4]
def knn(a):
    from sklearn.neighbors import KNeighborsRegressor
    #Seperating X and y
    X=df[['Year','Latitude','Longitude','Depth']]
    y=df[['Magnitude']]
    kneigh=KNeighborsRegressor(n_neighbors = 5)
    kneigh.fit(X, y.values.ravel())
    a=np.array([a])
    y_pred_knn=kneigh.predict(a)
    return y_pred_knn[0]
def style(p):

        p.title.align='center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'serif'

        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style= 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style= 'bold'

        p.xaxis.major_label_text_font_size = '12pt' 
        p.yaxis.major_label_text_font_size = '12pt'

        p.legend.location = 'top_left'
        return p
def showmap():
    
        # Earthquakein Map Representation 
    df_quakes_2016 = data[data['Year']==2016]

    df_quakes_2016=df_quakes_2016.toPandas()

    def plotMap():
        lat = df_quakes_2016['Latitude'].values.tolist()
        lon = df_quakes_2016['Longitude'].values.tolist()
        
        pred_lat = df_pred['Latitude'].values.tolist()
        pred_lon = df_pred['Longitude'].values.tolist()
        
        lst_lat = []
        lst_lon = []
        lst_pred_lat = []
        lst_pred_lon = []
        
        i=0
        j=0
        

        for i in range (len(lon)):
            r_major = 6378137.000
            x = r_major * math.radians(lon[i])
            scale = x/lon[i]
            y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 +
            lat[i] * (math.pi/180.0)/2.0)) * scale
            
            lst_lon.append(x)
            lst_lat.append(y)
            i += 1
            
        
        for j in range (len(pred_lon)):
            r_major = 6378137.000
            x = r_major * math.radians(pred_lon[j])
            scale = x/pred_lon[j]
            y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 +
            pred_lat[j] * (math.pi/180.0)/2.0)) * scale
        
            lst_pred_lon.append(x)
            lst_pred_lat.append(y)
            j += 1
            
        df_quakes_2016['coords_x'] = lst_lat
        df_quakes_2016['coords_y'] = lst_lon
        df_pred['coords_x'] = lst_pred_lat
        df_pred['coords_y'] = lst_pred_lon
        
        df_quakes_2016['Mag_Size'] = df_quakes_2016['Magnitude'] * 4
        df_pred['Mag_Size'] = df_pred['Pred_Magnitude'] * 4
        

        lats = df_quakes_2016['coords_x'].tolist()
        longs = df_quakes_2016['coords_y'].tolist()
        mags = df_quakes_2016['Magnitude'].tolist()
        years = df_quakes_2016['Year'].tolist()
        mag_size = df_quakes_2016['Mag_Size'].tolist()
        
        pred_lats = df_pred['coords_x'].tolist()
        pred_longs = df_pred['coords_y'].tolist()
        pred_mags = df_pred['Pred_Magnitude'].tolist()
        pred_year = df_pred['Year'].tolist()
        pred_mag_size = df_pred['Mag_Size'].tolist()
        
        
        cds = ColumnDataSource(
        data=dict(
        lat=lats,
        lon=longs,
        mag=mags,
        year=years,
        mag_s=mag_size
        )
        )
        
        pred_cds = ColumnDataSource(
        data=dict(
        pred_lat=pred_lats,
        pred_long=pred_longs,
        pred_mag=pred_mags,
        year=pred_year,
        pred_mag_s=pred_mag_size
        )
        )
        

        TOOLTIPS = [( "Year", "@year"), ("Magnitude", "@mag"),("Predicted Magnitude", "@pred_mag")
        ]
        

        p = figure(title = 'Earthquake Map',
        plot_width=2300, plot_height=450,
        x_range=(-2000000, 6000000),
        y_range=(-1000000, 7000000),
        tooltips=TOOLTIPS)
        
        p.circle(x='lon', y='lat', size='mag_s', fill_color='#cc0000', fill_alpha=0.7,
        source=cds, legend='Quakes 2016')
        

        p.circle(x='pred_long', y='pred_lat', size='pred_mag_s', fill_color='#ccff33', fill_alpha=7.0,
        source=pred_cds, legend='Predicted Quakes 2017')
        
        tile_provider = get_provider(Vendors.CARTODBPOSITRON)
        p.add_tile(tile_provider)
        

        p.title.align='center'
        p.title.text_font_size='20pt'
        p.title.text_font='serif'
        
        
        p.legend.location='bottom_right'
        p.legend.background_fill_color='black'
        p.legend.background_fill_alpha=0.8
        p.legend.click_policy='hide'
        p.legend.label_text_color='white'
        p.xaxis.visible=False
        p.yaxis.visible=False
        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color=None
        show(p)
    df_quakes_2016['Magnitude']
    plotMap()

def freqgraph():
    #Frequency of Earthquake By Year
    def plotBar():
    
        cds = ColumnDataSource(data=dict(
            yrs= df_quake_freq[ 'Year'].values.tolist(),
            numQuakes = df_quake_freq['Counts'].values.tolist()))

        TOOLTIPS =[ ('Number of earthquakes','@numQuakes'),('Year','@yrs')]

        barChart = figure(title='Frequency of Earthquakes by Year',
                    plot_height=400,
                    plot_width=1150,
                    x_axis_label='Years', 
                    y_axis_label='Number of Occurances',
                    x_minor_ticks=2,
                    y_range=(0, df_quake_freq['Counts'].max() +100), 
                    toolbar_location=None,
                    tooltips=TOOLTIPS)

        print(cds)
        barChart.vbar (x='yrs', bottom=0, top='numQuakes',
                color='#cc0000', width=0.75, 
                legend='Year', source=cds)

        barChart = style(barChart)
        show(barChart)
        return barChart
    plotBar()

def maggraph():
    def plotMagnitude():
 
        cds= ColumnDataSource(data=dict(
        yrs = df_quake_freq[ 'Year'].sort_values().values.tolist(),
        avg_mag = df_quake_freq['avg(Magnitude)'].round(1).values.tolist(), 
        max_mag= df_quake_freq [ 'max(Magnitude)'].values.tolist()))

        TOOLTIPS = [('Year', '@yrs'),('avg(Magnitude)', '@avg_mag'),('max(Magnitude)','@max_mag')]

        mp = figure(title='Maximum and Average Magnitude by Year', 
                    plot_width=1150,
                    plot_height=400,
        x_axis_label='Years',
        y_axis_label='Magnitude', y_range=(5, df_quake_freq[ 'max(Magnitude)'].max() + 1),
        x_minor_ticks=2,
        toolbar_location=None, 
        tooltips= TOOLTIPS)

        mp.line(x='yrs', y='max_mag', color='#cc0000', line_width=2, legend= 'Max Magnitude', source=cds) 
        mp.circle(x='yrs', y='max_mag', color='#cc0000', size=8, fill_color='#cc0000', source=cds)

        mp.line(x='yrs', y='avg_mag', color='yellow', line_width=2, legend = 'Avg Magnitude', source=cds) 
        mp.circle(x='yrs', y='avg_mag', color='yellow', size=8, fill_color='yellow', source=cds)
        mp =style(mp)
        show(mp)
        return mp

    plotMagnitude()


