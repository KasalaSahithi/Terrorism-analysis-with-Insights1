print('hii!!')

#importing the libraries
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate

app = dash.Dash()


def load_data():
  dataset_name = "globalterror.csv"

  pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  
  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]

  global date_list
  date_list = [x for x in range(1, 32)]


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  global country_list
  #country_list = [{"label": str(i), "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())]
  country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  global provstate_list
  #provstate_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
  provstate_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()


  global city_list
  #city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
  city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()


  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  
  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  
  #chart dropdown options
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
def open_webbrowser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app_ui():
  # Create the UI of the Webpage 
  main_layout = html.Div(
                style={
                          'background-image': 'url("/assets/13.jpg")',
                          'background-repeat': 'no-repeat',
                          'background-position': 'center',
                          'background-size': 'cover'
                          },children = [
  html.H1('Terrorism Analysis with Insights', id='Main_title',style={'textAlign':'center',
                                                                     'color':'midnightblue','height':'50px',
                                                                     'padding':'20px'
                                                                     }),
 
  dcc.Tabs(id="Tabs", value="Map",children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
          dcc.Tabs(id = "subtabs_1", value = "WorldMap",children = [
              dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
              dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
              ],
              colors={
                  'border':'blue',
                  'primary':'blue',
                  'background':'Lavender'}),
         html.Div(children=[ dcc.Dropdown(
              id='month', 
              style={
                     'float':'left',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue',
                    'background':'aliceblue'
                    },
              
                options=month_list,
                placeholder='Select Month',
                multi = True
                  ),
          dcc.Dropdown(
                id='date',
                style={
                    'float':'right',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue','background':'aliceblue'},
                placeholder='Select Day',
                multi = True
                  )]),
         
         html.Div(children=[ dcc.Dropdown(
                id='region_dropdown',
                style={
                     'float':'left',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue','background':'aliceblue'},
                options=region_list,
                placeholder='Select Region',
                multi = True
                  ),
          dcc.Dropdown(
                id='country_dropdown',
                style={
                     'float':'right',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue','background':'aliceblue'},
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select Country',
                multi = True
                  )]),
        
        html.Div(children=[ dcc.Dropdown(
                id='provstate_dropdown',
                style={
                    'float':'left',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue','background':'aliceblue'},
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select State or Province',
                multi = True
                  ),
          dcc.Dropdown(
                id='city_dropdown', 
                style={'float':'right',
                     'margin':'auto',
                    'width': '660px',
                    'color':'blue','background':'aliceblue'},
                options=[{'label': 'All', 'value': 'All'}],
                placeholder='Select City',
                multi = True
                  )]),
       
         html.Div(children=[ dcc.Dropdown(
                id='attacktype_dropdown', 
                style={
                    'float':'center',
                     'margin':'auto',
                    'width': '1000px',
                    'color':'blue','background':'aliceblue'},
                options=attack_type_list,
                placeholder='Select Attack Type',
                multi = True
                  )]),

          html.H3('Select the Year', id='year_title',style={'color':'darkmagenta',
                                                            }),
          
          dcc.RangeSlider(
                    id='mapyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                      ),
          html.Br()
    ]),
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
          dcc.Tabs(id = "subtabs_2", value = "WorldChart",children = [
              dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")],
              colors={
                  'border':'blue',
                  'primary':'blue',
                  'background':'Lavender'}),
            dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt"), 
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Hr(),
            html.Br(),
            dcc.RangeSlider(
                    id='chartyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
              ]
          )
         ],colors={
                  'border':'blue',
                  'primary':'blue',
                  'background':'Lavender'}
      ),
            
    
  html.Div(id = "graph-object", children ="Graph will be shown here"),
  html.Div(
      html.H3(children = 'Thankyou for using my webpage',style={'color':'darkmagenta',
                                                             'textAlign':'center',
                                                             'height':'25px'
                                                             
                                                             }))
  ])
        
  return main_layout


# Callback of your page
@app.callback(dash.dependencies.Output('graph-object', 'children'),
    [
     dash.dependencies.Input("Tabs", "value"),
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region_dropdown', 'value'),
    dash.dependencies.Input('country_dropdown', 'value'),
    dash.dependencies.Input('provstate_dropdown', 'value'),
    dash.dependencies.Input('city_dropdown', 'value'),
    dash.dependencies.Input('attacktype_dropdown', 'value'),
    dash.dependencies.Input('mapyear_slider', 'value'), 
    dash.dependencies.Input('chartyear_slider', 'value'), 
    
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("subtabs_2", "value")
    ]
    )

def update_app9_ui(Tabs, month_value, date_value,region_value,country_value,provstate_value,city_value,attack_value,mapyear_value,chartyear_value, chart_dp_value, search,
                   subtabs_2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month_value)))
        print("Data of month value = " , month_value)
        
        print("Data Type of Day value = " , str(type(date_value)))
        print("Data of Day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Data of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Data of country value = " , country_value)
        
        print("Data Type of provstate value = " , str(type(provstate_value)))
        print("Data of provstate value = " , provstate_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Data of city value = " , city_value)
        
        print("Data Type of Attack value = " , str(type(attack_value)))
        print("Data of Attack value = " , attack_value)
        
        print("Data Type of mapyear value = " , str(type(mapyear_value)))
        print("Data of year mapvalue = " , mapyear_value)
        
        # year_filter
        mapyear_range = range(mapyear_value[0], mapyear_value[1]+1)
        new_df = df[df["iyear"].isin(mapyear_range)]
        
        # month_filter
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)
                                & (new_df["iday"].isin(date_value))]
        # region, country, state, city filter
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if provstate_value == [] or provstate_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(provstate_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                        (new_df["country_txt"].isin(country_value)) &
                        (new_df["provstate"].isin(provstate_value))&
                        (new_df["city"].isin(city_value))]
                        
        if attack_value == [] or attack_value is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)] 
        
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        
        chartyear_range = range(chartyear_value[0], chartyear_value[1]+1)
        chart_df = df[df["iyear"].isin(chartyear_range)]
        
        
        if subtabs_2 == "WorldChart":
            pass
        elif subtabs_2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dp_value)
        fig = chartFigure
    return dcc.Graph(figure = fig)



@app.callback(
  Output("date", "options"),
  [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region_dropdown", "value"),
               Output("region_dropdown", "disabled"),
               Output("country_dropdown", "value"),
               Output("country_dropdown", "disabled")],
              [Input("subtabs_1", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country_dropdown', 'options'),
    [Input('region_dropdown', 'value')])
def set_country_options(region_value):
    option = []
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('provstate_dropdown', 'options'),
    [Input('country_dropdown', 'value')])
def set_state_options(country_value):
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in provstate_list.keys():
                option.extend(provstate_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city_dropdown', 'options'),
    [Input('provstate_dropdown', 'value')])
def set_city_options(provstate_value):
    option = []
    if provstate_value is None:
        raise PreventUpdate 
    else:
        for var in provstate_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]

# Flow of Project
def main():
  load_data()
  open_webbrowser()
  global app
  app.layout = create_app_ui()
  app.title = "Terrorism Analysis with Insights"
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() 

  print("byee")
  df = None
  app = None



if __name__ == '__main__':
    main()




