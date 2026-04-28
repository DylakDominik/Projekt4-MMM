import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# 1. Definicja parametrów obiektu i regulatora
a1, a0 = 1.0, 2.0
b2, b1, b0 = 1.0, 3.0, 2.0
Kp, Ki = 5.0, 10.0

# 2. Ustawienia symulacji czasu
dt = 0.01          
t_end = 15.0       # Wydłużamy czas do 15 sekund, żeby lepiej widzieć fale
t = np.arange(0, t_end, dt) 
N = len(t)         

# 3. GENEROWANIE SYGNAŁÓW WEJŚCIOWYCH (u_zad)
# Odkomentuj (usuń znak #) przed sygnałem, który chcesz przetestować, 
# a zakomentuj (dodaj #) pozostałe.

amp = 1.0  # Amplituda sygnału
freq = 0.2 # Częstotliwość (dla sinusa i trójkąta)

# Opcja A: Prostokątny o skończonym czasie trwania (np. od 1 do 8 sekundy)
#u_zad = np.zeros(N)
#u_zad[(t >= 1.0) & (t <= 8.0)] = amp

# Opcja B: Harmoniczny (Sinusoida)
#u_zad = amp * np.sin(2 * np.pi * freq * t)

# Opcja C: Trójkątny (korzystamy z funkcji sawtooth z biblioteki scipy)
u_zad = amp * signal.sawtooth(2 * np.pi * freq * t, 0.5)

# 4. Przygotowanie tablic i warunków początkowych
y = np.zeros(N)       
u_reg = np.zeros(N)   
x1 = 0.0
x2 = 0.0
calka_uchybu = 0.0

# 5. GŁÓWNA PĘTLA SYMULACYJNA
for k in range(1, N):
    zadane = u_zad[k]
    
    obecne_y = a1 * x2 + a0 * x1
    y[k] = obecne_y
    e = zadane - obecne_y
    
    calka_uchybu = calka_uchybu + e * dt
    sterowanie = Kp * e + Ki * calka_uchybu
    u_reg[k] = sterowanie
    
    dx1 = x2
    dx2 = (1.0 / b2) * (sterowanie - b1 * x2 - b0 * x1)
    
    x1 = x1 + dx1 * dt
    x2 = x2 + dx2 * dt

# 6. Rysowanie wykresu
plt.figure(figsize=(10, 5))
plt.plot(t, u_zad, 'r--', label='Sygnał zadany (wymuszenie)')
plt.plot(t, y, 'b-', label='Odpowiedź układu (y)')
plt.title('Symulacja układu: Reakcja na różne wymuszenia')
plt.xlabel('Czas [s]')
plt.ylabel('Wartość')
plt.legend()
plt.grid(True)
plt.show()