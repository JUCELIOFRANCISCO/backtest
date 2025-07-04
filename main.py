from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import pytz
import time
import threading

class BacktestApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.email_input = TextInput(hint_text="E-mail", multiline=False)
        self.password_input = TextInput(hint_text="Senha", multiline=False, password=True)
        self.pair_input = TextInput(hint_text="Par OTC (ex: EURUSD-OTC)", multiline=False)
        self.direction_input = TextInput(hint_text="Direção (CALL ou PUT)", multiline=False)
        self.time_input = TextInput(hint_text="Horário (HH:MM)", multiline=False)
        self.days_input = TextInput(hint_text="Dias de análise", multiline=False)
        self.output_label = Label(text="")

        self.start_button = Button(text="Executar Backtest")
        self.start_button.bind(on_press=self.start_backtest)

        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.pair_input)
        self.layout.add_widget(self.direction_input)
        self.layout.add_widget(self.time_input)
        self.layout.add_widget(self.days_input)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.output_label)
        return self.layout

    def start_backtest(self, instance):
        threading.Thread(target=self.execute_backtest).start()

    def execute_backtest(self):
        email = self.email_input.text.strip()
        senha = self.password_input.text.strip()
        par = self.pair_input.text.strip()
        direcao = self.direction_input.text.strip().lower()
        horario = self.time_input.text.strip()
        dias = int(self.days_input.text.strip())

        try:
            iq = IQ_Option(email, senha)
            iq.connect()
            iq.change_balance("PRACTICE")
            if not iq.check_connect():
                self.output_label.text = "Erro ao conectar."
                return

            timezone = pytz.timezone("America/Sao_Paulo")
            hoje = datetime.now(timezone).date()
            resultados = []

            for dias_atras in range(1, dias + 1):
                data = hoje - timedelta(days=dias_atras)
                hora, minuto = map(int, horario.split(":"))
                dt_local = timezone.localize(datetime(data.year, data.month, data.day, hora, minuto))
                dt_utc = dt_local.astimezone(pytz.utc)

                timestamp = int(dt_utc.timestamp())
                candles = iq.get_candles(par, 60, 1, timestamp)
                if candles:
                    candle = candles[0]
                    open_price = round(candle["open"], 5)
                    close_price = round(candle["close"], 5)
                    if open_price == close_price:
                        resultado = "DOJI"
                    elif close_price > open_price and direcao == "call":
                        resultado = "WIN"
                    elif close_price < open_price and direcao == "put":
                        resultado = "WIN"
                    else:
                        resultado = "LOSS"
                    resultados.append(f"{data.isoformat()} - {resultado}")
                else:
                    resultados.append(f"{data.isoformat()} - SEM DADOS")
                time.sleep(1)

            self.output_label.text = "\n".join(resultados)
        except Exception as e:
            self.output_label.text = f"Erro: {str(e)}"

if __name__ == "__main__":
    BacktestApp().run()
