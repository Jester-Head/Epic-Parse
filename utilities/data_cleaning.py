import pandas as pd

from config import ALL_ABILITIES, PVE_TALENTS_CSV, PVP_TALENTS_CSV, SPELLS_CSV

def load_datasets():
    # Load datasets
    talent_trees_df = pd.read_csv(ALL_ABILITIES)
    pve_talents_df = pd.read_csv(PVE_TALENTS_CSV)
    pvp_talents_df = pd.read_csv(PVP_TALENTS_CSV)
    spells_df = pd.read_csv(SPELLS_CSV)
    
    return talent_trees_df, pve_talents_df, pvp_talents_df, spells_df

def merge_datasets(talent_trees_df, pve_talents_df, pvp_talents_df, spells_df):
    # Merge datasets
    merged_data = pd.merge(talent_trees_df, spells_df, left_on='spell_id', right_on='id', how='outer', suffixes=('_talent', '_spell'))
    merged_data = pd.merge(merged_data, pve_talents_df, on='spell_id', how='outer', suffixes=('', '_pve'))
    merged_data = pd.merge(merged_data, pvp_talents_df, on='spell_id', how='outer', suffixes=('', '_pvp'))
    
    return merged_data

def clean_data(merged_data):
    # Cleaning the merged dataset

    # Remove duplicate rows
    cleaned_data = merged_data.drop_duplicates()

    # Fill in missing values with the placeholder "N/A"
    cleaned_data_filled = cleaned_data.fillna("N/A")

    # Drop specified columns
    columns_to_drop = [
        'media.key.href', 'media.id', 'spell_tooltip.range', 
        'tooltip_range', 'default_points', '_links_self_href', 
        'spell_key_href', 'playable_class_key_href', 
        'playable_specialization_key_href'
    ]
    cleaned_data_final = cleaned_data_filled.drop(columns=columns_to_drop, errors='ignore')

    # Combine id_pvp with id column
    cleaned_data_final['id'] = cleaned_data_final.apply(lambda row: row['id_pvp'] if row['id'] == "N/A" else row['id'], axis=1)

    # Add PvP set indicator
    pvp_related_columns = [col for col in cleaned_data_final.columns if "_pvp" in col or "pvp" in col.lower()]
    cleaned_data_final['from_pvp_set'] = cleaned_data_final[pvp_related_columns].apply(lambda row: any(val != "Missing_PvP" for val in row), axis=1)

    # Drop the id_pvp column and other specified columns
    cleaned_data_final = cleaned_data_final.drop(columns=['id_pvp', 'playable_specialization_key_href_pvp'])

    return cleaned_data_final



