import plotly.graph_objects as go

import plotly.graph_objects as go

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

