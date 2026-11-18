
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="IPL Super XI Selector",
    page_icon="🏏",
    layout="wide"
)

base = Path(__file__).resolve().parent

# =====================================
# LOAD DATA
# =====================================

@st.cache_data
def load_data():
    return pd.read_csv(base / "final_super_xi.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("final_super_xi.csv not found!")
    st.stop()

# =====================================
# DASHBOARD HEADER
# =====================================

st.title("🏏 IPL SUPER XI SELECTOR")
st.markdown(
    "### Smart Cricket Analytics & Player Performance Dashboard"
)

st.divider()

# =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.title("🎯 Dashboard Filters")

roles = ["All"] + sorted(df["role"].dropna().unique().tolist())

selected_role = st.sidebar.selectbox(
    "Select Player Role",
    roles
)

search = st.sidebar.text_input(
    "Search Player",
    placeholder="Enter player name"
)

# Apply filters
filtered = df.copy()

if selected_role != "All":
    filtered = filtered[
        filtered["role"] == selected_role
    ]

if search:
    filtered = filtered[
        filtered["player_name"].str.contains(
            search, case=False, na=False
        )
    ]

# =====================================
# KEY PERFORMANCE INDICATORS
# =====================================

st.subheader("📊 Team Performance Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Selected Players", len(df))

c2.metric(
    "Total Runs",
    int(filtered["batting_runs"].sum())
)

c3.metric(
    "Total Wickets",
    int(filtered["wickets"].sum())
)

c4.metric(
    "Average Strike Rate",
    round(filtered["strike_rate"].mean(), 2)
    if not filtered.empty else 0
)

st.divider()

# =====================================
# PLAYER TABLE
# =====================================

st.subheader("🏆 IPL Super XI Players")

if filtered.empty:
    st.warning("No players match your filters.")
else:
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

# =====================================
# TOP 5 PLAYERS
# =====================================

st.subheader("⭐ Top 5 Players")

top5 = df.nlargest(5, "total_score")

fig_top = px.bar(
    top5,
    x="player_name",
    y="total_score",
    color="total_score",
    title="Top 5 Players by Performance Score",
    text_auto=".2f"
)

st.plotly_chart(fig_top, use_container_width=True)

# =====================================
# BATTING ANALYSIS
# =====================================

st.subheader("🏏 Batting Performance")

col1, col2 = st.columns(2)

with col1:
    fig_runs = px.bar(
        filtered,
        x="player_name",
        y="batting_runs",
        title="Runs Scored",
        color="batting_runs"
    )

    st.plotly_chart(fig_runs, use_container_width=True)

with col2:
    fig_sr = px.bar(
        filtered,
        x="player_name",
        y="strike_rate",
        title="Batting Strike Rate",
        color="strike_rate"
    )

    st.plotly_chart(fig_sr, use_container_width=True)

# =====================================
# BOWLING ANALYSIS
# =====================================

st.subheader("🎯 Bowling Performance")

col1, col2 = st.columns(2)

with col1:
    fig_wickets = px.bar(
        filtered,
        x="player_name",
        y="wickets",
        title="Wickets Taken",
        color="wickets"
    )

    st.plotly_chart(fig_wickets, use_container_width=True)

with col2:
    fig_bowl = px.bar(
        filtered,
        x="player_name",
        y="wickets_per_100_balls",
        title="Wickets Per 100 Balls",
        color="wickets_per_100_balls"
    )

    st.plotly_chart(fig_bowl, use_container_width=True)

# =====================================
# PLAYER COMPARISON
# =====================================

st.subheader("⚖️ Player Comparison")

player_options = df["player_name"].dropna().unique().tolist()

selected_players = st.multiselect(
    "Select players to compare",
    player_options,
    default=player_options[:2]
)

if selected_players:
    comparison = df[
        df["player_name"].isin(selected_players)
    ]

    comparison_chart = px.bar(
        comparison,
        x="player_name",
        y=["batting_runs", "wickets"],
        barmode="group",
        title="Runs and Wickets Comparison"
    )

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )

# =====================================
# TEAM COMPOSITION
# =====================================

st.subheader("👥 Team Composition")

role_chart = px.pie(
    df,
    names="role",
    title="Player Role Distribution",
    hole=0.45
)

st.plotly_chart(
    role_chart,
    use_container_width=True
)

# =====================================
# DOWNLOAD
# =====================================

st.divider()

st.subheader("📥 Download IPL Super XI")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Player Data",
    data=csv,
    file_name="IPL_Super_XI.csv",
    mime="text/csv"
)

st.success("IPL Super XI Dashboard is Ready!")

# =====================================
# IPL PLAYER COMPARISON ENGINE
# =====================================

st.divider()

st.header("⚖️ IPL Player Comparison Engine")

st.write(
    "Compare two selected Super XI players "
    "across batting, bowling and pressure performance."
)

players = sorted(df["player_name"].dropna().unique())

if len(players) >= 2:

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox(
            "Select First Player",
            players,
            index=0,
            key="compare_player1"
        )

    with col2:
        player2_options = [p for p in players if p != player1]

        player2 = st.selectbox(
            "Select Second Player",
            player2_options,
            index=0,
            key="compare_player2"
        )

    p1 = df[df["player_name"] == player1].iloc[0]
    p2 = df[df["player_name"] == player2].iloc[0]

    st.subheader("Player Statistics")

    metrics = [
        ("Total Runs", "batting_runs"),
        ("Strike Rate", "strike_rate"),
        ("Total Wickets", "wickets"),
        ("Wickets per 100 Balls", "wickets_per_100_balls"),
        ("Pressure Batting Score", "pressure_bat_score"),
        ("Pressure Bowling Score", "pressure_bowl_score"),
        ("Overall Performance Score", "total_score")
    ]

    for label, column in metrics:

        value1 = float(p1[column])
        value2 = float(p2[column])

        c1, c2, c3 = st.columns([2, 2, 2])

        c1.metric(
            f"{player1} - {label}",
            round(value1, 2)
        )

        c2.metric(
            f"{player2} - {label}",
            round(value2, 2)
        )

        if value1 > value2:
            winner = player1
        elif value2 > value1:
            winner = player2
        else:
            winner = "Tie"

        c3.metric("Better Performance", winner)

    # Comparison chart
    st.subheader("📊 Performance Comparison Chart")

    comparison = pd.DataFrame({
        "Metric": [
            "Batting Runs",
            "Strike Rate",
            "Wickets",
            "Wickets per 100 Balls",
            "Pressure Batting",
            "Pressure Bowling",
            "Overall Score"
        ],
        player1: [
            p1["batting_runs"],
            p1["strike_rate"],
            p1["wickets"],
            p1["wickets_per_100_balls"],
            p1["pressure_bat_score"],
            p1["pressure_bowl_score"],
            p1["total_score"]
        ],
        player2: [
            p2["batting_runs"],
            p2["strike_rate"],
            p2["wickets"],
            p2["wickets_per_100_balls"],
            p2["pressure_bat_score"],
            p2["pressure_bowl_score"],
            p2["total_score"]
        ]
    })

    comparison_long = comparison.melt(
        id_vars="Metric",
        var_name="Player",
        value_name="Performance"
    )

    fig_compare = px.bar(
        comparison_long,
        x="Metric",
        y="Performance",
        color="Player",
        barmode="group",
        title="Head-to-Head Player Comparison"
    )

    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )

    # Overall winner
    st.subheader("🏆 Comparison Result")

    if p1["total_score"] > p2["total_score"]:
        st.success(f"{player1} has the higher overall performance score!")
    elif p2["total_score"] > p1["total_score"]:
        st.success(f"{player2} has the higher overall performance score!")
    else:
        st.info("Both players have equal overall performance scores.")

else:
    st.warning("At least two players are required for comparison.")
