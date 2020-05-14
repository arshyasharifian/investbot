import numpy as np
import pandas as pd
from datetime import datetime, date
import yahoofinancials
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

app_colors = {
    'background': '#111111',
    'text': '#FFFFFF'}


def get_stock(input_stock, start_date, end_date):
    start = start_date
    end = end_date

    stock = yahoofinancials.YahooFinancials(input_stock).get_historical_price_data(start, end, 'daily')
    df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

    for i in range(len(stock[input_stock]['prices'])):
        date = datetime.strptime(stock[input_stock]['prices'][i]['formatted_date'], '%Y-%m-%d')
        df.loc[date] = [stock[input_stock]['prices'][i]['open'],
                        stock[input_stock]['prices'][i]['high'],
                        stock[input_stock]['prices'][i]['low'],
                        stock[input_stock]['prices'][i]['close'],
                        stock[input_stock]['prices'][i]['volume']]

    return df


# Initiating a dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Specifying the layout of app
app.layout = html.Div(children=[
    # title of the webpage
    html.Div(children=[
        html.H1('Stock dashboard', className='four columns', style={'display': 'block'})], className='row'),

    html.Div([
        html.P('Stock Ticker ', className='one column', style={'display': 'inline'}),
        dcc.Input(
            id='stock_ticker',
            type='text',
            className='one column',
            style={'width': '10%'}),
        html.Button(id='click_button', n_clicks=0, children='submit', style={'display': 'inline'})
    ], className='row'),

    html.Div(children=[
        html.P('Chart Type', className='one column', style={'display': 'inline'}),
        dcc.RadioItems(id='chart-style',
                       options=[
                           {'label': 'Candle stick', 'value': 1},
                           {'label': 'Line', 'value': 2},
                           {'label': 'Open-high-low-close chart', 'value': 3}
                       ],
                       value=1,
                       className='three columns',
                       style={'display': 'inline-block'}),

        html.P('Calculation', className='one column', style={'display': 'inline'}),

        dcc.Checklist(id='calculation',
                      options=[
                          {'label': '5 day moving average', 'value': 'mv'}
                      ],
                      value=[],
                      className='two columns',
                      style={'display': 'block'})
    ], className='row'),

    html.Div(children=[
        # output chart
        html.Div(id='output_graph',
                 className='seven columns', style={'width': '1000px', 'height': '100px', 'display': 'inline-block'}),
        html.Div(id='output_news',
                 className='five columns', style={'width': '500px', "height": "300px",
                                                  "overflowY": "scroll", 'float': 'right', 'display': 'inline-block'})
    ], className='row')

], style={'margin-top': '-10px', 'height': '1000px'}, )


# Function to generate the chart
@app.callback(
    Output(component_id='output_graph', component_property='children'),
    [Input(component_id='chart-style', component_property='value'),
     Input(component_id='calculation', component_property='value'),
     Input(component_id='click_button', component_property='n_clicks')],
    [State(component_id='stock_ticker', component_property='value')]
)
def generate_chart(style, calculation, n_clicks, input_stock):
    start_date = str(date.today().year - 5) + '-' + str(date.today().month) + '-' + str(date.today().day)
    end_date = str(date.today())

    df = get_stock(input_stock, start_date, end_date)
    data = []
    if style == 1:
        data_trace = go.Candlestick(x=df.index,
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'],
                                    name=input_stock
                                    )
    if style == 2:
        data_trace = go.Scatter(x=df.index,
                                y=df['Close'],
                                name=input_stock
                                )
    if style == 3:
        data_trace = go.Ohlc(x=df.index,
                             open=df['Open'],
                             high=df['High'],
                             low=df['Low'],
                             close=df['Close'],
                             name=input_stock
                             )

    if calculation == 'mv':
        mv_trace = go.Scatter(x=df.index,
                              y=df['Close'].rolling(5).mean(),
                              name='moving average',
                              line={"color": "#f4d44d"})
        data.append(mv_trace)

    data.append(data_trace)

    layout = dict(
        title='{} historical data'.format(input_stock),
        xaxis=dict(
            rangeselector=dict(buttons=list([
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(count=5,
                     label="5d",
                     step="day",
                     stepmode="backward"),
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])),
            rangeslider=dict(visible=True),
            type="date")
    )
    return dcc.Graph(id='stock_graph',
                     figure={"data": data,
                             "layout": layout
                             }
                     )


@app.callback(
    Output(component_id='output_news', component_property='children'),
    [Input(component_id='click_button', component_property='n_clicks')],
    [State(component_id='stock_ticker', component_property='value')])
def generate_table(n_clicks, input_stock):
    # stock_news = rs.stocks.get_news(input_stock)
    with open('news.json', 'r') as f:
        stock_news = json.loads(f.read())

    table = html.Table(
        [
            html.Tr([
                html.Th('Latest News for {}'.format(input_stock))
            ])
        ]
        +
        [
            html.Tr([
                html.Td([
                    html.A(stock_news[i]['title'],
                           href=stock_news[i]["url"],
                           target="_blank")
                ])
            ]) for i in range(0, 6)
        ]

    )
    return table


if __name__ == "__main__":
    app.run_server(debug=True)
