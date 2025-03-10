import pandas as pd

def g(df, decimals=2):
    """
    Formatea las columnas numéricas de un DataFrame con el número de decimales especificado.

    Esta función recorre las columnas de un DataFrame y aplica un formato numérico a aquellas columnas 
    que contengan datos numéricos. Las columnas de tipo string o datetime se dejan sin cambios.
    
    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos a formatear.
    
    decimals : int, opcional, por defecto 2
        El número de decimales que se desea mostrar en las columnas numéricas.

    Retorna:
    --------
    pandas.DataFrame
        Un nuevo DataFrame con las columnas numéricas formateadas según el número de decimales especificado.
        Las columnas de tipo string o datetime no son alteradas.

    """
    format_str = f'{{:,.{decimals}f}}'
    return df.apply(lambda col: col.apply(lambda x: format_str.format(x) if pd.api.types.is_numeric_dtype(col) else x))

def format_number(n):
    """
    Formats a number with thousand separators.

    Parameters:
    -----------
    n : int
        The number to format.

    Returns:
    --------
    str
        The formatted number as a string.
    """
    return f"{n:,}"

def describe_dataset(metrics, separator_length=50):
    """
    Prints key summary statistics based on a dictionary of metrics.

    Parameters:
    -----------
    metrics : dict
        Dictionary where keys are description labels and values are the precomputed metric values.
    
    separator_length : int, optional
        Number of dashes used as a separator (default: 50).
    """
    separator = "-" * separator_length
    for label, value in metrics.items():
        print(separator)
        print(f"{label}: {value}")
    print(separator)
