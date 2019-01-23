# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 18:31:37 2019

@author: baren
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt

import pyodbc
import pandas as pd

server = "ZAJNBRABABOTHA"
database = "master"



connstr = """DRIVER={ODBC Driver 11 for SQL Server};
            SERVER={server};
            database={database};
            Trusted_Connection=yes"""
            
conn = pyodbc.connect('Driver={ODBC Driver 11 for SQL Server};'
                      'Server=ZAJNBRABABOTHA;'
                      'Database={master};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute("select * from sys.databases")
vals = cursor.fetchall()  
databases = pd.DataFrame([row.name for row in vals], columns=['DB_Names'])    
database_name = "AdventureWorks2014"

sql = f"""SELECT * FROM {database_name}.information_schema.tables"""
"""
cursor.execute(sql)
vals2 = cursor.fetchall()
tables = pd.DataFrame([row.TABLE_NAME for row in vals2], columns=['Table_Names'])
tables['Schema'] = pd.DataFrame([row.TABLE_SCHEMA for row in vals2])
print(tables.head())
"""

def select_table(database_name):
    sql = f"""SELECT * FROM {database_name}.information_schema.tables"""
    cursor.execute(sql)
    vals2 = cursor.fetchall()
    tables = pd.DataFrame([row.TABLE_NAME for row in vals2], columns=['Table_Names'])
    tables['Schema'] = pd.DataFrame([row.TABLE_SCHEMA for row in vals2])
    return [{'label': i[1] + "." + i[0], 'value': i[1] + "." + i[0]} for i in tables.values]


def generate_table(table, db):
    sql = f"""Select * from {db}.{table}"""
    table_data = pd.read_sql(sql, conn)
    return table_data.to_dict('records')

def query(txt_box):
    table_data = pd.read_sql(str(txt_box), conn)
    return table_data.to_dict('records')
    


app = dash.Dash()
#app.config['suppress_callback_exceptions']=True
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='View tables', value='tab-1', children=[
            html.Div([
            html.H3(children='Databases in {} server'.format(server)),
            dcc.Dropdown(
                id='database-dropdown',
                options=[{'label': i[0], 'value': i[0]} for i in databases.values
                ], placeholder='Select available databases'),
            dcc.Dropdown(
                id='table-dropdown',
                placeholder='Select available tables',
                multi=False
            ),
            html.Button('Submit', id='Table_submit_button'),
            dt.DataTable(
                # Initialise the rows
                rows=[{}],
                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                id='table'
                ),
            html.Div(id='selected-indexes'),
        ])]),
        dcc.Tab(label='Custom Query', value='tab-2', children=[html.Div([
            html.H3(children='Custom Query'),
            dcc.Textarea(placeholder='Enter a value...',
            style={'width': '100%'},
            id="txt_box"
            ),
                html.Button('Submit', id='Table_submit_button_2'),
                dt.DataTable(
                    # Initialise the rows
                    rows=[{}],
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='table_2'
                    ),
                html.Div(id='selected-indexes_2'),
        ])]),
    ]),
    html.Div(id='tabs-content')
])


def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3(children='Databases in {} server'.format(server)),
            dcc.Dropdown(
                id='database-dropdown',
                options=[{'label': i[0], 'value': i[0]} for i in databases.values
                ], placeholder='Select available databases'),
            dcc.Dropdown(
                id='table-dropdown',
                placeholder='Select available tables',
                multi=False
            ),
            html.Button('Submit', id='Table_submit_button'),
            dt.DataTable(
                # Initialise the rows
                rows=[{}],
                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                id='table'
                ),
            html.Div(id='selected-indexes'),
        ]) 
    elif tab == 'tab-2':
        return html.Div([
            html.H3(children='Custom Query'),
            dcc.Textarea(placeholder='Enter a value...',
            style={'width': '100%'},
            id="txt_box"
            ),
                html.Button('Submit', id='Table_submit_button_2'),
                dt.DataTable(
                    # Initialise the rows
                    rows=[{}],
                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    id='table_2'
                    ),
                html.Div(id='selected-indexes'),
        ])
"""
app.layout = html.Div(children=[
    html.H4(children='Databases in {} server'.format(server)),
    dcc.Dropdown(
        id='database-dropdown',
        options=[{'label': i[0], 'value': i[0]} for i in databases.values
        ], placeholder='Select available databases'),
    dcc.Dropdown(
        id='table-dropdown',
        placeholder='Select available tables',
        multi=False
    ),
    html.Button('Submit', id='Table_submit_button'),
    dt.DataTable(
        # Initialise the rows
        rows=[{}],
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id='table'
        ),
    html.Div(id='selected-indexes'),
])    
 """   
@app.callback(
    dash.dependencies.Output('table-dropdown', 'options'),
    [dash.dependencies.Input('database-dropdown', 'value')])
def drop_table(dropdown_value): 
    if dropdown_value is None:
        pass
    else:
        return select_table(dropdown_value)

@app.callback(
    dash.dependencies.Output('table', 'rows'),
    [dash.dependencies.Input('Table_submit_button', 'n_clicks')],
    [dash.dependencies.State('table-dropdown', 'value'),
    dash.dependencies.State('database-dropdown', 'value')])
def show_table(n_clicks, table, db):    
    if table is None or db is None:
        pass
    else:
        return generate_table(table, db)

@app.callback(
    dash.dependencies.Output('table_2', 'rows'),
    [dash.dependencies.Input('Table_submit_button_2', 'n_clicks')], 
    [dash.dependencies.State('txt_box', 'value')])
def show_table_2(n_clicks, txt_box):
    return query(txt_box)


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == '__main__':
    app.run_server(debug=True)            