import time #con esto importo el modulo de tiempo de python que me permite trabajar con el tiempo.

import logging #con esto importo el modulo de logs que me permite crear los log.

import random # este  modulo me permitira simular los usuarios que demandan taxis. 

logging.basicConfig(
    filename="taximeter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def calculate_fare(seconds_stopped, seconds_moving, multiplier): # remember to keep identation
    """
    calcular la tarifa total en euros. 
    - Stopped: 0.02 €/s
    - Moving 0.05 €/s
    """
    base_fare = (seconds_stopped * 0.02 + seconds_moving * 0.05 )
     #esto calcula el precio base es la "funcion principal" de mi codigo
    fare = base_fare * multiplier
    logging.info(
        f"Fare calculated: €{fare:.2f}"
     )
    return fare

def save_trip(stopped_time, moving_time, total_fare): # Guarda el resumen del viaje en un archivo de texto.

    with open("trip_history.txt", "a") as file:

        file.write("\n--- Trip Summary ---\n")
        file.write(f"Stopped time: {stopped_time:.1f} seconds\n")
        file.write(f"Moving time: {moving_time:.1f} seconds\n")
        file.write(f"Total fare: €{total_fare:.2f}\n")
        file.write("------------------------\n")

def simulate_market_conditions(): #creo una funcion para simular demanda en el mercado

    demand = random.randint(20, 120) # esta funcion de python me permite generar numeros aleatorios, en este caso entre 20 y 120 (incluidos)

    available_taxis = random.randint(10, 60) # esta funcion "random.randint(10, 60)" de python me permite generar numeros aleatorios, en este caso entre 10 y 60 (incluidos)

    return demand, available_taxis

# una vez tengo oferta y demanda creo funcion para calcular un multiplicador para mi tarifa base. 
def calculate_surge_multiplier(
    demand,
    available_taxis
):

    if available_taxis == 0:
        return 3.0

    ratio = demand / available_taxis

    if ratio >= 3:
        return 2.5

    elif ratio >= 2:
        return 2.0

    elif ratio >= 1.5:
        return 1.5

    else:
        return 1.0

def get_demand_level(multiplier):

    if multiplier >= 2.5:
        return "Very High"

    elif multiplier >= 2.0:
        return "High"

    elif multiplier >= 1.5:
        return "Medium"

    else:
        return "Low"

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

    while True: 
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
                logging.warning("Error: No active trip. Please start a trip first.")
                print("Error: please start a trip first.") #este print lo coloque porque no daba mensaje si colocaba la opcion "move" de inicio, sin viaje iniciado. 
            # en la siguiente linea se calcula el tiempo del estado anterior.
                continue
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
            demand, available_taxis = simulate_market_conditions() #aqui llamo a la funcion con valores ramdon que defini al inicio "simulate_market_conditions"
            multiplier = calculate_surge_multiplier(demand, available_taxis) #defino mi variable "multipler"
            demand_level = get_demand_level(multiplier) # 
            total_fare = calculate_fare(stopped_time, moving_time, multiplier)
            save_trip(stopped_time, moving_time, total_fare)
            print(f"\n--- Trip Summary ---") # porque uso el "f" sino voy a incluir una variable aqui? IA indica que no es necesario
            print(f"Stopped time: {stopped_time:.1f} seconds") #.1f formatea numeros decimales ejemplo 12.3456 > 12.3 depues de usar el .1f
            print(f"Moving time: {moving_time:.1f} seconds")
            print(f"Demand level during the trip: {demand_level}")
            print(f"Total fare: €{total_fare:.2f}") #.2f formatea numeros decimales ejemplo 12.3456 > 12.34 depues de usar el .2f. el numero despues del punti indica la cantidad de decimales a mostrar

            # Reset las variables para el proximo viaje
            trip_active = False
            state = None

        elif command == "exit":
            if trip_active:
                print("Error: Finish the current trip before exiting.")
                logging.warning("Attempt to exit while trip is active") # aqui agregue que no se pueda usar "exit" si hay viaje en curso. Y me genere un log. 
                continue

            logging.info("Program terminated.")
            break

        else:
            print("Uknown command. Use: start, stop, move, finish, or exit")

if __name__ == "__main__":
    taximeter()

    






        








