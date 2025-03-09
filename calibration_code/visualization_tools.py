import plotly.graph_objects as go
import plotly.express as px

def add_trace_to_figure(fig, df, x_column, y_column, chart_type, secondary_y, custom_colors):
    """
    Adds a line or bar trace to a Plotly figure.
    
    Parameters:
    - fig (go.Figure): Plotly figure to update.
    - df (pd.DataFrame): DataFrame containing the data.
    - x_column (str): Column for the X-axis.
    - y_column (str): Column for the Y-axis.
    - chart_type (str): Type of chart ('line' or 'bar').
    - secondary_y (bool): Whether to use a secondary Y-axis.
    - custom_colors (dict, optional): Dictionary mapping column names to specific colors.
    """
    color = custom_colors.get(y_column, None) if custom_colors else None
    
    if chart_type == 'line':
        fig.add_trace(go.Scatter(
            x=df[x_column], y=df[y_column],
            mode='lines', name=y_column,
            line=dict(color=color),
            yaxis='y2' if secondary_y else 'y1'
        ))
    elif chart_type == 'bar':
        fig.add_trace(go.Bar(
            x=df[x_column], y=df[y_column],
            name=y_column,
            marker=dict(color=color),
            yaxis='y2' if secondary_y else 'y1'
        ))

def configure_layout(fig, title, x_title, y_title, y2_title, width, height):
    """
    Configures the layout of a Plotly figure.
    
    Parameters:
    - fig (go.Figure): Plotly figure to update.
    - title (str): Chart title.
    - x_title (str): Label for the X-axis.
    - y_title (str): Label for the primary Y-axis.
    - y2_title (str, optional): Label for the secondary Y-axis.
    - width (int): Width of the figure.
    - height (int): Height of the figure.
    """
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis=dict(title=y_title),
        yaxis2=dict(title=y2_title, overlaying='y', side='right', showgrid=False) if y2_title else None,
        width=width,
        height=height,
        legend=dict(orientation='h', x=0.5, y=-0.2, xanchor='center', yanchor='top')
    )

def plot_interactive_chart(
    df, y_columns, x_column=None, chart_types=None, secondary_y=None,
    title="Interactive Chart", x_title="X-Axis", y_title="Y-Axis", y2_title=None,
    width=900, height=500, custom_colors=None
):
    """
    Creates an interactive Plotly chart with customizable line and bar plots.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data to plot.
    - y_columns (list): List of column names to plot on the Y-axis.
    - x_column (str, optional): Column to use for the X-axis. If None, the index is used.
    - chart_types (dict, optional): Dictionary specifying the type of chart for each column ('line' or 'bar').
    - secondary_y (list, optional): List of columns to be plotted on a secondary Y-axis.
    - title (str): Chart title.
    - x_title (str): Label for the X-axis.
    - y_title (str): Label for the primary Y-axis.
    - y2_title (str, optional): Label for the secondary Y-axis.
    - width (int): Width of the figure.
    - height (int): Height of the figure.
    - custom_colors (dict, optional): Dictionary mapping column names to specific colors.
    
    Returns:
    - A Plotly interactive figure.
    """
    if x_column is None:
        df = df.reset_index()
        x_column = df.columns[0]
    
    fig = go.Figure()
    
    for y_col in y_columns:
        chart_type = chart_types.get(y_col, 'line') if chart_types else 'line'
        sec_y = y_col in secondary_y if secondary_y else False
        add_trace_to_figure(fig, df, x_column, y_col, chart_type, sec_y, custom_colors)
    
    configure_layout(fig, title, x_title, y_title, y2_title, width, height)
    return fig


def sort_dataframe(df, x_column, y_column, order="none"):
    """
    Sorts a DataFrame based on a specific column.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        x_column (str): Column to use as x-axis categories.
        y_column (str): Column used for sorting.
        order (str, optional): Sorting order. Options:
            - "asc" (ascending order)
            - "desc" (descending order)
            - "none" (no sorting, default)

    Returns:
        pd.DataFrame: Sorted DataFrame.
    """
    if order == "asc":
        df = df.sort_values(by=y_column, ascending=True)
    elif order == "desc":
        df = df.sort_values(by=y_column, ascending=False)
    return df


def plot_categorical_proportions(df, x_column, y_columns, stacked=False, 
                                 title="Proporción de Categoría por Variable", 
                                 x_title="Categoría", y_title="Proporción", 
                                 legend_title="Grupo", colors=None, 
                                 width=1000, height=600, sort_order="none", sort_by=None):
    """
    Plots categorical proportions using Plotly.

    Parameters:
        df (pd.DataFrame): DataFrame containing proportion data.
        x_column (str): Column name to use as x-axis categories.
        y_columns (list): List of column names to use as y-axis series.
        stacked (bool, optional): Whether to stack bars. Defaults to False.
        title (str, optional): Title of the plot. Defaults to "Proporción de Categoría por Variable".
        x_title (str, optional): Label for x-axis. Defaults to "Categoría".
        y_title (str, optional): Label for y-axis. Defaults to "Proporción".
        legend_title (str, optional): Title of the legend. Defaults to "Grupo".
        colors (dict, optional): Dictionary mapping column names to colors. Defaults to None.
        width (int, optional): Width of the figure. Defaults to 1000.
        height (int, optional): Height of the figure. Defaults to 600.
        sort_order (str, optional): Sorting order ("asc", "desc", "none"). Defaults to "none".
        sort_by (str, optional): Column name to sort by (should be in y_columns). Defaults to None.

    Returns:
        go.Figure: Plotly figure object.
    """
    # Aplicar ordenamiento si es necesario
    if sort_by and sort_by in y_columns:
        df = sort_dataframe(df, x_column, sort_by, sort_order)

    fig = go.Figure()

    for col in y_columns:
        fig.add_trace(go.Bar(
            x=df[x_column], 
            y=df[col], 
            name=col, 
            marker_color=colors.get(col) if colors else None
        ))

    fig.update_layout(
        barmode="stack" if stacked else "group",
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        legend_title=legend_title,
        width=width,
        height=height,
        xaxis=dict(tickangle=45),
        template="plotly_white",
        legend=dict(
            orientation="h",    
            yanchor="bottom",   
            y=-0.3,             
            xanchor="center",   
            x=0.5               
        )
    )

    return fig




