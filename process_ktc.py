import pandas as pd


def load_data(file_path, superflex=True):
    """
    Load the CSV data into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        DataFrame: The loaded data.
    """
    value = "SF Value" if superflex else "Non-SF Value"
    df = pd.read_csv(file_path)
    return df.sort_values(by=value, ascending=False, ignore_index=True)


def map_pick_numbers(df, league_sizes):
    """
    Map player ranks to startup pick numbers for different league sizes.

    Args:
        df (DataFrame): The dataframe with player rankings and values.
        league_sizes (list): A list of league sizes to calculate values for.

    Returns:
        DataFrame: The dataframe with mapped startup pick numbers.
    """
    max_rank = 500  # Only consider the first 500 ranked players
    for size in league_sizes:
        # Create a new column for each league size
        col_name = f"Pick Number ({size}-team)"
        df[col_name] = df.index.to_series().apply(lambda x: calculate_pick(x + 1, size))
    return df


def calculate_pick(rank, team_count):
    """
    Calculate the round and pick number based on rank and team count.

    Args:
        rank (int): The player's rank.
        team_count (int): The number of teams in the league.

    Returns:
        str: The formatted pick number as 'round.pick'.
    """
    if rank > team_count * max_rounds:
        return None  # If the rank is beyond the considered rounds, return None
    round_number = ((rank - 1) // team_count) + 1
    pick_number = ((rank - 1) % team_count) + 1
    return f"{round_number}.{str(pick_number).zfill(2)}"


# League sizes to calculate startup pick numbers for
league_sizes = [10, 12, 16, 20, 32]

# Define the maximum number of rounds to consider
max_rounds = 500 // min(
    league_sizes
)  # Here we consider enough rounds to cover 500 players in the smallest league

# File path to the CSV file
file_path = "ktc_pulled.csv"

# Load the data
df = load_data(file_path)

# Map the player ranks to startup pick numbers
df_with_picks = map_pick_numbers(df, league_sizes)

# Display the first few rows of the dataframe
print(df_with_picks.head())
df_with_picks.to_csv("ktc_values.csv", header=True, index=False)
with open("table.html", "w") as fo:
    df_with_picks.to_html(
        fo, index=False, table_id="valuesTable", classes="display nowrap"
    )
