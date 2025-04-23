#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract.py — Script corrigido para processar dados UFC e gerar estatísticas por lutador
"""

import os
import pandas as pd
import numpy as np
import argparse

def generate_fighter_stats(input_dir, output_file):
    # 1) Carrega arquivos CSV
    f_fighters = os.path.join(input_dir, 'ufc_fighter_data.csv')
    f_fights   = os.path.join(input_dir, 'ufc_fight_data.csv')
    f_stats    = os.path.join(input_dir, 'ufc_fight_stat_data.csv')

    fighters = pd.read_csv(f_fighters)
    fights   = pd.read_csv(f_fights)
    stats    = pd.read_csv(f_stats)

    # 2) Garante que temos a coluna 'fighter_id'
    #    Se o CSV usar outro nome (ex: 'id'), renomeie para 'fighter_id'
    if 'id' in fighters.columns and 'fighter_id' not in fighters.columns:
        fighters = fighters.rename(columns={'id': 'fighter_id'})

    # 3) Prepara dados de lutadores
    fighters['full_name'] = fighters['fighter_f_name'] + ' ' + fighters['fighter_l_name']
    fighters['dob']       = pd.to_datetime(fighters['fighter_dob'], errors='coerce')
    today = pd.to_datetime('2025-04-20')
    fighters['age'] = (today - fighters['dob']).dt.days // 365

    # 4) Converte para formato “longo”: uma linha por lutador por luta
    cols = ['fight_id', 'f_1', 'f_2', 'winner', 'result']
    f1 = fights[cols].rename(columns={'f_1': 'fighter_id', 'f_2': 'opponent_id'})
    f2 = fights[cols].rename(columns={'f_2': 'fighter_id', 'f_1': 'opponent_id'})
    df_long = pd.concat([f1, f2], ignore_index=True)

    # 5) Marca vitória/derrota
    df_long['is_win']  = df_long['fighter_id'] == df_long['winner']
    df_long['is_loss'] = (~df_long['is_win']) & df_long['result'].notna()

    # 6) Mescla estatísticas próprias
    df_long = df_long.merge(stats, on=['fight_id', 'fighter_id'], how='left')

    # 7) Mescla estatísticas do oponente (prefixo 'opp_')
    stats_opp = stats.rename(columns={
        'fighter_id':     'opponent_id',
        'knockdowns':     'opp_knockdowns',
        'total_strikes_att':  'opp_total_str_att',
        'total_strikes_succ':'opp_total_str_succ',
        'sig_strikes_att':   'opp_sig_str_att',
        'sig_strikes_succ':  'opp_sig_str_succ',
        'takedown_att':      'opp_td_att',
        'takedown_succ':     'opp_td_succ',
        'submission_att':    'opp_sub_att',
    })
    df_long = df_long.merge(
        stats_opp[['fight_id','opponent_id',
                   'opp_total_str_att','opp_total_str_succ',
                   'opp_td_att','opp_td_succ','opp_sub_att']],
        on=['fight_id','opponent_id'], how='left'
    )

    # 8) Calcula métricas por luta
    df_long['strike_accuracy'] = df_long['sig_strikes_succ'] / df_long['sig_strikes_att']
    df_long['td_off_pct']      = df_long['takedown_succ']   / df_long['takedown_att']
    df_long['td_def_pct']      = 1 - (df_long['opp_td_succ'] / df_long['opp_td_att'])
    df_long['str_abs_pct']     = df_long['opp_total_str_succ'] / df_long['opp_total_str_att']

    # Remove infs e NaNs
    for c in ['strike_accuracy', 'td_off_pct', 'td_def_pct', 'str_abs_pct']:
        df_long[c] = df_long[c].replace([np.inf, -np.inf], np.nan)

    # 9) Junta demografia e estância (como placeholder)
    df_long = df_long.merge(
        fighters[['fighter_id','full_name','fighter_stance','age']],
        on='fighter_id', how='left'
    )

    # 10) Agrega estatísticas por lutador usando tuplas (coluna, função)
    agg = df_long.groupby(['fighter_id','full_name','fighter_stance','age']).agg(
        total_fights      = ('fight_id',      'count'),
        wins              = ('is_win',        'sum'),
        losses            = ('is_loss',       'sum'),
        avg_total_str_att = ('total_strikes_att','mean'),
        avg_sig_str_att   = ('sig_strikes_att','mean'),
        avg_strike_acc    = ('strike_accuracy','mean'),
        avg_td_att        = ('takedown_att',  'mean'),
        avg_td_off_pct    = ('td_off_pct',    'mean'),
        avg_td_def_pct    = ('td_def_pct',    'mean'),
        avg_sub_att       = ('submission_att','mean'),
        avg_str_abs_pct   = ('str_abs_pct',   'mean'),
        ko_wins           = ('result', lambda s: ((s.str.contains('KO', na=False)) & df_long.loc[s.index,'is_win']).sum()),
        ko_losses         = ('result', lambda s: ((s.str.contains('KO', na=False)) & df_long.loc[s.index,'is_loss']).sum()),
        sub_wins          = ('result', lambda s: ((s.str.contains('SUB', na=False)) & df_long.loc[s.index,'is_win']).sum()),
        sub_losses        = ('result', lambda s: ((s.str.contains('SUB', na=False)) & df_long.loc[s.index,'is_loss']).sum()),
    ).reset_index()

    # 11) Classificação de estilo de luta
    def classify_style(r):
        if r['avg_sub_att'] >= 1 and r['sub_wins'] > r['ko_wins']:
            return 'Jiu-Jitsu'
        if r['avg_td_att'] >= 1 and r['avg_td_off_pct'] >= 0.5:
            return 'Wrestler'
        if r['avg_sig_str_att'] >= 20 and r['avg_strike_acc'] >= 0.5:
            return 'Kickboxer'
        if r['avg_strike_acc'] >= 0.5:
            return 'Boxer'
        return 'Mixed'

    agg['fighting_style'] = agg.apply(classify_style, axis=1)

    # 12) Salva arquivo final
    agg.to_csv(output_file, index=False)
    print(f"Resumo com estatísticas e estilo salvo em: {output_file}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Gera estatísticas por lutador UFC.")
    parser.add_argument('input_dir', help="Diretório com os CSVs raw")
    parser.add_argument('output_file', help="Caminho de saída para o CSV consolidado")
    args = parser.parse_args()

    generate_fighter_stats(args.input_dir, args.output_file)
