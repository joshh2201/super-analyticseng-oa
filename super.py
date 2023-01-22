import pandas as pd
import re

def str_to_table(data):
    """
    Takes stringified table, applies data transformations and cleaning, and returns a pandas dataframe.
    """

    data_arr = [i.split(';') for i in data.split('\n')][:-1]    # omitting last element in list prevents null row in dataframe
    df = pd.DataFrame(data_arr[1:], columns=data_arr[0])
    df['Airline Code'] = df['Airline Code'].apply(__airline_code)
    df['FlightCodes'] = _flight_code(pd.to_numeric(df['FlightCodes']).fillna(0).astype(int).values)
    df[['To','From']] = df['To_From'].astype(str).apply(_to_from)
    return df

def _flight_code(series):
    """
    Fills zero values in the series by incrementing previous non-zero value by 10.
    """

    for i in range(len(series)):
        if series[i] == 0:
            series[i] = series[i-1] + 10
    return series

def _to_from(string):
    """
    Applies title case to the string and splits it into two series.
    """

    return pd.Series(string.title().split('_'))

def __airline_code(code):
    """
    Removes non-letter characters and extra spaces in the string.
    """
    return re.findall("[A-Za-z]+\s?[A-Za-z]+",code,re.IGNORECASE)[0]

if __name__ == '__main__':
    data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'
    data_table = str_to_table(data)
    print(data_table.head())