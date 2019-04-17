import io
import pandas as pd
import numpy as np
import tablib


def binary_excel_to_df(binary):
    """
    I am using 'python' engine because it has no problem with UTF characters
    while as default 'C' engine might raise exceptions in some cases
    """
    binary_stream = io.BytesIO(binary)
    return pd.read_excel(binary_stream)


def df_to_dataset(df: pd.DataFrame, **kwargs):
    """
    :param kwargs: kwargs are additional keys to pass to `df`
    For example if kwargs is {'some': 3}, than df gets new column `some` with value set to 3 in every row
    """
    df = df.replace(np.nan, '', regex=True)

    for key, value in kwargs.items():
        df[key] = value

    headers = df.columns.values.tolist()
    data = df.values.tolist()

    return tablib.Dataset(*data, headers=headers)


def collect_excel_import_errors(result):
    errors = []
    for row_error in result.row_errors():
        errors.append(f'Row {row_error[0] + 1}: {row_error[1][0].error}')
    return errors
