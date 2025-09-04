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
from kivy.utils import get_color_from_hex as getHex

# Asegúrate de que los valores de color estén entre 0.0 y 1.0
BG_COLOR = (231/255, 240/255, 249/255, 0.1)
BUTTON_COLOR = (159/255, 197/255, 232/255, 0.5)

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
        self.time_limit = 600

    def build(self):
        Window.clearcolor = BG_COLOR
        
        self.root_layout = BoxLayout(orientation='vertical', padding=sp(25), spacing=sp(10))
        
        # Etiqueta para el cronómetro de la contracción actual
        self.time_label = Label(text='00:00.00', font_size='50sp', color=(0,0,0,1), size_hint=(1,.15))
        self.time_label.bind(size=self.set_size)
        self.root_layout.add_widget(self.time_label)

        # Etiqueta para el temporizador total de la sesión
        self.leyend = Label(text='', font_size='22sp', color=(0,0,0,1), size_hint=(1,.1))
        self.leyend.bind(size=self.set_size)
        self.root_layout.add_widget(self.leyend)

        # Botones
        self.buttons_layout = BoxLayout(orientation='horizontal', spacing=sp(10), size_hint=(1,.1))
        self.start_button = Button(
            text='Inicio',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        
        self.end_button = Button(
            text='Fin',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )

        self.reset_button = Button(
            text='Reiniciar',
            size_hint=(.7, .8),
            font_size=sp(22),
            background_color=BUTTON_COLOR,
            color=(0,0,0,1),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )

        self.start_button.bind(on_press=self.start_timer)
        self.end_button.bind(on_press=self.end_contraction)
        self.reset_button.bind(on_press=self.reset)
        self.start_button.bind(size=self.set_size)
        self.end_button.bind(size=self.set_size)
        self.reset_button.bind(size=self.set_size)

        self.buttons_layout.add_widget(self.start_button)
        self.buttons_layout.add_widget(self.end_button)
        self.buttons_layout.add_widget(self.reset_button)
        self.root_layout.add_widget(self.buttons_layout)
        
        
        self.grid = GridLayout(cols=2, spacing=sp(5), size_hint=(1,.60))
        self.root_layout.add_widget(self.grid)

        self.tqm = Label(text='Para la mejor doctora. Te amito <3', font_size='10sp', color=(0,0,0,0.5), size_hint=(1,.1))
        self.root_layout.add_widget(self.tqm)

        return self.root_layout

    def set_size(self, instance, value):
        """Ajusta el tamaño del texto para que se ajuste al botón."""
        # Establece el tamaño del texto con un ancho fijo (el del botón) y una altura ilimitada
        instance.text_size = (instance.width, None)
        instance.valign = 'middle'
        instance.halign = 'center'

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
        self.time_label_n = Label(text=f'{time_string}', font_size='20sp', color=(0,0,0,1))
        self.con_label.bind(size=self.set_size)
        self.time_label_n.bind(size=self.set_size)
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
