import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd
import pyrebase
from data import config
from dash import dash_table

firebase = pyrebase.initialize_app(config)
db = firebase.database()

retrieve_data = db.get()
df = pd.DataFrame.from_dict(retrieve_data.val(), orient='index')
df = df.reset_index()
df.rename(columns={'index': 'id'}, inplace=True)
df = df[['id', 'Date Time', 'First Name', 'Last Name', 'Date Of Birth',
         'Email', 'Address', 'Country', 'Mobile No']]

metaTags = [
    {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minium-scale=0.5'}]

app = dash.Dash(__name__, meta_tags=metaTags,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.CERULEAN]
                )
server = app.server

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.Img(src=app.get_asset_url('database.png'),
                         className='image'),
                html.Div('CRUD APP',
                         style={'line-height': '15px'},
                         className='title_text')
            ], className='title_row')
        ], className='title_background twelve columns')
    ], className='row'),

    html.Div(id='insert_user_data', children=[]),

    html.Div([
        html.Div([
            html.P(dcc.Markdown('''Insert user data using the below button in the **Google Firebase** Database.'''),
                   style={'margin-bottom': '-10px', 'color': 'black'}),
            dbc.Button("Add Data",
                       id="open-centered-user",
                       n_clicks=0,
                       class_name='text_size'),
        ], className='button_text'),
    ], className='modal_row'),

    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Add data using the below cells."),
                        close_button=True),
        dbc.ModalBody([
            html.Div([
                html.Div([
                    html.P('First name', style={'color': 'white'}),
                    dcc.Input(id='first_name',
                              placeholder='Type first name',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Last name', style={'color': 'white'}),
                    dcc.Input(id='last_name',
                              placeholder='Type last name',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Date of birth', style={'color': 'white'}),
                    dcc.Input(id='date_of_birth',
                              placeholder='dd/mm/yyyy',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Email', style={'color': 'white'}),
                    dcc.Input(id='email_address',
                              placeholder='Type email',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Address', style={'color': 'white'}),
                    dcc.Input(id='living_address',
                              placeholder='Type address',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Country name', style={'color': 'white'}),
                    dcc.Input(id='name_country',
                              placeholder='Type country name',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
                html.Div([
                    html.P('Mobile no.', style={'color': 'white'}),
                    dcc.Input(id='mobile_number',
                              placeholder='Type mobile number',
                              style={'margin-top': '-10px', 'color': 'black'})
                ], className='input_column'),
            ], className='input_row'),

            html.Div([
                dbc.Button('Submit Data',
                           id='insert_user_data_button',
                           n_clicks=0,
                           class_name='text_size')
            ], className='button_row'),
        ]),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close-centered-user",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal-centered-user",
        centered=True,
        is_open=False,
        size="xl"),

    html.Div([
        dbc.Modal([
            dbc.ModalBody("Data has been added. View the inserted data in the below table.",
                          style={'color': 'black'}),
            dbc.ModalFooter(
                dbc.Button("Close",
                           id="user_data_added_close",
                           className="ms-auto",
                           n_clicks=0
                           )
            ),
        ], id="user_data_added_modal",
            is_open=False
        )
    ]),

    html.Div([
        dbc.Spinner(html.Div([dash_table.DataTable(id='my_user_datatable',
                                                   columns=[{"name": i, "id": i} for i in df.columns],
                                                   page_size=13,
                                                   sort_action="native",
                                                   sort_mode="multi",
                                                   virtualization=True,
                                                   style_cell={'textAlign': 'left',
                                                               'min-width': '100px',
                                                               'backgroundColor': 'rgba(255, 255, 255, 0)',
                                                               'minWidth': 180,
                                                               'maxWidth': 180,
                                                               'width': 180},
                                                   style_header={
                                                       'backgroundColor': 'black',
                                                       'fontWeight': 'bold',
                                                       'font': 'Lato, sans-serif',
                                                       'color': 'orange',
                                                       'border': '1px solid white',
                                                   },
                                                   style_data={'textOverflow': 'hidden',
                                                               'color': 'black',
                                                               'fontWeight': 'bold',
                                                               'font': 'Lato, sans-serif'},
                                                   fixed_rows={'headers': True},
                                                   )
                              ], className='bg_table'), color='success')
    ], className='bg_container')

])


@app.callback(
    Output("modal-centered-user", "is_open"),
    [Input("open-centered-user", "n_clicks")],
    [Input("close-centered-user", "n_clicks")],
    [State("modal-centered-user", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("user_data_added_modal", "is_open"),
    [Input("insert_user_data_button", "n_clicks")],
    [Input("user_data_added_close", "n_clicks")],
    [State("user_data_added_modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(Output('insert_user_data', 'children'),
              Output('first_name', 'value'),
              Output('last_name', 'value'),
              Output('date_of_birth', 'value'),
              Output('email_address', 'value'),
              Output('living_address', 'value'),
              Output('name_country', 'value'),
              Output('mobile_number', 'value'),
              [Input('insert_user_data_button', 'n_clicks')],
              [State('first_name', 'value')],
              [State('last_name', 'value')],
              [State('date_of_birth', 'value')],
              [State('email_address', 'value')],
              [State('living_address', 'value')],
              [State('name_country', 'value')],
              [State('mobile_number', 'value')],
              prevent_initial_call=True)
def update_value(n_clicks, first_name, last_name, date_of_birth, email_address, living_address, name_country,
                 mobile_number):
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    firtsName = first_name
    lastName = last_name
    dateOfBirth = date_of_birth
    email = email_address
    livingAdddress = living_address
    countryName = name_country
    mobileNumber = mobile_number

    add_data = {'Date Time': dt_string,
                'First Name': firtsName,
                'Last Name': lastName,
                'Date Of Birth': dateOfBirth,
                'Email': email,
                'Address': livingAdddress,
                'Country': countryName,
                'Mobile No': mobileNumber}

    if n_clicks > 0:
        return [
            db.push(add_data)
        ], '', '', '', '', '', '', ''


@app.callback(Output('my_user_datatable', 'data'),
              [Input("user_data_added_close", "n_clicks")])
def display_table(n1):
    retrieve_data = db.get()
    df = pd.DataFrame.from_dict(retrieve_data.val(), orient='index')
    df = df.reset_index()
    df.rename(columns={'index': 'id'}, inplace=True)
    df = df[['id', 'Date Time', 'First Name', 'Last Name', 'Date Of Birth',
             'Email', 'Address', 'Country', 'Mobile No']]
    if n1 >= 0:
        return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
