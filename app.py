# app.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- Streamlit Page Setup ---
st.set_page_config(page_title="IPL Data Analysis", layout="wide")
st.title("🏏 IPL Data Analysis (2008 - 2019)")

# --- Load Data ---
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries2.csv")  # cleaned deliveries
overwise = pd.read_csv("overwise statistics without super over.csv")

# --- Sidebar Menu ---
st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choose Analysis:", 
                              ["Team Wins", "Top Players", "Overwise Trends", "Season-wise Analysis"])

# --- Team Wins Analysis ---
if option == "Team Wins":
    st.header("Team-wise Wins in IPL")
    
    wins = matches['winner'].value_counts()
    
    st.subheader("Bar Chart of Wins per Team")
    st.bar_chart(wins)
    
    st.subheader("Top 5 Teams by Wins")
    st.dataframe(wins.head())

# --- Top Players Analysis ---
elif option == "Top Players":
    st.header("Top Players Stats")
    
    # Top Run Scorers
    st.subheader("🏏 Top Run Scorers")
    runs = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False)
    st.bar_chart(runs.head(10))
    st.dataframe(runs.head(10))
    
    # Top Wicket Takers
    st.subheader("🎯 Top Wicket Takers")
    wickets = deliveries[deliveries['dismissal_kind'].notna()].groupby('bowler').size().sort_values(ascending=False)
    st.bar_chart(wickets.head(10))
    st.dataframe(wickets.head(10))

# --- Overwise Trends Analysis ---
elif option == "Overwise Trends":
    st.header("Overwise Run Trends")
    
    # Replace 'runs' with your exact column name from overwise CSV if different
    y_column = 'runs'  
    team_column = 'batting_team'  
    x_column = 'over'
    
    plt.figure(figsize=(12,6))
    sns.lineplot(data=overwise, x=x_column, y=y_column, hue=team_column)
    plt.title("Runs per Over by Team")
    plt.xlabel("Over")
    plt.ylabel("Runs")
    st.pyplot(plt)
    
    st.write("You can see how teams score over each over in a typical IPL match.")

# --- Season-wise Analysis ---
elif option == "Season-wise Analysis":
    st.header("🏆 Season-wise Analysis")
    
    # Top Team per Season
    st.subheader("Top Team per Season")
    top_teams = matches.groupby('season')['winner'].agg(lambda x: x.value_counts().idxmax())
    st.dataframe(top_teams)
    
    st.subheader("Overall Wins of Top Teams")
    st.bar_chart(top_teams.value_counts())

    # Top Run Scorer per Season
    st.subheader("Top Run Scorer per Season")
    
    # Merge deliveries2 with matches to get season info
    deliveries_season = deliveries.merge(matches[['id','season']], left_on='match_id', right_on='id')
    
    top_batsmen = deliveries_season.groupby(['season','batsman'])['batsman_runs'].sum().reset_index()
    
    # Pick top scorer per season
    top_scorer_per_season = top_batsmen.loc[top_batsmen.groupby('season')['batsman_runs'].idxmax()]
    
    st.dataframe(top_scorer_per_season[['season','batsman','batsman_runs']])
    
    # Bar chart of runs for top scorer per season
    st.bar_chart(top_scorer_per_season.set_index('batsman')['batsman_runs'])

# --- Footer ---
st.sidebar.write("Made with ❤️ using Streamlit & IPL Data")
