import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import time
from kivy.logger import Logger

id_contraction = 0
promedio = []

kivy.require('2.3.1') # Especifica una versión de Kivy si es necesario

class StopwatchApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=20)

        self.time_label = Label(text='00:00.00', font_size='50sp')
        self.root_layout.add_widget(self.time_label)

        self.buttons_layout = BoxLayout(spacing=10)
        self.start_button = Button(text='Inicio contracción')
        self.end_button = Button(text='Fin contracción')
        self.reset_button = Button(text='Reiniciar')

        self.start_button.bind(on_press=self.start_timer)
        self.end_button.bind(on_press=self.end_contraction)
        self.reset_button.bind(on_press=self.reset)

        self.buttons_layout.add_widget(self.start_button)
        self.buttons_layout.add_widget(self.end_button)
        self.buttons_layout.add_widget(self.reset_button)
        self.root_layout.add_widget(self.buttons_layout)

        self.remaining_time=0.0
        self.start_time = None
        self.elapsed_time = 0.0
        self.timer_event1 = None

        return self.root_layout
    
    def new_contraction(self):
        global id_contraction, promedio
        id_contraction = id_contraction + 1
        i=id_contraction//2
        promedio.insert(i,self.elapsed_time)

        self.time_label_n = Label(text="Contraction "+str(i), font_size='50sp')
        self.root_layout.add_widget(self.time_label_n)
        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.timer_event = None
        return self.root_layout

    def update_time(self, dt,id_clock):
        """Actualiza el temporizador y la etiqueta."""
        #while self.remaining_time <=10:
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            
        if self.start_time1:
            self.remaining_time = time.time() - self.start_time1
            
        if id_clock==1:
        # Formatear el tiempo
            minutes, seconds = divmod(self.remaining_time, 60)
            time_string = f'{int(minutes):02d}:{int(seconds):02d}.{int(self.remaining_time * 100 % 100):02d}'
            self.time_label.text = time_string
            
        if id_clock==2:
            # Formatear el tiempo
            minutes, seconds = divmod(self.elapsed_time, 60)
            time_string = f'{int(minutes):02d}:{int(seconds):02d}.{int(self.elapsed_time * 100 % 100):02d}'
            self.time_label_n.text = time_string
        #else:
         #   for i in promedio:
          #      n=n+1
           #     suma=i+suma
            #prom=suma/n
            #Logger.info(prom)
            #time.sleep(5)
            
    def start_timer(self, instance):
        """Inicia o reanuda el cronómetro."""
        
        self.timer_event1 = Clock.schedule_interval(lambda dt: self.update_time(dt,1), 0.01) # Actualiza cada 0.01 segundos
        self.start_time1=time.time()-self.remaining_time

        self.new_contraction()         
        self.start_time = time.time() # Restaura el tiempo si se había pausado
        self.timer_event = Clock.schedule_interval(lambda dt: self.update_time(dt,2), 0.01) # Actualiza cada 0.01 segundos     

    def end_contraction(self, instance):
        """Pausa el cronómetro."""
        if self.timer_event:
            Clock.unschedule(self.timer_event) # Cancela la llamada programada
            # Mantenemos slf.start_time en None para que la siguiente actualización se base en self.elapsed_time
            self.new_contraction()

    def reset(self, instance):
        """Reinicia el cronómetro a cero."""
        self.remaining_time,self.start_time1=0,0
        self.root.clear_widgets()
        self.stop()
        self.__init__()
        self.run()

if __name__ == '__main__':
    StopwatchApp().run()