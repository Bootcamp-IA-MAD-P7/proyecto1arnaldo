import time #con esto importo la funcionalidad/libreria de python que me permite trabajar con el tiempo

import logging

logging.basicConfig(
    filename="taximeter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def calculate_fare(seconds_stopped, seconds_moving): # remember to keep identation
    """
    calcular la tarifa total en euros. 
    - Stopped: 0.02 €/s
    - Moving 0.05 €/s
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05 #esto calcula el precio total
    logging.info(
        f"Fare calculated: €{fare:.2f}"
     )
    return fare

def taximeter():
    """
    funcion para manejar y mostrar las opciones del taximetro
    """
    print("Welcome to the F5 Taximeter!")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n")

    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None # 'stopped' o 'moving'
    state_start_time = 0

    while True: #preguntar Alexandra, IA indica que puede ser command = input(" ").strip().lower() sin el >, es decir el > solo ¿es para visualmente identificar donde se debe escribir? ¿sin significado logico? solo visual?
        command = input("> ").strip().lower() #esto indica que se debe escribir algo input("") sin espacios .strip() y en minusculas .lower()

        if command == "start":
            if trip_active:
                logging.warning(
                    "Attempt to start while trip already active."
                )    
                print("Error: A trip is already in progress.")
                continue
            trip_active = True
            logging.info("Trip started.")
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            print("Trip started. Initial state: 'stopped'.")

        elif command in ("stop", "move"):
            if not trip_active:
                print("Error: No active trip. Please start first.")
                continue
            # en la siguiente linea se calcula el tiempo del estado anterior 
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration # += forma corta de decir // stopped_time = stopped_time + duration
            else:
                moving_time += duration # += forma corta de decir // moving_time = moving_time + duration

            #cambia el estado
            state = 'stopped' if command == "stop" else 'moving' #operador ternario, forma mas corta de decir  if command == "stop" /n state = 'stopped' /n else state = 'moving'
            state_start_time = time.time()
            print(f"State change to '{state}'.")

        elif command == "finish":
            if not trip_active:
                print("Error: No active trip to finish.")
                continue
            #agrega tiempodel ultimo estado
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration #  += forma corta de decir // stopped_time = stopped_time + duration
            else:
                moving_time += duration # forma corta de decir // moving_time = moving_time + duration

            #calcula la tarifa total y muestra el resumen del viaje

            total_fare = calculate_fare(stopped_time, moving_time)
            print(f"\n--- Trip Summary ---") # porque uso el "f" sino voy a incluir una variable aqui? IA indica que no es necesario
            print(f"Stopped time: {stopped_time:.1f} seconds") #.1f formatea numeros decimales ejemplo 12.3456 > 12.3 depues de usar el .1f
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Total fare: €{total_fare:.2f}") #.2f formatea numeros decimales ejemplo 12.3456 > 12.34 depues de usar el .2f. el numero despues del punti indica la cantidad de decimales a mostrar

            # Reset las variables para el proximo viaje
            trip_active = False
            state = None

        elif command == "exit":
            logging.info("Program terminated.")
            break

        else:
            print("Uknown command. Use: start, stop, move, finish, or exit")

if __name__ == "__main__":
    taximeter()

    






        








