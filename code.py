import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

k = pd.read_csv("movies.csv")
l = pd.read_csv("movies2.csv")
netflix = pd.read_csv("Netflix Revenue.csv")
m = pd.read_csv("top_100_movies_full_best_effort.csv")

st.title("Analysis of Box Office Success in the Modern Film Industry")

st.divider()

st.markdown("""
            ***Guiding Questions***
            1. How have box office sales changed in the past ten years and how have they been impacted by streaming services?
            2. What genre produces the most box office hits?
            3. How does a movie’s budget effect its box office sales?
            4. How do IMDb ratings effect box office success?
            5. What actors and directors generate the most box office success?
            6. Do the actors and directors that generate the most revenue also win the most awards?
""")

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

st.markdown("""
**Analysis:** 
            These line charts compare the average revenue of top box office movies against the total revenue by Netflix from 1998 to 2024. Both revenues were rising until 2020, when
            the Covid-19 Pandemic forced people to stay away from going to the movies, causing the total average revenue of box office to decline while Netflix's revenue continued to 
            increase. Although Netflix’s growth could suggest a shift toward at-home viewing, it’s hard to fully determine its impact on box office performance since the pandemic disrupted 
            normal moviegoing behavior.""")

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

# Convert large values for cleaner chart labels
l['budget_m'] = l['budget'] / 1_000_000
l['revenue_b'] = l['revenue'] / 1_000_000_000

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
    x='budget_m',
    y='revenue_b',
    hover_name='title',
    hover_data={
        'year': True,
        'budget_m': ':$,.1f',
        'revenue_b': ':$,.2f'
    },
    title=f"Budget vs Revenue ({year_range[0]}–{year_range[1]})",
    labels={
        'budget_m': 'Budget (Millions USD)',
        'revenue_b': 'Revenue (Billions USD)'
    }
)

x = filtered_l['budget_m']
y = filtered_l['revenue_b']

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
    xaxis_title="Budget (Millions USD)",
    yaxis_title="Revenue (Billions USD)"
)

fig1.update_xaxes(tickprefix="$", ticksuffix="M")
fig1.update_yaxes(tickprefix="$", ticksuffix="B")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
**Analysis:** 
            There seems to be a positive relationship between a movie's budget and its revenue,
            as the regression line tends to slope upwards no matter the timeframe.""")

filtered_k['Primary Genre'] = filtered_k['Genres'].str.split(',').str[0]

genre_revenue = (
    filtered_k.groupby('Primary Genre', as_index=False)['$Worldwide']
    .sum()
    .sort_values('$Worldwide', ascending=False)
    .head(10)
)

genre_revenue['worldwide_b'] = genre_revenue['$Worldwide'] / 1_000_000_000

st.subheader(f"Top 10 Genres by Worldwide Revenue ({year_range[0]}–{year_range[1]})")

fig_genre = px.bar(
    genre_revenue,
    x='Primary Genre',
    y='worldwide_b',
    title=f"Top 10 Genres by Worldwide Revenue ({year_range[0]}–{year_range[1]})",
    labels={
        'Primary Genre': 'Genre',
        'worldwide_b': 'Worldwide Revenue (Billions USD)'
    }
)

fig_genre.update_traces(
    hovertemplate='Genre: %{x}<br>Total Revenue: $%{y:,.2f}B<extra></extra>'
)

fig_genre.update_layout(
    xaxis_title="Genre",
    yaxis_title="Worldwide Revenue (Billions USD)"
)

fig_genre.update_yaxes(tickprefix="$", ticksuffix="B")

st.plotly_chart(fig_genre, use_container_width=True)

st.markdown("""
**Analysis:** 
            Comedy films appear to generate higher total revenue among top box office hits
            prior to 2010, while action films dominate in the years after. Throughout the 
            time period analyzed, the top three most popular movie genres by box office hits were
            action, adventure, and comedy.""")

st.subheader(f"Rating vs Revenue ({year_range[0]}–{year_range[1]})")

fig_rating = px.scatter(
    filtered_l,
    x='vote_average',
    y='revenue_b',
    color='runtime',
    color_continuous_scale='viridis',
    hover_name='title',
    hover_data={
        'year': True,
        'vote_average': ':.1f',
        'runtime': True,
        'revenue_b': ':$,.2f'
    },
    title=f"Rating vs Revenue ({year_range[0]}–{year_range[1]})",
    labels={
        'vote_average': 'Rating (Out of 10)',
        'revenue_b': 'Revenue (Billions USD)',
        'runtime': 'Runtime (minutes)'
    }
)

x_rating = filtered_l['vote_average']
y_rating = filtered_l['revenue_b']

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
    hovertemplate='Title: %{hovertext}<br>Rating: %{x:.1f}/10<br>Revenue: $%{y:,.2f}B<br>Runtime: %{marker.color:.0f} min<extra></extra>'
)

fig_rating.update_layout(
    xaxis_title="Rating (Out of 10)",
    yaxis_title="Revenue (Billions USD)"
)

fig_rating.update_yaxes(tickprefix="$", ticksuffix="B")

st.plotly_chart(fig_rating, use_container_width=True)

st.markdown("""
**Analysis:** 
            It seems that ratings do not have much correlation with revenue. This could be because
            ratings were open for a longer time period, whereas revenue was only counted while movies
            were still playing in theatres. The weak relationship suggests that audience 
            ratings are not strong predictors of box office success""")

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

st.markdown("""
**Analysis:** 
            The actor and director analysis suggests that box office success and award recognition do not always align. While some actors and directors
            were top ten in both categories, such as Peter Jackson, Elijah Wood, and Leonardo DiCaprio, many others only appeared in one list or in
            lower spots in another category. Overall, these findings suggest that financial success and award recognition are related in some cases, but
            they are not perfectly correlated.
            """)

st.divider()

st.caption("Overview of highest grossing movies since 2000.")

k['Primary Genre'] = k['Genres'].str.split(",").str[0]

top5_by_year = (
    k.sort_values(['Year', '$Worldwide'], ascending=[True, False])
     .groupby('Year')
     .head(5)
)


fig2 = px.scatter(
    top5_by_year,
    x='Year',
    y='$Worldwide',
    size='Domestic %',
    color='Primary Genre',
    color_discrete_sequence=px.colors.qualitative.Set1,
    hover_name='Release Group',
    title='Top 5 Highest Grossing Movies by Year'
)


st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Data Sources")

st.markdown("""
- IMDb Top 250 Movies Dataset: https://www.kaggle.com/datasets/yaranathakur/imdb-top-250-movies  
- IMDb Top 100 Movies Dataset 2025 Edition: https://www.kaggle.com/datasets/shayanzk/imdb-top-100-movies-dataset-2025-edition  
- IMDb Films by Actor: https://www.kaggle.com/code/genghiskhaant/imdb-films-by-actor  
- Netflix Revenue and Usage Statistics: https://www.kaggle.com/datasets/adnananam/netflix-revenue-and-usage-statistics  
""")