def createDataFrame():
    '''
    
    '''
    df_temp = pd.read_csv(os.path.join(root, filename),
                          parse_dates=[['Date', 'Time']], encoding="ISO-8859-1", on_bad_lines='skip', engine='python')
    df_temp['rack_num'] = rack_number
    df_temp.drop(['Row'], axis=1, inplace=True)
    return df_temp


def formatDataFrame(df):
    '''
    
    '''
    df = pd.concat(df, axis=0)
    df.reset_index(inplace=True, drop=True)
    return df
