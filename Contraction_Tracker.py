import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import time
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.logger import Logger

# Asegúrate de que los valores de color estén entre 0.0 y 1.0
BG_COLOR = (2.20/2.55, 2.38/2.55, 2.36/2.55, 0.8)
BUTTON_COLOR = (0.7, 0.94, 0.8, 1)

class Tracker(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Inicializamos todas las variables de estado en el constructor
        self.id_contraction = 1
        self.promedio = []
        self.start_time_total = None
        self.start_time_CTR = None
        self.timer_event_total = None
        self.timer_event_CTR = None
        self.elapsed_time_total = 0.0
        self.elapsed_time_CTR = 0.0
        self.time_limit = 5

    def build(self):
        Window.clearcolor = BG_COLOR
        
        self.root_layout = BoxLayout(orientation='vertical', padding=sp(25), spacing=sp(10))

        # Etiqueta para el temporizador total de la sesión
        self.leyend = Label(text='', font_size='22sp', color=(0,0,0,1), size_hint=(1,.5))
        
        
        # Etiqueta para el cronómetro de la contracción actual
        self.time_label = Label(text='00:00.00', font_size='50sp', color=(0,0,0,1), size_hint=(1,.8))
        self.root_layout.add_widget(self.time_label)
        self.root_layout.add_widget(self.leyend)
        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=sp(10), size_hint=(1,.5))

        self.start_button = Button(
            text='Inicio contracción',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1)
        )
        
        self.end_button = Button(
            text='Fin contracción',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1)
        )

        self.reset_button = Button(
            text='Reiniciar',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1)
        )

        self.start_button.bind(on_press=self.start_timer)
        self.end_button.bind(on_press=self.end_contraction)
        self.reset_button.bind(on_press=self.reset)

        self.buttons_layout.add_widget(self.start_button)
        self.buttons_layout.add_widget(self.end_button)
        self.buttons_layout.add_widget(self.reset_button)
        self.root_layout.add_widget(self.buttons_layout)
        
        
        self.grid = GridLayout(cols=2)
        self.root_layout.add_widget(self.grid)

        return self.root_layout

    def update_time(self, dt):
        """Actualiza los temporizadores de la sesión y la contracción."""
        if self.start_time_total:
            self.elapsed_time_total = time.time() - self.start_time_total

            if self.elapsed_time_total >= self.time_limit:
                Clock.unschedule(self.timer_event_total)
                self.timer_event_total = None
                if self.timer_event_CTR:
                    self.end_contraction(self)
                n=0
                suma=0
                for duration in self.promedio:
                    Logger.info(self.promedio[n])
                    if duration==0:
                        continue
                    n+=1
                    suma= duration+suma
                    prom = suma/n
                    minutes, seconds = divmod(prom, 60)
                    f_prom = f'{int(minutes):02d}:{int(seconds):02d}.{int(prom * 100 % 100):02d}'
                    self.leyend.text=('Promedio de duración de contracciones: '+f_prom+
                    '\nCantidad de contracciones: '+str(n))
                return

            minutes, seconds = divmod(self.elapsed_time_total, 60)
            time_string = f'{int(minutes):02d}:{int(seconds):02d}.{int(self.elapsed_time_total * 100 % 100):02d}'
            self.time_label.text = time_string
        
        if self.start_time_CTR:
            self.elapsed_time_CTR = time.time() - self.start_time_CTR
            minutes, seconds = divmod(self.elapsed_time_CTR, 60)
            time_string = f'{int(minutes):02d}:{int(seconds):02d}.{int(self.elapsed_time_CTR * 100 % 100):02d}'
            self.leyend.text = f'Contracción {self.id_contraction}: {time_string}'

    def start_timer(self, instance):
        """Inicia el temporizador general y el de la contracción."""
        if self.timer_event_CTR:
            # Ya hay una contracción en curso, no hacer nada.
            return
            
        # Si es la primera contracción, inicia el temporizador total de la sesión
        if not self.timer_event_total:
            self.reset(self)
            self.start_time_total = time.time()
            self.timer_event_total = Clock.schedule_interval(self.update_time, 0.01)

        # Inicia el cronómetro de la contracción
        self.start_time_CTR = time.time()
        self.timer_event_CTR = Clock.schedule_interval(self.update_time, 0.01)

    def end_contraction(self, instance):
        """Finaliza la contracción, guarda su duración y actualiza la UI."""
        if not self.timer_event_CTR:
            # No hay ninguna contracción en curso
            return

        # Detiene el temporizador de la contracción
        Clock.unschedule(self.timer_event_CTR)
        self.timer_event_CTR = None

        # Guarda la duración de la contracción
        duration = time.time() - self.start_time_CTR
        self.promedio.append(duration)

        # Formatea la duración para mostrarla
        minutes, seconds = divmod(duration, 60)
        time_string = f'{int(minutes):02d}:{int(seconds):02d}.{int(duration * 100 % 100):02d}'

        # Agrega las etiquetas de la nueva contracción en la cuadrícula
        self.con_label = Label(text=f'Contracción {self.id_contraction}', font_size='20sp', color=(0,0,0,1))
        self.time_label_n = Label(text=f'Duración: {time_string}', font_size='20sp', color=(0,0,0,1))
        self.grid.add_widget(self.con_label)
        self.grid.add_widget(self.time_label_n)

        # Prepara la siguiente contracción
        self.id_contraction += 1
        self.start_time_CTR = None
        self.elapsed_time_CTR = 0.0
        self.time_label.text = '00:00.00'
        self.leyend.text=''

    def reset(self, instance):
        """Reinicia el estado de la aplicación sin cerrarla."""
        # Detiene todos los temporizadores
        if self.timer_event_total:
            Clock.unschedule(self.timer_event_total)
            self.timer_event_total = None
        if self.timer_event_CTR:
            Clock.unschedule(self.timer_event_CTR)
            self.timer_event_CTR = None

        # Reinicia las variables de estado
        self.id_contraction = 1
        self.promedio = []
        self.start_time_total = None
        self.start_time_CTR = None
        self.elapsed_time_total = 0.0
        self.elapsed_time_CTR = 0.0

        # Reinicia la UI
        self.grid.clear_widgets()
        self.time_label.text = '00:00.00'
        self.leyend.text = ''
        
if __name__ == '__main__':
    Tracker().run()
