import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv("Top_Tech_House_Songs_From_Playlists.csv")

# Key mapping
key_mapping = {
    0: 'C', 1: 'C♯ / D♭', 2: 'D', 3: 'D♯ / E♭', 4: 'E', 5: 'F',
    6: 'F♯ / G♭', 7: 'G', 8: 'G♯ / A♭', 9: 'A', 10: 'A♯ / B♭', 11: 'B'
}
data['Key_Name'] = data['Key'].map(key_mapping)

# Sidebar Filters
st.sidebar.title("Filters")
key_filter = st.sidebar.multiselect(
    "Filter by Key(s)", 
    options=data['Key_Name'].unique(), 
    default=data['Key_Name'].unique()
)
tempo_range = st.sidebar.slider(
    "Filter by Tempo Range (BPM)", 
    min_value=int(data['Tempo'].min()), 
    max_value=int(data['Tempo'].max()), 
    value=(120, 130)
)

# Apply Filters
filtered_data = data[
    (data['Key_Name'].isin(key_filter)) & 
    (data['Tempo'] >= tempo_range[0]) & 
    (data['Tempo'] <= tempo_range[1])
]

# Dropdown Menu for Navigation
st.title("🎶 Tech House Song Analysis Dashboard")
page = st.selectbox(
    "Select a Section",
    ["Dataset Overview", "Key and Tempo Insights", "Feature Exploration", "Dynamic Song Ranking"]
)

if page == "Dataset Overview":
    # Dataset Overview
    st.subheader("Dataset Overview")
    st.write(filtered_data)

elif page == "Key and Tempo Insights":
    # Key and Tempo Insights
    st.subheader("Key and Tempo Insights")
    st.markdown("### Key Distribution")
    key_counts = filtered_data['Key_Name'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=key_counts.index, y=key_counts.values, ax=ax)
    ax.set_title("Key Distribution")
    ax.set_xlabel("Key")
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.markdown("### Tempo Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_data['Tempo'], bins=20, kde=True, ax=ax)
    ax.set_title("Tempo Distribution")
    ax.set_xlabel("Tempo (BPM)")
    ax.set_ylabel("Count")
    st.pyplot(fig)

elif page == "Feature Exploration":
    # Feature Exploration
    st.subheader("Feature Exploration")
    feature = st.selectbox("Select Feature", options=["Energy", "Danceability", "Valence", "Speechiness"])
    fig, ax = plt.subplots()
    sns.histplot(filtered_data[feature], kde=True, ax=ax)
    ax.set_title(f"Distribution of {feature}")
    ax.set_xlabel(feature)
    st.pyplot(fig)

elif page == "Dynamic Song Ranking":
    # Dynamic Song Ranking
    st.subheader("Dynamic Song Ranking")
    rank_feature = st.selectbox(
        "Select a Feature to Rank Songs By", 
        options=["Popularity", "Danceability", "Energy", "Valence", "Speechiness"]
    )
    num_songs = st.slider(
        "Number of Songs to Display", 
        min_value=5, 
        max_value=20, 
        value=10
    )
    ranked_songs = filtered_data.nlargest(num_songs, rank_feature)[["Track Name", "Artist Name", rank_feature]]
    st.markdown(f"#### Top {num_songs} Songs Ranked by {rank_feature}")
    st.write(ranked_songs)

# Footer
st.markdown("### Explore more insights using the dropdown menu!")
