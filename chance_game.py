import random
from dataclasses import dataclass #Importación del decorador @dataclass para definir las configuraciones del juego (GameConfig, GameResult y SimulationResults)

# Configuración del juego
@dataclass
class GameConfig:
    min_bet: int = 5  # Apuesta mínima permitida
    max_bet: int = 100  # Apuesta máxima permitida
    win_threshold: int = 500  # Balance necesario para ganar
    lose_threshold: int = -100  # Balance en el cual se pierde
    initial_balance: int = 0  # Balance inicial del jugador
    num_simulations: int = 1000  # Número de simulaciones a realizar

# Resultados de una partida individual
@dataclass
class GameResult:
    final_balance: int  # Balance (cantidad de dinero) final al terminar la partida
    num_rounds: int  # Número de rondas jugadas en la partida
    max_balance: int  # Balance máximo alcanzado durante la partida
    min_balance: int  # Balance mínimo alcanzado durante la partida

# Resultados agregados de todas las simulaciones
@dataclass
class SimulationResults:
    wins: int = 0  # Número total de victorias en todas las simulaciones
    losses: int = 0  # Número total de derrotas en todas las simulaciones
    total_rounds: int = 0  # Número total de rondas jugadas en todas las simulaciones
    total_balance: int = 0  # Suma de los balances finales de todas las simulaciones
    max_balance: int = 0  # Balance máximo alcanzado en cualquier simulación
    min_balance: int = 0  # Balance mínimo alcanzado en cualquier simulación

def roll_dice() -> int:
    """Simula el lanzamiento de un dado de 6 caras."""
    return random.randint(1, 6)

def is_win(roll: int) -> bool:
    """Determina si el lanzamiento es ganador (par)."""
    return roll % 2 == 0

def play_game(config: GameConfig) -> GameResult:
    """Simula una partida individual del juego."""
    balance = config.initial_balance  # Inicializar el balance con el valor inicial
    rounds = 0  # Contador de rondas jugadas
    max_balance = balance  # Inicializar el balance máximo con el balance inicial
    min_balance = balance  # Inicializar el balance mínimo con el balance inicial

    while config.lose_threshold < balance < config.win_threshold:
        # Continuar jugando mientras el balance esté entre los límites de ganar y perder
        bet = random.randint(config.min_bet, config.max_bet)  
        rounds += 1  

        if is_win(roll_dice()):
            balance += bet  # Incrementar el balance si se gana
        else:
            balance -= bet  # Reducir el balance si se pierde

        max_balance = max(max_balance, balance)
        min_balance = min(min_balance, balance)  

    return GameResult(balance, rounds, max_balance, min_balance) 

def run_simulations(config: GameConfig) -> SimulationResults:
    """Ejecuta múltiples simulaciones del juego y recopila estadísticas."""
    results = SimulationResults()  # Inicializar los resultados agregados

    for _ in range(config.num_simulations):
        game_result = play_game(config)  
        
        if game_result.final_balance >= config.win_threshold:
            results.wins += 1 
        elif game_result.final_balance <= config.lose_threshold:
            results.losses += 1 

        results.total_rounds += game_result.num_rounds 
        results.total_balance += game_result.final_balance  
        results.max_balance = max(results.max_balance, game_result.max_balance) 
        results.min_balance = min(results.min_balance, game_result.min_balance) 

    return results  # Devolver los resultados agregados

def print_results(config: GameConfig, results: SimulationResults):
    """Imprime un análisis detallado de los resultados de la simulación."""
    print(f"\n--- Resultados de {config.num_simulations} simulaciones ---")
    print(f"Victorias: {results.wins} ({results.wins/config.num_simulations*100:.2f}%)")
    print(f"Derrotas: {results.losses} ({results.losses/config.num_simulations*100:.2f}%)")
    print(f"Empates: {config.num_simulations - results.wins - results.losses} ({(config.num_simulations - results.wins - results.losses)/config.num_simulations*100:.2f}%)")
    print(f"\nPromedio de rondas por juego: {results.total_rounds/config.num_simulations:.2f}")
    print(f"Balance promedio final: ${results.total_balance/config.num_simulations:.2f}")
    print(f"Máximo balance alcanzado: ${results.max_balance}")
    print(f"Mínimo balance alcanzado: ${results.min_balance}")
    
    if results.wins > 0:
        print(f"\nProbabilidad de ganar: {results.wins/config.num_simulations*100:.2f}%")
        print(f"Ganancia promedio al ganar: ${(config.win_threshold - config.initial_balance):.2f}")
    
    if results.losses > 0:
        print(f"Probabilidad de perder: {results.losses/config.num_simulations*100:.2f}%")
        print(f"Pérdida promedio al perder: ${(config.lose_threshold - config.initial_balance):.2f}")

def main():
    # Configuración personalizable
    config = GameConfig(
        min_bet=5,
        max_bet=50,
        win_threshold=500,
        lose_threshold=-100,
        initial_balance=0,
        num_simulations=100000
    )

    # Ejecutar simulaciones
    results = run_simulations(config)

    # Imprimir resultados
    print_results(config, results)

if __name__ == "__main__":
    main()
