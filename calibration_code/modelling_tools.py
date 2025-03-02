import pandas as pd
import plotly.express as px

def show_unique_values(df, col, transpose=True):
    """
    Displays unique values of a column in a formatted DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - col (str): The column name to extract unique values from.
    - transpose (bool): Whether to transpose the result (default is True).

    Returns:
    - pd.DataFrame: A DataFrame containing the unique values.
    """
    unique_values = pd.DataFrame(df[col].unique(),
                                 index=[''] * len(df[col].unique()),
                                 columns=[''])

    return unique_values.transpose() if transpose else unique_values


def plot_univariate_freq(df, column_name, figsize=(900, 500), title=None, normalize=False):
    """
    Generates an interactive bar chart displaying the frequency distribution of a categorical column using Plotly.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - column_name (str): The name of the categorical column to plot.
    - figsize (tuple): The figure size (width, height) in pixels, default is (900, 500).
    - title (str): Custom title for the plot. If None, a default title is generated.
    - normalize (bool): If True, displays proportions instead of absolute counts.

    Raises:
    - ValueError: If the specified column is not found in the DataFrame.

    Returns:
    - plotly.graph_objects.Figure: The generated interactive plot.
    """

    # Check if the column exists in the DataFrame
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    # Compute frequency (excluding NaN values)
    freq_df = df[column_name].dropna().value_counts(normalize=normalize)
    freq_df = freq_df.rename_axis(column_name).reset_index(name='count')

    # Convert proportions to percentages if normalize=True
    if normalize:
        freq_df['count'] *= 100  # Convert to percentage

    # Define the title
    if title is None:
        title = f"Distribution of {column_name}" + (" (Normalized)" if normalize else "")

    # Create the interactive bar chart
    fig = px.bar(
        freq_df,
        x=column_name,
        y='count',
        text=freq_df['count'].apply(lambda x: f"{x:.2f}%" if normalize else f"{int(x)}"),
        title=title,
        labels={column_name: column_name, 'count': 'Proportion (%)' if normalize else 'Frequency'},
        color_discrete_sequence=['skyblue']
    )

    # Customize layout
    fig.update_traces(textposition='outside', marker=dict(line=dict(color='black', width=1)))
    fig.update_layout(
        xaxis_tickangle=-45,
        height=figsize[1],
        width=figsize[0],
        template='plotly_white'
    )

    return fig

def plot_histogram(df, column, bins=20, fill_color="skyblue", edge_color="black", edge_width=1.5, figsize=(800,500), show_mean=True):
    """
    Generates an interactive histogram for a given continuous column using Plotly,
    ensuring skyblue bars with black borders.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - column (str): The name of the numeric column to plot.
    - bins (int): Number of bins for the histogram (default: 20).
    - fill_color (str): Fill color of the bars (default: 'skyblue').
    - edge_color (str): Color of the bar borders (default: 'black').
    - edge_width (float): Width of the bar borders (default: 1.5).
    - figsize (tuple): Figure size in pixels (default: (800, 500)).
    - show_mean (bool): Whether to display the mean as a vertical line (default: True).

    Returns:
    - plotly.graph_objects.Figure: The generated interactive histogram.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    if not pd.api.types.is_numeric_dtype(df[column]):
        raise TypeError(f"Column '{column}' must be numeric.")

    # Create the histogram
    fig = px.histogram(df, x=column, nbins=bins, title=f"Distribution of {column}")

    # Ensure bars are skyblue and have black edges
    fig.update_traces(marker=dict(color=fill_color, line=dict(color=edge_color, width=edge_width)))

    # Add a vertical line for the mean if show_mean=True
    if show_mean:
        mean_value = df[column].mean()
        fig.add_vline(x=mean_value, line_dash="dash", line_color="red",
                      annotation_text=f"Mean: {mean_value:.2f}", annotation_position="top right")

    # Customize layout
    fig.update_layout(
        xaxis_title=column,
        yaxis_title="Count",
        width=figsize[0], height=figsize[1],
        template="plotly_white"
    )

    return fig


def rename_low_density_categories(df, column, threshold, new_category="Otros"):
    """
    Creates a new DataFrame where categories in a given column that have fewer than `threshold` occurrences
    are grouped into a new category.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - column (str): The name of the categorical column to process.
    - threshold (int): Minimum count required to keep a category (default: 72).
    - new_category (str): The name of the new grouped category (default: "Otros").

    Returns:
    - pd.DataFrame: A new DataFrame with updated values in the specified column.
    """

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")

    df_copy = df.copy()

    value_counts = df_copy[column].value_counts()

    # Identify categories that appear fewer times than the threshold
    rare_categories = value_counts[value_counts < threshold].index

    df_copy[column] = df_copy[column].apply(lambda x: new_category if x in rare_categories else x)

    return df_copy

import pandas as pd

def create_deciles(df, continuous_variable, n_deciles=10):
    """
    Divides a continuous variable into deciles and returns a DataFrame with decile labels.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        continuous_variable (str): Name of the continuous variable to be divided into deciles.
        n_deciles (int): Number of deciles to create (default is 10).

    Returns:
        pd.DataFrame: DataFrame with decile labels.
        pd.DataFrame: Summary table with decile ranges, counts, and proportions.
    """
    df = df.copy()
    df["Decile"] = pd.qcut(df[continuous_variable], q=n_deciles, labels=False, duplicates="drop")
    decile_summary = df.groupby("Decile")[continuous_variable].agg(["min", "max", "count"])
    decile_summary.rename(columns={"min": "Decile_Min", "max": "Decile_Max", "count": "Decile_Count"}, inplace=True)
    decile_summary["Decile_Proportion"] = decile_summary["Decile_Count"] / decile_summary["Decile_Count"].sum()
    return df, decile_summary


def count_categories_by_decile(df, decile_col="Decile", target_col="Credit_Score"):
    """
    Counts the frequency of each category within each decile.

    Parameters:
        df (pd.DataFrame): DataFrame containing the decile column and the categorical variable.
        decile_col (str): Name of the decile column.
        target_col (str): Name of the categorical variable to count.

    Returns:
        pd.DataFrame: Frequency table showing the number of cases per category in each decile with prefixed column names.
    """
    count_table = df.groupby([decile_col, target_col]).size().unstack(fill_value=0)
    count_table = count_table.add_prefix("count_")
    return count_table


def calculate_category_proportions(df, decile_col="Decile", target_col="Credit_Score"):
    """
    Computes the proportion of each category within each decile.

    Parameters:
        df (pd.DataFrame): DataFrame containing the decile column and the categorical variable.
        decile_col (str): Name of the decile column.
        target_col (str): Name of the categorical variable to calculate proportions.

    Returns:
        pd.DataFrame: Table of proportions of each category within each decile with prefixed column names.
    """
    count_table = count_categories_by_decile(df, decile_col, target_col)
    prop_table = count_table.div(count_table.sum(axis=1), axis=0)  # Normalize by row
    prop_table = prop_table.add_prefix("prop_")
    return prop_table


def summarize_decile_analysis(df, continuous_variable, target_col="Credit_Score", n_deciles=10):
    """
    Combines decile summary, category counts, and category proportions into a single structure.

    Parameters:
        df (pd.DataFrame): DataFrame containing the continuous variable and categorical target.
        continuous_variable (str): Name of the continuous variable.
        target_col (str): Name of the categorical target variable.
        n_deciles (int): Number of deciles to create (default is 10).

    Returns:
        dict: Contains DataFrame with deciles and a combined analysis DataFrame.
    """
    df_deciles, decile_summary = create_deciles(df, continuous_variable, n_deciles)
    category_counts = count_categories_by_decile(df_deciles, "Decile", target_col)
    category_proportions = calculate_category_proportions(df_deciles, "Decile", target_col)

    decile_analysis = pd.concat([decile_summary, category_counts, category_proportions], axis=1)
    
    analysis_summary = {
        "df_deciles": df_deciles,
        "decile_summary": decile_analysis,
    }
    
    return analysis_summary

def group_deciles(df_deciles, group_map, new_col_name="Grouped_Decile"):
    """
    Groups deciles into larger categories based on a user-defined mapping.

    Parameters:
        df_deciles (pd.DataFrame): DataFrame containing the deciles column.
        group_map (dict): Dictionary mapping decile numbers to group names.
        new_col_name (str): Name of the new grouped column (default: "Grouped_Decile").

    Returns:
        pd.DataFrame: Updated DataFrame with the new grouped column.
    """
    df = df_deciles.copy()
    df[new_col_name] = df["Decile"].map(group_map)
    return df


def summarize_grouped_deciles(df, grouped_col="Grouped_Decile", continuous_variable="Age", target_col="Credit_Score", prefix="Grouped"):
    """
    Summarizes statistics for newly grouped deciles, ensuring consistency with the original decile summary structure.

    Parameters:
        df (pd.DataFrame): DataFrame containing the grouped deciles column.
        grouped_col (str): Name of the grouped decile column.
        continuous_variable (str): Name of the original continuous variable.
        target_col (str): Name of the categorical target variable.
        prefix (str): Prefix to use for column names to differentiate from original deciles.

    Returns:
        pd.DataFrame: Summary statistics for the grouped deciles.
    """
    # Obtener los valores mínimos y máximos de la variable continua en cada grupo
    grouped_summary = df.groupby(grouped_col)[continuous_variable].agg(["min", "max", "count"])
    grouped_summary.rename(columns={"min": f"{prefix}_Min", "max": f"{prefix}_Max", "count": f"{prefix}_Count"}, inplace=True)

    # Calcular la proporción de cada grupo respecto al total
    grouped_summary[f"{prefix}_Proportion"] = grouped_summary[f"{prefix}_Count"] / grouped_summary[f"{prefix}_Count"].sum()

    # Calcular conteos y proporciones por categoría usando funciones existentes
    category_counts = count_categories_by_decile(df, grouped_col, target_col)
    category_proportions = calculate_category_proportions(df, grouped_col, target_col)

    # Unir todas las tablas en un solo dataframe final
    grouped_analysis = pd.concat([grouped_summary, category_counts, category_proportions], axis=1)

    return grouped_analysis.reset_index()


