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

def assign_deciles(df, continuous_variable, decile_col_name, n_deciles=10):
    """
    Assigns deciles to a continuous variable and adds a specified decile column.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        continuous_variable (str): Name of the continuous variable to be divided into deciles.
        decile_col_name (str): Name of the new column to store decile labels.
        n_deciles (int): Number of deciles to create (default is 10).

    Returns:
        pd.DataFrame: Updated DataFrame with the decile column.
    """
    df = df.copy()
    df[decile_col_name] = pd.qcut(df[continuous_variable], q=n_deciles, labels=False, duplicates="drop")
    return df


def statistics_by_decile(df, decile_col_name, continuous_variable):
    """
    Computes min, max, and count for each decile.

    Parameters:
        df (pd.DataFrame): DataFrame containing the decile column and the continuous variable.
        decile_col_name (str): Name of the decile column.
        continuous_variable (str): Name of the continuous variable.

    Returns:
        pd.DataFrame: Summary table with min, max, and count per decile.
    """
    return df.groupby(decile_col_name)[continuous_variable].agg(["min", "max", "count"])


def rename_decile_summary(decile_summary, prefix="Decile_"):
    """
    Renames columns in a decile summary table to standardized names.

    Parameters:
        decile_summary (pd.DataFrame): Decile summary with min, max, and count.
        prefix (str): Prefix to apply to column names (default: "Decile_").

    Returns:
        pd.DataFrame: Renamed decile summary.
    """
    return decile_summary.rename(columns={"min": f"{prefix}Min", "max": f"{prefix}Max", "count": f"{prefix}Count"})


def calculate_decile_proportions(decile_summary, count_col="Decile_Count", proportion_col="Decile_Proportion"):
    """
    Computes proportions for each decile.

    Parameters:
        decile_summary (pd.DataFrame): Decile summary containing count values.
        count_col (str): Name of the column containing count values (default: "Decile_Count").
        proportion_col (str): Name of the new proportion column (default: "Decile_Proportion").

    Returns:
        pd.Series: Decile proportions.
    """
    return decile_summary[count_col] / decile_summary[count_col].sum()


def count_categories_by_decile(df, decile_col, target_col):
    """
    Counts the frequency of each category within each decile.

    Parameters:
        df (pd.DataFrame): DataFrame containing the decile column and the categorical variable.
        decile_col (str): Name of the decile column.
        target_col (str): Name of the categorical variable to count.

    Returns:
        pd.DataFrame: Frequency table showing the number of cases per category in each decile.
    """
    return df.groupby([decile_col, target_col]).size().unstack(fill_value=0)


def rename_count_columns(count_df, prefix="count_"):
    """
    Renames count columns by adding a prefix.

    Parameters:
        count_df (pd.DataFrame): DataFrame with category counts.
        prefix (str): Prefix to apply to column names (default: "count_").

    Returns:
        pd.DataFrame: DataFrame with renamed columns.
    """
    return count_df.rename(columns={col: f"{prefix}{col}" for col in count_df.columns})


def calculate_category_proportions(df, decile_col, target_col):
    """
    Computes the proportion of each category within each decile.

    Parameters:
        df (pd.DataFrame): DataFrame containing the decile column and the categorical variable.
        decile_col (str): Name of the decile column.
        target_col (str): Name of the categorical variable to calculate proportions.

    Returns:
        pd.DataFrame: Table of proportions of each category within each decile.
    """
    count_table = count_categories_by_decile(df, decile_col, target_col)
    return count_table.div(count_table.sum(axis=1), axis=0)


def rename_prop_columns(prop_df, prefix="prop_"):
    """
    Renames proportion columns by adding a prefix.

    Parameters:
        prop_df (pd.DataFrame): DataFrame with category proportions.
        prefix (str): Prefix to apply to column names (default: "prop_").

    Returns:
        pd.DataFrame: DataFrame with renamed columns.
    """
    return prop_df.rename(columns={col: f"{prefix}{col}" for col in prop_df.columns})


def summarize_decile_analysis(df, continuous_variable, decile_col_name, target_col, n_deciles=10):
    """
    Combines decile summary, category counts, and category proportions into a single structure.

    Parameters:
        df (pd.DataFrame): DataFrame containing the continuous variable and categorical target.
        continuous_variable (str): Name of the continuous variable.
        decile_col_name (str): Name of the decile column.
        target_col (str): Name of the categorical target variable.
        n_deciles (int): Number of deciles to create (default is 10).

    Returns:
        dict: Contains DataFrame with deciles and a combined analysis DataFrame.
    """
    df_deciles = assign_deciles(df, continuous_variable, decile_col_name, n_deciles)
    decile_summary = statistics_by_decile(df_deciles, decile_col_name, continuous_variable)

    # Renombrar y calcular proporciones
    decile_summary = rename_decile_summary(decile_summary)
    decile_summary["Decile_Proportion"] = calculate_decile_proportions(decile_summary)

    # Obtener conteos y proporciones por categoría
    category_counts = rename_count_columns(count_categories_by_decile(df_deciles, decile_col_name, target_col))
    category_proportions = rename_prop_columns(calculate_category_proportions(df_deciles, decile_col_name, target_col))

    # Combinar resultados
    decile_analysis = pd.concat([decile_summary, category_counts, category_proportions], axis=1)

    return {
        "df_deciles": df_deciles,
        "decile_summary": decile_analysis,
    }


def group_deciles(df_deciles, decile_col_name, grouped_col_name, group_map):
    """
    Maps deciles into larger groups based on a user-defined mapping.

    Parameters:
        df_deciles (pd.DataFrame): DataFrame containing the decile column.
        decile_col_name (str): Name of the column that stores decile labels.
        grouped_col_name (str): Name of the new column to store grouped decile labels.
        group_map (dict): Dictionary mapping decile numbers to group names.

    Returns:
        pd.DataFrame: Updated DataFrame with the new grouped column.
    """
    df_grouped = df_deciles.copy()
    df_grouped[grouped_col_name] = df_grouped[decile_col_name].map(group_map)
    return df_grouped


def summarize_grouped_deciles(df_grouped, grouped_col, continuous_variable, target_col, prefix="Grouped_"):
    """
    Summarizes statistics for newly grouped deciles, including numerical ranges, category counts, 
    and category proportions.

    Parameters:
        df_grouped (pd.DataFrame): DataFrame containing the grouped decile column.
        grouped_col (str): Name of the column containing the grouped decile categories.
        continuous_variable (str): Name of the original continuous variable.
        target_col (str): Name of the categorical target variable.
        prefix (str, optional): Prefix for column names to differentiate grouped statistics. 
                                Default is 'Grouped_'.

    Returns:
        dict: A dictionary containing:
            - 'statistics' (pd.DataFrame): Min, max, and count for each grouped decile.
            - 'counts' (pd.DataFrame): Frequency of each category in each grouped decile.
            - 'proportions' (pd.DataFrame): Proportion of each category within each grouped decile.
            - 'df' (pd.DataFrame): Final consolidated table with all the above information.
    """
    stats = statistics_by_decile(df_grouped, grouped_col, continuous_variable)
    stats = rename_decile_summary(stats, prefix)
    stats[f"{prefix}Proportion"] = calculate_decile_proportions(stats, f"{prefix}Count", f"{prefix}Proportion")

    counts = rename_count_columns(count_categories_by_decile(df_grouped, grouped_col, target_col))
    proportions = rename_prop_columns(calculate_category_proportions(df_grouped, grouped_col, target_col))

    df_final = pd.concat([stats, counts, proportions], axis=1)

    return {
        "statistics": stats,
        "counts": counts,
        "proportions": proportions,
        "df": df_final
    }





