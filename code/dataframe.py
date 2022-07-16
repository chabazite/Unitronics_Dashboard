import pandas as pd
import os

def createDataFrame(root, filename, rack_number):
    """
    this function reads each csv file and creates a temporary dataframe from each file,
    which will be used to append to a larger dataframe list

    Args:
        root (string): root directory path to search for files
        filename (string): individual filenames within root directory
        rack_number (string): rack number string created from filename search

    Returns:
        DataFrame: temporary dataframe to be appended to the master dataframe
    """
    df_temp = pd.read_csv(os.path.join(root, filename),
                          parse_dates=[['Date', 'Time']], encoding="ISO-8859-1", on_bad_lines='skip', engine='python')
    df_temp['rack_num'] = rack_number
    df_temp.drop(['Row'], axis=1, inplace=True)

    return df_temp


def concatDataFrame(df):
    """
    takes the  list of dataframes created above and concatonates them into a single master dataframe

    Args:
        df (Dataframe): temporary dataframe list

    Returns:
        dataframe: master dataframe
    """
    df = pd.concat(df, axis=0)
    df.reset_index(inplace=True, drop=True)
    return df
