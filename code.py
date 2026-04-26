import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

k = pd.read_csv('https://raw.githubusercontent.com/purslowj1/project/refs/heads/main/movies.csv')
l = pd.read_csv('https://raw.githubusercontent.com/purslowj1/project/refs/heads/main/movies2.csv')
netflix = pd.read_csv('https://raw.githubusercontent.com/purslowj1/project/refs/heads/main/Netflix%20Revenue.csv')
m = pd.read_csv('https://raw.githubusercontent.com/purslowj1/project/refs/heads/main/top_100_movies_full_best_effort.csv')

st.title("Analysis of Box Office Success in the Modern Film Industry")

st.divider()

st.caption("Evaluating the performance of box office revenue vs Netflix Revenue.")

k_avg = k.groupby('Year')['$Worldwide'].mean().reset_index()

fig_movies = px.line(
    k_avg,
    x='Year',
    y='$Worldwide',
    title='Average Worldwide Revenue by Year',
    markers=True
)

fig_movies.update_traces(
    hovertemplate='Year: %{x}<br>Average Worldwide Revenue: $%{y:,.2f}<extra></extra>'
)

fig_movies.add_annotation(
    x=2020,
    y=k_avg.loc[k_avg['Year'] == 2020, '$Worldwide'].values[0],
    text="COVID-19 dip",
    showarrow=True,
    arrowhead=2,
    ax=45,
    ay=-40
)

fig_movies.update_yaxes(tickformat="$,.0s")
fig_movies.update_layout(xaxis_title="Year", yaxis_title="Average Revenue")

fig_netflix = px.line(
    netflix,
    x='Year',
    y='Total Revenue (Millions)',
    title='Netflix Total Revenue by Year',
    markers=True
)

fig_netflix.update_traces(
    hovertemplate='Year: %{x}<br>Netflix Revenue: $%{y:,.2f}M<extra></extra>'
)

fig_netflix.update_layout(
    xaxis_title="Year",
    yaxis_title="Revenue (Millions)"
)

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_movies, use_container_width=True)

with col2:
    st.plotly_chart(fig_netflix, use_container_width=True)

st.divider()

st.caption("Exploring trends in revenue by genre, ratings, runtime, and budget over time.")

l['release_date'] = pd.to_datetime(l['release_date'], errors='coerce')
l['year'] = l['release_date'].dt.year
l['budget'] = pd.to_numeric(l['budget'], errors='coerce')
l['revenue'] = pd.to_numeric(l['revenue'], errors='coerce')
l['vote_average'] = pd.to_numeric(l['vote_average'], errors='coerce')
l['runtime'] = pd.to_numeric(l['runtime'], errors='coerce')
l['year'] = pd.to_numeric(l['year'], errors='coerce')
l = l.dropna(subset=['budget', 'revenue', 'year', 'vote_average', 'runtime'])
l['year'] = l['year'].astype(int)
l = l[(l['year'] >= 1990) & (l['year'] <= 2022)]

year_range = st.slider(
    "Select Year Range",
    min_value=1990,
    max_value=2022,
    value=(1990, 2022)
)

filtered_l = l[
    (l['year'] >= year_range[0]) &
    (l['year'] <= year_range[1])
].copy()

filtered_k = k[
    (k['Year'] >= year_range[0]) &
    (k['Year'] <= year_range[1])
].copy()

st.subheader(f"Budget vs Revenue ({year_range[0]}–{year_range[1]})")

fig1 = px.scatter(
    filtered_l,
    x='budget',
    y='revenue',
    hover_name='title',
    hover_data={'year': True, 'budget': ':$,.0f', 'revenue': ':$,.0f'},
    title=f"Budget vs Revenue ({year_range[0]}–{year_range[1]})",
    labels={
        'budget': 'Budget',
        'revenue': 'Revenue'
    }
)

x = filtered_l['budget']
y = filtered_l['revenue']

if len(filtered_l) > 1:
    slope, intercept = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = slope * x_line + intercept

    fig1.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name='Average Budget vs Revenue Regression'
        )
    )

fig1.update_layout(
    xaxis_title="Budget (Millions)",
    yaxis_title="Revenue (Millions)"
)

fig1.update_xaxes(tickformat="$,.0s")
fig1.update_yaxes(tickformat="$,.0s")

st.plotly_chart(fig1, use_container_width=True)

filtered_k['Primary Genre'] = filtered_k['Genres'].str.split(',').str[0]

genre_revenue = (
    filtered_k.groupby('Primary Genre', as_index=False)['$Worldwide']
    .sum()
    .sort_values('$Worldwide', ascending=False)
    .head(10)
)

st.subheader(f"Top 10 Genres by Worldwide Revenue ({year_range[0]}–{year_range[1]})")

fig_genre = px.bar(
    genre_revenue,
    x='Primary Genre',
    y='$Worldwide',
    title=f"Top 10 Genres by Worldwide Revenue ({year_range[0]}–{year_range[1]})"
)

fig_genre.update_traces(
    hovertemplate='Genre: %{x}<br>Total Revenue: $%{y:,.0f}<extra></extra>'
)

fig_genre.update_yaxes(tickformat="$,.0s")
fig_genre.update_layout(
    xaxis_title="Genre",
    yaxis_title="Worldwide Revenue"
)

st.plotly_chart(fig_genre, use_container_width=True)

st.subheader(f"Rating vs Revenue ({year_range[0]}–{year_range[1]})")

fig_rating = px.scatter(
    filtered_l,
    x='vote_average',
    y='revenue',
    color='runtime',
    color_continuous_scale='viridis',
    hover_name='title',
    hover_data={
        'year': True,
        'vote_average': ':.1f',
        'runtime': True,
        'revenue': ':$,.0f'
    },
    title=f"Rating vs Revenue ({year_range[0]}–{year_range[1]})",
    labels={
        'vote_average': 'Rating (Out of 10)',
        'revenue': 'Revenue',
        'runtime': 'Runtime (minutes)'
    }
)

x_rating = filtered_l['vote_average']
y_rating = filtered_l['revenue']

if len(filtered_l) > 1:
    m_rating, b_rating = np.polyfit(x_rating, y_rating, 1)
    x_line_rating = np.linspace(x_rating.min(), x_rating.max(), 100)
    y_line_rating = m_rating * x_line_rating + b_rating

    fig_rating.add_trace(
        go.Scatter(
            x=x_line_rating,
            y=y_line_rating,
            mode='lines',
            name='Regression Line'
        )
    )

fig_rating.update_traces(
    hovertemplate='Title: %{hovertext}<br>Rating: %{x:.1f}/10<br>Revenue: $%{y:,.0f}<br>Runtime: %{marker.color:.0f} min<extra></extra>'
)

fig_rating.update_yaxes(tickformat="$,.0s")
fig_rating.update_layout(
    xaxis_title="Rating (Out of 10)",
    yaxis_title="Revenue"
)

st.plotly_chart(fig_rating, use_container_width=True)

m["Box Office ($M)"] = pd.to_numeric(m["Box Office ($M)"], errors="coerce")
m["Oscars Won"] = pd.to_numeric(m["Oscars Won"], errors="coerce")
m = m.dropna(subset=["Box Office ($M)", "Oscars Won"])
m = m.drop_duplicates(subset=["Title"])

director_data = m.assign(Director=m["Director"].str.split("|")).explode("Director")
director_data["Director"] = director_data["Director"].str.strip()

actor_data = m.assign(Actor=m["Main Actor(s)"].str.split("|")).explode("Actor")
actor_data["Actor"] = actor_data["Actor"].str.strip()

top_director_revenue = (
    director_data.groupby("Director", as_index=False)["Box Office ($M)"]
    .sum()
    .sort_values("Box Office ($M)", ascending=False)
    .head(10)
)

top_actor_revenue = (
    actor_data.groupby("Actor", as_index=False)["Box Office ($M)"]
    .sum()
    .sort_values("Box Office ($M)", ascending=False)
    .head(10)
)

top_director_awards = (
    director_data.groupby("Director", as_index=False)["Oscars Won"]
    .sum()
    .sort_values("Oscars Won", ascending=False)
    .head(10)
)

top_actor_awards = (
    actor_data.groupby("Actor", as_index=False)["Oscars Won"]
    .sum()
    .sort_values("Oscars Won", ascending=False)
    .head(10)
)

st.divider()

st.caption("Identifying trends in box office success by actors and directors from the top 100 all time rated movies.")

st.subheader("Director Analysis (Top 100 Movies)")

col1, col2 = st.columns(2)

with col1:
    fig_director_revenue = px.bar(
        top_director_revenue,
        x="Box Office ($M)",
        y="Director",
        orientation="h",
        title="Top 10 Directors by Box Office Revenue",
        labels={"Box Office ($M)": "Box Office Revenue ($M)"}
    )
    fig_director_revenue.update_traces(
        hovertemplate="Director: %{y}<br>Revenue: $%{x:,.1f}M<extra></extra>"
    )
    fig_director_revenue.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_director_revenue, use_container_width=True)

with col2:
    fig_director_awards = px.bar(
        top_director_awards,
        x="Oscars Won",
        y="Director",
        orientation="h",
        title="Top 10 Directors by Oscars Won",
        labels={"Oscars Won": "Total Oscars Won"}
    )
    fig_director_awards.update_traces(
        hovertemplate="Director: %{y}<br>Oscars Won: %{x}<extra></extra>"
    )
    fig_director_awards.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_director_awards, use_container_width=True)

st.subheader("Actor Analysis (Top 100 Movies)")

col3, col4 = st.columns(2)

with col3:
    fig_actor_revenue = px.bar(
        top_actor_revenue,
        x="Box Office ($M)",
        y="Actor",
        orientation="h",
        title="Top 10 Actors by Box Office Revenue",
        labels={"Box Office ($M)": "Box Office Revenue ($M)"}
    )
    fig_actor_revenue.update_traces(
        hovertemplate="Actor: %{y}<br>Revenue: $%{x:,.1f}M<extra></extra>"
    )
    fig_actor_revenue.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_actor_revenue, use_container_width=True)

with col4:
    fig_actor_awards = px.bar(
        top_actor_awards,
        x="Oscars Won",
        y="Actor",
        orientation="h",
        title="Top 10 Actors by Oscars Won",
        labels={"Oscars Won": "Total Oscars Won"}
    )
    fig_actor_awards.update_traces(
        hovertemplate="Actor: %{y}<br>Oscars Won: %{x}<extra></extra>"
    )
    fig_actor_awards.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_actor_awards, use_container_width=True)

st.divider()

st.caption("Overview of highest grossing movies since 2000.")

k['Primary Genre'] = k['Genres'].str.split(",").str[0]

fig2 = px.scatter(
    k,
    x='Year',
    y='$Worldwide',
    size='Domestic %',
    color='Primary Genre',
    color_discrete_sequence=px.colors.qualitative.Set1,
    hover_name='Release Group',
    title='Highest Grossing Movie by Year'
)

st.plotly_chart(fig2, use_container_width=True)
