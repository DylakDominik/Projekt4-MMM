import numpy as np
import matplotlib.pyplot as plt

# 1. Definicja parametrów (zgodnie z wymogami - można je zmieniać)
a1, a0 = 1.0, 2.0
b2, b1, b0 = 1.0, 3.0, 2.0

Kp, Ki = 5.0, 10.0  # Nastawy regulatora PI

# 2. Ustawienia symulacji (Metoda numeryczna)
dt = 0.01          # Krok całkowania (im mniejszy, tym dokładniej)
t_end = 10.0       # Czas trwania symulacji w sekundach
t = np.arange(0, t_end, dt) # Tablica czasu
N = len(t)         # Liczba próbek

# 3. Przygotowanie tablic na wyniki (wypełnione zerami - czyli nasze warunki początkowe!)
y = np.zeros(N)       # Wyjście układu
u_reg = np.zeros(N)   # Sygnał z regulatora (sterujący)
u_zad = np.ones(N)    # Sygnał zadany (na razie zwykły skok jednostkowy - prostokąt)

# Zmienne stanu dla metody numerycznej (pamięć z poprzedniego kroku)
x1 = 0.0
x2 = 0.0
calka_uchybu = 0.0

# 4. GŁÓWNA PĘTLA SYMULACYJNA (Metoda Eulera)
for k in range(1, N):
    
    # a) Odczytanie zadanej wartości w danej chwili
    zadane = u_zad[k]
    
    # b) Obliczenie błędu (uchybu)
    # Wyjście w tym kroku liczymy na podstawie obecnych stanów x1, x2
    obecne_y = a1 * x2 + a0 * x1
    y[k] = obecne_y
    
    e = zadane - obecne_y
    
    # c) Regulator PI (numeryczne całkowanie metodą prostokątów/Eulera)
    calka_uchybu = calka_uchybu + e * dt
    sterowanie = Kp * e + Ki * calka_uchybu
    u_reg[k] = sterowanie
    
    # d) Równania różniczkowe obiektu
    dx1 = x2
    dx2 = (1.0 / b2) * (sterowanie - b1 * x2 - b0 * x1)
    
    # e) Zaktualizowanie stanów na następny krok (Metoda Eulera)
    x1 = x1 + dx1 * dt
    x2 = x2 + dx2 * dt

# 5. Rysowanie prostego wykresu, żeby sprawdzić, czy działa
plt.figure(figsize=(10, 5))
plt.plot(t, u_zad, 'r--', label='Sygnał zadany')
plt.plot(t, y, 'b-', label='Odpowiedź układu (y)')
plt.title('Symulacja układu zamkniętego (Metoda Eulera)')
plt.xlabel('Czas [s]')
plt.ylabel('Wartość')
plt.legend()
plt.grid(True)
plt.show()