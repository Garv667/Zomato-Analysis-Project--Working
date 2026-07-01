import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page config ----------
st.set_page_config(page_title="Zomato Restaurant Analysis", layout="wide")
sns.set_style("whitegrid")

# ---------- Load data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Zomato-data.csv")
    # Clean rate column: "4.1/5" -> 4.1
    df["rate"] = df["rate"].astype(str).str.replace("/5", "", regex=False)
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df = df.rename(columns={"approx_cost(for two people)": "approx_cost",
                             "listed_in(type)": "type"})
    return df

df = load_data()

st.title("🍽️ Zomato Restaurant Analysis")
st.caption("Explore restaurant ratings, cost, and booking trends from the Zomato dataset")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

type_options = sorted(df["type"].dropna().unique())
selected_types = st.sidebar.multiselect("Restaurant Type", type_options, default=type_options)

online_order = st.sidebar.selectbox("Online Order", ["All", "Yes", "No"])
book_table = st.sidebar.selectbox("Table Booking", ["All", "Yes", "No"])

cost_min, cost_max = int(df["approx_cost"].min()), int(df["approx_cost"].max())
cost_range = st.sidebar.slider("Approx Cost for Two (₹)", cost_min, cost_max, (cost_min, cost_max))

rate_min, rate_max = float(df["rate"].min()), float(df["rate"].max())
rate_range = st.sidebar.slider("Rating", rate_min, rate_max, (rate_min, rate_max))

# ---------- Apply filters ----------
filtered = df[
    df["type"].isin(selected_types)
    & df["approx_cost"].between(cost_range[0], cost_range[1])
    & df["rate"].between(rate_range[0], rate_range[1])
]

if online_order != "All":
    filtered = filtered[filtered["online_order"] == online_order]
if book_table != "All":
    filtered = filtered[filtered["book_table"] == book_table]

# ---------- Key metrics ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Restaurants", len(filtered))
col2.metric("Avg Rating", f"{filtered['rate'].mean():.2f}" if len(filtered) else "—")
col3.metric("Avg Cost (for 2)", f"₹{filtered['approx_cost'].mean():.0f}" if len(filtered) else "—")
col4.metric("Total Votes", f"{filtered['votes'].sum():,}")

st.divider()

if filtered.empty:
    st.warning("No restaurants match the selected filters. Try widening your filter ranges.")
else:
    # ---------- Charts ----------
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Rating Distribution")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.histplot(filtered["rate"], bins=15, kde=True, color="#e23744", ax=ax)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    with row1_col2:
        st.subheader("Cost vs Rating")
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.scatterplot(
            data=filtered, x="approx_cost", y="rate",
            hue="type", size="votes", sizes=(20, 200), alpha=0.7, ax=ax
        )
        ax.set_xlabel("Approx Cost for Two (₹)")
        ax.set_ylabel("Rating")
        ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
        st.pyplot(fig)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Restaurant Type Breakdown")
        fig, ax = plt.subplots(figsize=(5, 4))
        type_counts = filtered["type"].value_counts()
        ax.pie(type_counts, labels=type_counts.index, autopct="%1.0f%%",
               colors=sns.color_palette("Set2"))
        ax.set_ylabel("")
        st.pyplot(fig)

    with row2_col2:
        st.subheader("Online Order & Table Booking")
        fig, ax = plt.subplots(figsize=(5, 4))
        summary = pd.DataFrame({
            "Online Order": filtered["online_order"].value_counts(),
            "Table Booking": filtered["book_table"].value_counts()
        }).fillna(0)
        summary.plot(kind="bar", ax=ax, color=["#e23744", "#2c2c2c"])
        ax.set_ylabel("Count")
        ax.set_xlabel("")
        plt.xticks(rotation=0)
        st.pyplot(fig)

    st.divider()

    # ---------- Top restaurants ----------
    st.subheader("🏆 Top Rated Restaurants")
    top_n = st.slider("Show top N restaurants by rating", 5, 30, 10)
    top_df = filtered.sort_values(["rate", "votes"], ascending=False).head(top_n)
    st.dataframe(
        top_df[["name", "type", "rate", "votes", "approx_cost", "online_order", "book_table"]],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ---------- Raw data explorer ----------
    st.subheader("🔎 Data Explorer")
    search = st.text_input("Search by restaurant name")
    display_df = filtered.copy()
    if search:
        display_df = display_df[display_df["name"].str.contains(search, case=False, na=False)]

    st.dataframe(
        display_df.sort_values("name").reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing {len(display_df)} of {len(df)} total restaurants")

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_zomato_data.csv", "text/csv")
