import plotly.graph_objects as go
import plotly.express as px

def create_rent_comparison_chart(current_rent, market_rate, comps):
    """Create a bar chart comparing current rent with market rate"""
    rents = [current_rent, market_rate]
    labels = ['Your Rent', 'Market Average']

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=rents,
            marker_color=['#FF4B4B', '#1F77B4']
        )
    ])

    fig.update_layout(
        title='Rent Comparison',
        yaxis_title='Monthly Rent ($)',
        showlegend=False
    )

    return fig

def create_trend_chart(market_data):
    """Create a line chart showing rental trends"""
    if not market_data or 'seasonal_patterns' not in market_data:
        return go.Figure()  # Return empty figure if no data

    seasonal_patterns = market_data.get('seasonal_patterns', {})
    seasons = list(seasonal_patterns.keys())
    changes = [seasonal_patterns[season] * 100 for season in seasons]  # Convert to percentage

    fig = go.Figure(data=[
        go.Scatter(
            x=seasons,
            y=changes,
            mode='lines+markers',
            line=dict(color='#FF4B4B')
        )
    ])

    fig.update_layout(
        title='Seasonal Rent Patterns',
        yaxis_title='Price Change (%)',
        showlegend=False
    )

    return fig

def create_market_position_gauge(value_score):
    """Create a gauge chart showing the value score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF4B4B"},
            'steps': [
                {'range': [0, 33], 'color': "#EF553B"},
                {'range': [33, 66], 'color': "#FFA15A"},
                {'range': [66, 100], 'color': "#00CC96"}
            ]
        }
    ))

    fig.update_layout(
        title="Value Score",
        height=300
    )

    return fig

def create_price_metrics_chart(price_metrics, market_data):
    """Create a radar chart showing various price metrics"""
    categories = ['Value Score', 'Market Percentile', 'Price Stability', 'Negotiation Power']

    # Calculate negotiation power based on market data
    vacancy_rate = market_data.get('vacancy_rate', 0) * 100
    yearly_change = market_data.get('yearly_change', 0) * 100
    negotiation_power = min(100, max(0, 
        50 + (vacancy_rate * 3) - (yearly_change * 2)
    ))

    values = [
        price_metrics['value_score'],
        price_metrics['market_percentile'],
        100 - (price_metrics['price_volatility'] * 100),  # Convert volatility to stability
        negotiation_power
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='#FF4B4B'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Market Position Analysis"
    )

    return fig