from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Laser-Induced Temperature Calculation In Tissue. To będzie super projekt!!!', style={'textAlign':'center'}),
])

if __name__ == '__main__':
    app.run(debug=True)