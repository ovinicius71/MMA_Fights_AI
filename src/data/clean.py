def clean_data(df):
    """
    Realiza uma limpeza básica nos dados, removendo linhas com valores ausentes em colunas críticas.
    """
    critical_columns = ['fighter1', 'fighter2', 'outcome']  # Ajuste conforme necessário
    df_cleaned = df.dropna(subset=critical_columns)
    return df_cleaned

def infer_fighting_style(df_fights, fighter_name):
    """
    Infere o estilo de luta de um lutador com base em suas estatísticas de lutas.
    Retorna 'grappler' se a média de takedowns for alta, caso contrário 'striker'.
    """
    fighter_data = df_fights[(df_fights['fighter1'] == fighter_name) | (df_fights['fighter2'] == fighter_name)]
    if fighter_data.empty:
        return 'unknown'
    
    # Exemplo simplificado: se a média de takedowns for maior que 2, é grappler
    takedown_avg = fighter_data['fighter1_takedown_avg_per15m'].mean() if fighter_name in fighter_data['fighter1'].values else fighter_data['fighter2_takedown_avg_per15m'].mean()
    return 'grappler' if takedown_avg > 2 else 'striker'

def create_fighter_profile(df_fighters, df_fights, fighter_name):
    """
    Cria um perfil detalhado para um lutador, incluindo estatísticas médias e histórico de lutas.
    Retorna um dicionário com as informações do lutador.
    """
    fighter_data = df_fights[(df_fights['fighter1'] == fighter_name) | (df_fights['fighter2'] == fighter_name)]
    if fighter_data.empty:
        return None
    
    # Calcula vitórias e derrotas
    wins = len(fighter_data[fighter_data['outcome'] == fighter_name])
    losses = len(fighter_data) - wins
    
    # Extrai estatísticas médias
    stats = {
        'name': fighter_name,
        'style': infer_fighting_style(df_fights, fighter_name),
        'sig_strikes_pm': fighter_data['fighter1_sig_strikes_landed_pm'].mean() if fighter_name in fighter_data['fighter1'].values else fighter_data['fighter2_sig_strikes_landed_pm'].mean(),
        'takedown_avg': fighter_data['fighter1_takedown_avg_per15m'].mean() if fighter_name in fighter_data['fighter1'].values else fighter_data['fighter2_takedown_avg_per15m'].mean(),
        'wins': wins,
        'losses': losses,
        'fights': len(fighter_data)
    }
    
    return stats
