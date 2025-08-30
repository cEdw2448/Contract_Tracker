import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import time

id_contraction = 0
promedio = []

kivy.require('2.3.1') # Especifica una versión de Kivy si es necesario

class StopwatchApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=20)

        self.time_label = Label(text='00:00:00.00', font_size='50sp')
        self.root_layout.add_widget(self.time_label)

        self.buttons_layout = BoxLayout(spacing=10)
        self.start_button = Button(text='Inicio contracción')
        self.end_button = Button(text='Fin contracción')
        self.reset_button = Button(text='Reiniciar')

        self.start_button.bind(on_press=self.start_timer)
        self.end_button.bind(on_press=self.end_contraction)
        self.reset_button.bind(on_press=self.reset_timer)

        self.buttons_layout.add_widget(self.start_button)
        self.buttons_layout.add_widget(self.end_button)
        self.buttons_layout.add_widget(self.reset_button)
        self.root_layout.add_widget(self.buttons_layout)

        self.start_time = None
        self.elapsed_time = 0.0
        self.timer_event = None

        return self.root_layout
    
    def new_contraction(self):
        global id_contraction, promedio
        id_contraction = id_contraction + 1
        promedio.append(self.elapsed_time)

        self.time_label = Label(text="Contraction "+str(id_contraction//2), font_size='50sp')
        self.root_layout.add_widget(self.time_label)
        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.timer_event = None
        return self.root_layout

    def update_time(self, dt):
        """Actualiza el temporizador y la etiqueta."""
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
        else:
            # Si el cronómetro no se ha iniciado, mantiene el tiempo cero
            self.elapsed_time = 0.0

        # Formatear el tiempo
        minutes, seconds = divmod(self.elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        time_string = f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(self.elapsed_time * 100 % 100):02d}'
        self.time_label.text = time_string

    def start_timer(self, instance):
        """Inicia o reanuda el cronómetro."""
        if self.timer_event is None: # Solo inicia si no está ya corriendo
            time.time()
            self.new_contraction()
            self.start_time = time.time() # Restaura el tiempo si se había pausado
            self.timer_event = Clock.schedule_interval(self.update_time, 0.01) # Actualiza cada 0.01 segundos

    def end_contraction(self, instance):
        """Pausa el cronómetro."""
        if self.timer_event:
            Clock.unschedule(self.timer_event) # Cancela la llamada programada
            # Mantenemos slf.start_time en None para que la siguiente actualización se base en self.elapsed_time
            self.new_contraction()

    def reset_timer(self, instance):
        """Reinicia el cronómetro a cero."""
        self.update_time(None) # Actualiza la etiqueta a 00:00:00.00

if __name__ == '__main__':
    StopwatchApp().run()