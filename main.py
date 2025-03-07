import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Функція для генерації гармоніки з шумом
def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    # Створюємо часовий вектор
    t = np.linspace(0, 1, 1000)
    # Генеруємо гармонічний сигнал
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    # Генеруємо шум
    noise = np.random.normal(noise_mean, noise_covariance, t.shape)
    # Повертаємо сигнал із шумом або без нього, залежно від вибору користувача
    return t, harmonic + noise if show_noise else harmonic

# Власний фільтр (простий ковзний середній)
def custom_filter(signal_data, window_size=5):
    # Згладжуємо сигнал за допомогою ковзного середнього
    return np.convolve(signal_data, np.ones(window_size)/window_size, mode='same')

# Ініціалізація Dash-додатку
app = dash.Dash(__name__)

# Початкові параметри
initial_params = {
    'amplitude': 1,
    'frequency': 5,
    'phase': 0,
    'noise_mean': 0,
    'noise_covariance': 0.1,
    'show_noise': True,
    'window_size': 5
}

# Макет інтерфейсу
app.layout = html.Div([
    html.H1("Harmonic Signal Generator"),  # Заголовок
    dcc.Graph(id='harmonic-plot'),  # Поле для графіка
    
    # Слайдери для керування параметрами гармоніки та шуму
    html.Label("Amplitude"),
    dcc.Slider(id='amplitude-slider', min=0, max=5, step=0.1, value=initial_params['amplitude']),
    
    html.Label("Frequency"),
    dcc.Slider(id='frequency-slider', min=1, max=20, step=0.1, value=initial_params['frequency']),
    
    html.Label("Phase"),
    dcc.Slider(id='phase-slider', min=-np.pi, max=np.pi, step=0.1, value=initial_params['phase']),
    
    html.Label("Noise Mean"),
    dcc.Slider(id='noise-mean-slider', min=-1, max=1, step=0.1, value=initial_params['noise_mean']),
    
    html.Label("Noise Covariance"),
    dcc.Slider(id='noise-covariance-slider', min=0, max=1, step=0.1, value=initial_params['noise_covariance']),
    
    # Чекбокс для перемикання шуму
    dcc.Checklist(id='show-noise', options=[{'label': 'Show Noise', 'value': 'show'}], value=['show']),
    
    html.Label("Filter Window Size"),
    dcc.Slider(id='window-size-slider', min=1, max=20, step=1, value=initial_params['window_size']),
    
    # Кнопка для скидання параметрів
    html.Button('Reset', id='reset-button', n_clicks=0)
])

# Колбек для оновлення графіка на основі вхідних параметрів
@app.callback(
    Output('harmonic-plot', 'figure'),
    [
        Input('amplitude-slider', 'value'),
        Input('frequency-slider', 'value'),
        Input('phase-slider', 'value'),
        Input('noise-mean-slider', 'value'),
        Input('noise-covariance-slider', 'value'),
        Input('show-noise', 'value'),
        Input('window-size-slider', 'value')
    ]
)
def update_plot(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, window_size):
    # Перевіряємо, чи потрібно показувати шум
    show_noise = 'show' in show_noise
    
    # Генеруємо сигнал
    t, noisy_signal = harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise)
    
    # Фільтруємо сигнал
    filtered_signal = custom_filter(noisy_signal, window_size)
    
    # Створюємо графік
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=noisy_signal, mode='lines', name='Noisy Signal'))  # Шумний сигнал
    fig.add_trace(go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal'))  # Відфільтрований сигнал
    
    # Оновлюємо заголовок і підписи осей
    fig.update_layout(title="Harmonic Signal with Noise and Filtering", xaxis_title="Time", yaxis_title="Amplitude")
    return fig

# Запуск додатку
if __name__ == '__main__':
    app.run_server(debug=True)
