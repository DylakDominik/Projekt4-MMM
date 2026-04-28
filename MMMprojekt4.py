import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# 1. Ustawienia czasu symulacji
dt = 0.01
t_end = 15.0
t = np.arange(0, t_end, dt)
N = len(t)

# 2. Inicjalizacja wykresu i zrobienie miejsca na interfejs na dole
fig, ax = plt.subplots(figsize=(10, 7))
# TA LINIA JEST KLUCZOWA DLA BRAKU NACHODZENIA
plt.subplots_adjust(left=0.1, bottom=0.45) # Zostawiamy 45% miejsca na dole okna

# Puste linie, które będziemy aktualizować
line_zad, = ax.plot(t, np.zeros(N), 'r--', label='Sygnał zadany')
line_y, = ax.plot(t, np.zeros(N), 'b-', label='Odpowiedź układu (y)')
ax.set_title('Symulator Układu Zamkniętego z regulatorem PI')
ax.set_xlabel('Czas [s]')
ax.set_ylabel('Wartość')
ax.legend(loc='upper right')
ax.grid(True)
ax.set_ylim(-2.5, 2.5) # Sztywna oś Y, żeby wykres nie skakał przy zmianach

# 3. Definicja miejsc w oknie na nasze suwaki i przyciski [lewo, dół, szerokość, wysokość]
ax_typ = plt.axes([0.1, 0.25, 0.15, 0.15])
ax_Kp = plt.axes([0.35, 0.35, 0.5, 0.03])
ax_Ki = plt.axes([0.35, 0.30, 0.5, 0.03])

ax_a1 = plt.axes([0.1, 0.15, 0.35, 0.03])
ax_a0 = plt.axes([0.1, 0.10, 0.35, 0.03])

ax_b2 = plt.axes([0.55, 0.20, 0.35, 0.03])
ax_b1 = plt.axes([0.55, 0.15, 0.35, 0.03])
ax_b0 = plt.axes([0.55, 0.10, 0.35, 0.03])

# 4. Tworzenie kontrolek GUI
radio_typ = RadioButtons(ax_typ, ('Prostokąt', 'Sinusoida', 'Trójkąt'))

slider_Kp = Slider(ax_Kp, 'Kp (Reg)', 0.1, 20.0, valinit=5.0)
slider_Ki = Slider(ax_Ki, 'Ki (Reg)', 0.0, 20.0, valinit=10.0)

slider_a1 = Slider(ax_a1, 'a1 (Licznik)', -5.0, 5.0, valinit=1.0)
slider_a0 = Slider(ax_a0, 'a0 (Licznik)', -5.0, 5.0, valinit=2.0)

# Współczynnik b2 (przy najwyższej potędze mianownika) nie może być zerem!
slider_b2 = Slider(ax_b2, 'b2 (Mianownik)', 0.1, 5.0, valinit=1.0) 
slider_b1 = Slider(ax_b1, 'b1 (Mianownik)', 0.1, 10.0, valinit=3.0)
slider_b0 = Slider(ax_b0, 'b0 (Mianownik)', 0.1, 10.0, valinit=2.0)

# 5. GŁÓWNA FUNKCJA OBLICZENIOWA (Uruchamiana przy każdym ruchu suwaka)
def aktualizuj(val):
    # a) Pobieranie aktualnych wartości z suwaków
    Kp, Ki = slider_Kp.val, slider_Ki.val
    a1, a0 = slider_a1.val, slider_a0.val
    b2, b1, b0 = slider_b2.val, slider_b1.val, slider_b0.val
    typ_sygnalu = radio_typ.value_selected
    
    # b) Generowanie odpowiedniego sygnału
    u_zad = np.zeros(N)
    amp = 1.0
    freq = 0.2
    
    if typ_sygnalu == 'Prostokąt':
        u_zad[(t >= 1.0) & (t <= 8.0)] = amp
    elif typ_sygnalu == 'Sinusoida':
        u_zad = amp * np.sin(2 * np.pi * freq * t)
    elif typ_sygnalu == 'Trójkąt':
        u_zad = amp * signal.sawtooth(2 * np.pi * freq * t, 0.5)
        
    # c) Symulacja Metodą Eulera od zera dla nowych parametrów
    y = np.zeros(N)
    x1, x2, calka_uchybu = 0.0, 0.0, 0.0
    
    for k in range(1, N):
        zadane = u_zad[k]
        obecne_y = a1 * x2 + a0 * x1
        y[k] = obecne_y
        e = zadane - obecne_y
        
        calka_uchybu += e * dt
        sterowanie = Kp * e + Ki * calka_uchybu
        
        dx1 = x2
        dx2 = (1.0 / b2) * (sterowanie - b1 * x2 - b0 * x1)
        
        x1 += dx1 * dt
        x2 += dx2 * dt
        
    # d) Aktualizacja samych linii na istniejącym wykresie
    line_zad.set_ydata(u_zad)
    line_y.set_ydata(y)
    fig.canvas.draw_idle()

# 6. Reakcja na kliknięcia (podpięcie funkcji do akcji)
radio_typ.on_clicked(aktualizuj)
slider_Kp.on_changed(aktualizuj)
slider_Ki.on_changed(aktualizuj)
slider_a1.on_changed(aktualizuj)
slider_a0.on_changed(aktualizuj)
slider_b2.on_changed(aktualizuj)
slider_b1.on_changed(aktualizuj)
slider_b0.on_changed(aktualizuj)

# Wymuszenie pierwszego obliczenia zaraz po uruchomieniu programu
aktualizuj(0)

# Wyświetlenie okna
plt.show()