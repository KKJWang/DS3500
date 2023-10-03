import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from collections import Counter
import random

from Human_vs_Human_dash import TicTacToe
from play_ai_vs_ai_benchmark import run_benchmark_games
from strategy import create_ai
from strategy import create_random_valid_strategy

# Tic Tac Toe game code
game = TicTacToe()
# Define initial values for stats and duration
stats = Counter()
duration = 0
# Define the Dash app

def reset_game():
    global game
    game = TicTacToe()

def get_board():
    board = []
    for i in range(3):
        row = []
        for j in range(3):
            position = i*3 + j
            cell = html.Button(
                id=f'cell-{position}',
                className='cell',
                n_clicks=0,
                disabled=game.board[position] != ' ',
                children=game.board[position]
            )
            row.append(cell)
        board.append(html.Div(row, className='board-row'))
    return board

# Benchmark code
stats = Counter()
duration = 0

app = dash.Dash(__name__)
app.title = 'Tic Tac Toe'

app.layout = html.Div([
    html.Div([
        html.H1('Tic Tac Toe Game'),
        html.P('This is a human vs human game!'),
        html.P('Click on a cell to make your move. "X" is first'),
        html.Div(get_board(), className='board'),
        html.Div(id='message', className='message'),
        html.Button('Refresh Game', id='refresh-button', n_clicks=0),
        html.H4('After clicking Refresh Game button, click at a new cell to refresh'),
    ], style={'text-align': 'center', 'margin-bottom': '50px'}),
    html.Div([
        html.H1('Tic Tac Toe'),
        html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Tic_tac_toe.svg/1024px-Tic_tac_toe.svg.png', style={'height': '300px', 'width': '300px'})
    ], style={'text-align': 'center', 'margin-bottom': '50px'}),
    html.Div([
        html.H1(children=f'Tic Tac Toe Benchmark Results'),
        html.Div(id='duration', children='Click "Run Benchmark" to see results. It will refresh every time you click it!'),
        dcc.Graph(id='example-graph', figure=go.Figure()),
        html.Button('Run Benchmark', id='run-benchmark-button', n_clicks=0)
    ])
])

# Tic Tac Toe game callbacks
@app.callback(
    [Output('cell-0', 'children'),
     Output('cell-1', 'children'),
     Output('cell-2', 'children'),
     Output('cell-3', 'children'),
     Output('cell-4', 'children'),
     Output('cell-5', 'children'),
     Output('cell-6', 'children'),
     Output('cell-7', 'children'),
     Output('cell-8', 'children'),
     Output('message', 'children')],
    [Input('cell-0', 'n_clicks'),
     Input('cell-1', 'n_clicks'),
     Input('cell-2', 'n_clicks'),
     Input('cell-3', 'n_clicks'),
     Input('cell-4', 'n_clicks'),
     Input('cell-5', 'n_clicks'),
     Input('cell-6', 'n_clicks'),
     Input('cell-7', 'n_clicks'),
     Input('cell-8', 'n_clicks'),
     Input('refresh-button', 'n_clicks')]
)
def make_move(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [' ']*9 + ['']
    triggered_element = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_element == 'refresh-button':
        return dash.no_update
    position = int(triggered_element.split('-')[1])
    game.make_move(position)
    if game.winner:
        message = f'{game.winner} wins!'
        reset_game()
    elif game.game_over():
        message = 'Tie game.'
        reset_game()
    else:
        message = f"{game.player}'s turn"
    return game.board + [message]


@app.callback(
    Output('refresh-button', 'n_clicks'),
    Input('refresh-button', 'n_clicks')
)

def refresh_game(n_clicks):
    if n_clicks > 0:
        reset_game()
        return 0
    return n_clicks
@app.callback(
    Output('example-graph', 'figure'),
    Input('run-benchmark-button', 'n_clicks')
)
def update_on_click(n_clicks):
    if n_clicks:
        p1 = create_ai(create_random_valid_strategy(uniform=True))
        p2 = create_ai(create_random_valid_strategy(uniform=True))
        return update_graph(p1, p2)
    else:
        return {'data': [], 'layout': {}}

def update_graph(p1, p2):
    stats, duration = run_benchmark_games(p1, p2)
    data = [go.Bar(
        x=['X wins', 'O wins', 'Draw'],
        y=[stats['X'], stats['O'], stats['DRAW']],
        marker={'color': f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'}
    )]
    layout = go.Layout(title=f'Tic Tac Toe Results (N = {sum(stats.values())})', xaxis_title='Results', yaxis_title='Count')

    return {'data': data, 'layout': layout}


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
