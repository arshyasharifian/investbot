import robin_stocks as rs
import numpy as np
from datetime import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

with open('robinhood_config.txt', 'r') as f:
    file = f.read().split('\n')

f.close()
username = file[0]
password = file[1]
valid_code = file[2]

username = username.split(' ')[1]
password = password.split(' ')[1]
valid_code = valid_code.split(' ')[1]

login = rs.login(username, password)
min_time = datetime(datetime.today().year,
                    datetime.today().month,
                    datetime.today().day,
                    0, 0, 0)

max_time = datetime(datetime.today().year,
                    datetime.today().month,
                    datetime.today().day,
                    21, 0, 0)
p_list = []
t_list = []

stocks_list = ['aapl', 'tsla', 'msft']


def get_latest_buyPower(stocks_list):
    principle = float(rs.profiles.load_account_profile()['buying_power'])
    stock_price_list = rs.stocks.get_latest_price(stocks_list)
    for stock in stock_price_list:
        principle += float(stock)

    return principle, datetime.now()


# Initiating a dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div([
        html.H5('Live Graph Testing'),
    ], className='row'),
    html.Div([
        dcc.Graph(id='live_graph', animate=True),
        dcc.Interval(id='interval_component', interval=20*1000, n_intervals=0)  # interval = 20 sec
    ])
])


@app.callback(Output('live_graph', 'figure'),
              [Input('interval_component', 'n_intervals')])
def update_graph(n):
    global stocks_list
    global min_time
    global max_time
    global p_list
    global t_list

    principle, current_time = get_latest_buyPower(stocks_list)
    principle += np.random.rand()

    p_list.append(principle)
    t_list.append(current_time)

    trace = go.Scatter(x=t_list,
                       y=p_list,
                       name='random plot',
                       mode='lines+markers')

    layout = go.Layout(xaxis=dict(range=[min_time, max_time])
                       )
    fig = {'data': [trace],
           'layout': layout
           }

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
