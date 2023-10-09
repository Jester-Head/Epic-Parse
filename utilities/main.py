from data_cleaning import load_datasets, merge_datasets
from data_fetcher import get_all_pve_talents, get_all_pvp_talents, get_all_spells, get_spell_index, save_talent_index, save_talent_tree_index, save_talent_tree_nodes
from wow_api import WoWData
import file_utils
import data_processing
import config


def initialize_api():
    """ Initialize the WoW API and obtain the access token. """
    # Obtain access token using WoWData class with provided CLIENT_ID and CLIENT_SECRET
    access_token = WoWData().create_access_token(
        client_id=config.CLIENT_ID, client_secret=config.CLIENT_SECRET)
    return access_token


def fetch_and_save_data(access_token):
    """ Fetch data from the WoW API and save it to the appropriate files. """
    # Fetch spell index data and save as JSON
    get_spell_index(access_token=access_token, filename=config.SPELLS_INDEX)

    # Fetch all spell details and save as JSON
    get_all_spells(access_token=access_token,
                   read_file=config.SPELLS_INDEX, write_file=config.SPELLS)

    # Save PvE talent index data as JSON
    save_talent_index(config.PVE_TALENTS_INDEX, WoWData(
    ).get_talent_index(access_token=access_token))

    # Fetch all PvE talent details and save as JSON
    get_all_pve_talents(access_token=access_token,
                        read_file=config.PVE_TALENTS_INDEX, write_file=config.PVE_TALENTS)

    # Save PvP talent index data as JSON
    save_talent_index(config.PVP_TALENTS_INDEX, WoWData(
    ).get_pvp_talent_index(access_token=access_token))

    # Fetch all PvP talent details and save as JSON
    get_all_pvp_talents(access_token=access_token,
                        read_file=config.PVP_TALENTS_INDEX, write_file=config.PVP_TALENTS)

    # Save talent tree index data as JSON
    save_talent_tree_index(access_token, config.INDEX_JSON)

    # Save talent tree nodes data as JSON
    save_talent_tree_nodes(access_token, config.INDEX_JSON,
                           config.OUT_DIR_NODES)  # Different Structure


def process_data():
    """ Process the saved data. """
    # Extract spell info from saved JSON and store in a CSV file
    spells = data_processing.load_json_data(config.SPELLS)
    spells.to_csv(config.SPELLS_CSV)

    # Extract pve talent info from saved JSON and store in a CSV file
    pve_talents = data_processing.flatten_pve_to_dataframe(
        file_utils.read_json_file(config.PVE_TALENTS))
    pve_talents.to_csv(config.PVE_TALENTS_CSV, index=False)

    # Extract pvp talent info from saved JSON and store in a CSV file
    pvp_talents = data_processing.flatten_pvp_to_dataframe(
        file_utils.read_json_file(config.PVP_TALENTS))
    pvp_talents.to_csv(config.PVP_TALENTS_CSV, index=False)

    # Extract talent tree info from saved JSON and store in a DataFrame
    spec_df = data_processing.extract_spec_talent_trees(config.INDEX_JSON)

    # Save extracted talent tree info to a CSV
    spec_df.to_csv(config.INDEX_CSV, index=False)

    # Save each talent tree's data as separate JSON files
    data_processing.save_spec_trees(config.INDEX_CSV, config.OUT_DIR)

    # Convert saved JSON files related to talent tree nodes info to CSV format
    file_utils.convert_talent_nodes_csv(config.OUT_DIR_NODES)

    # Convert saved JSON files related to talent tree info to CSV format
    file_utils.convert_json_to_csv(config.OUT_DIR)

    # Add class and talent spec to talent tree info and update CSV file
    file_utils.update_talents_csv(config.OUT_DIR)


def driver():
    """ Main orchestration function. """
    access_token = initialize_api()
    fetch_and_save_data(access_token)
    process_data()


def clean_data():
    # Load the datasets
    talent_trees_df, pve_talents_df, pvp_talents_df, spells_df = load_datasets()

    # Merge the datasets
    merged_data = merge_datasets(
        talent_trees_df, pve_talents_df, pvp_talents_df, spells_df)

    # Clean the merged dataset
    cleaned_data = clean_data(merged_data)

    # Save the cleaned dataset to a CSV file
    cleaned_data.to_csv('/path/to/cleaned_dataset.csv', index=False)
    print("Cleaned dataset saved successfully!")


if __name__ == "__main__":
    driver()
