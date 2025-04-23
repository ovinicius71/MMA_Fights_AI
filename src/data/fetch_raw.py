import pandas as pd

def load_fighter_data(fighter_file):
    """
    Carrega os dados dos lutadores a partir do arquivo CSV.
    Retorna um DataFrame com os dados dos lutadores.
    """
    try:
        df_fighters = pd.read_csv(fighter_file)
        print("Dados dos lutadores carregados com sucesso!")
        return df_fighters
    except Exception as e:
        print(f"Erro ao carregar os dados dos lutadores: {e}")
        return None

def load_fight_data(fight_file):
    """
    Carrega os dados das lutas a partir do arquivo CSV.
    Retorna um DataFrame com os dados das lutas.
    """
    try:
        df_fights = pd.read_csv(fight_file)
        print("Dados das lutas carregados com sucesso!")
        return df_fights
    except Exception as e:
        print(f"Erro ao carregar os dados das lutas: {e}")
        return None
    