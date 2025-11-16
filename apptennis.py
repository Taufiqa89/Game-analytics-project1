import streamlit as st

import pandas as pd

import mysql.connector


connection= mysql.connector.connect(
 host= "localhost",
 user= "root",
 password=" ",
 database="tennis_data"
)

print(connection)
mycursor = connection.cursor()


# Play the audio in Streamlit
audio_file = open("C:/Users/taufi/Desktop/Main_boot/Mini_project1/movement-200697.mp3", "rb")
audio_bytes = audio_file.read()
st.audio(audio_bytes, format="audio/mp3", autoplay=True)


#Mainpage bgcolor
def set_bg_gradient(color1, color2):
    css_code = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(to right, {color1}, {color2});
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

#Gradient from orange to pink
set_bg_gradient("#FF4500", "#FFB6C1")


#sidebar bgcolor
def set_sidebar_gradient(color1, color2):
    css_code = f"""
    <style>
    [data-testid="stSidebar"] {{
        background: linear-gradient(to bottom, {color1}, {color2});
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

#Sidebar gradient from blue to purple
set_sidebar_gradient("#8e44ad", "#87CEFA")

#Title with custom color
st.markdown("<h1 style='color: white;'>🎾TENNIS SPORTS EXPLORER</h1>", unsafe_allow_html=True)
st.write("\n")

st.markdown("<h2 style='color: white;'>🏃‍♂️🏃‍♀️COMPETITORS INFO</h2>", unsafe_allow_html=True)

mycursor.execute("select * from competitors ")
data=mycursor.fetchall()
df=pd.DataFrame(data,columns=mycursor.column_names)

#1.Homepage Dashboard:
# Total number of competitors.

mycursor.execute("""SELECT c.name,r.ranks,r.points
    FROM competitors c JOIN competitor_rankings r ON 
    c.competitor_id = r.competitor_id""")
D1=mycursor.fetchall()
A1=pd.DataFrame(D1,columns=mycursor.column_names)

d1=df["competitor_id"].count()
st.sidebar.markdown(f"<h3 style='color: white; font-weight: bold;'>👥 TOTAL NO OF COMPETITORS: {d1}</h3>", unsafe_allow_html=True)

#Numberof countries represented.

d2=df["country"].nunique()
st.sidebar.markdown(f"<h3 style='color: white; font-weight: bold;'>🌍 TOTAL NUMBER OF COUNTRIES: {d2}</h3>", unsafe_allow_html=True)

#Highest points scored by a competitor.
st.sidebar.markdown(f"<h3 style='color: white; font-weight: bold;'>🏆 HIGHEST POINTS SCORED:</h3>", unsafe_allow_html=True)

mycursor.execute("""SELECT c.name, MAX(r.points) FROM competitors c
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
    GROUP BY c.name""")

d3=mycursor.fetchall()
A1=pd.DataFrame(d3,columns=mycursor.column_names)
st.sidebar.dataframe(A1,hide_index=True)

#2.Search and Filter Competitors:

#Allow users to search for a competitor by name.

mycursor.execute("""SELECT c.competitor_id, c.name,c.country,
        c.country_code,c.abbreviation,r.ranks,r.points from competitors c 
        JOIN competitor_rankings r ON c.competitor_id=r.competitor_id""")
b1=mycursor.fetchall()
b2=pd.DataFrame(b1,columns=mycursor.column_names)
st.dataframe(b2,hide_index=True)

st.markdown("<h2 style='color: white;'>🔎SEARCH AND FILTER COMPETITORS:</h2>", unsafe_allow_html=True)
search_name = st.text_input("")

if search_name:
    filtered_df = b2[b2['name'].str.contains(search_name, case=False, na=False)]
else:
    filtered_df = b2

st.dataframe(filtered_df, hide_index=True)

#Filter competitors by rank range, country, or points threshold.
st.markdown("<h4 style='color: white;'>Competitors by Rank Range:</h4>", unsafe_allow_html=True)
min_rank, max_rank = st.slider("", 1, 1000, (1, 100))
filtered_df = b2[(b2['ranks'] >= min_rank) & (b2['ranks'] <= max_rank)]


st.dataframe(filtered_df, hide_index=True)

st.markdown("<h4 style='color: white;'>Filter Competitors by country:</h4>", unsafe_allow_html=True)
country = st.selectbox("", b2['country'].unique())
filtered_df = b2[b2['country'] == country]

st.dataframe(filtered_df)

#3.Competitor Details Viewer:
#Display detailed information about a selected competitor, including:
#Rank, movement, competitions played, and country.


# Select a competitor

mycursor.execute("""SELECT c.competitor_id, c.name,c.country,
            r.ranks,r.movement,r.competitions_played from competitors c JOIN competitor_rankings r ON c.competitor_id=r.competitor_id""")

c1 = mycursor.fetchall()
c2 = pd.DataFrame(c1, columns=mycursor.column_names)
st.markdown("<h2 style='color: white;'>📋COMPETITOR DETAILS VEIWER:</h2>", unsafe_allow_html=True)
competitor = st.selectbox("", c2['name'].unique())
filtered_df = c2[c2['name'] == competitor]
st.dataframe(filtered_df, hide_index=True)

#4.Country-Wise Analysis:
#List countries with the total number of competitors and their average points.

mycursor.execute("""
    SELECT c.country, COUNT(c.competitor_id) AS total_competitors, 
    AVG(r.points) AS average_points FROM competitors c 
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
    GROUP BY c.country
""")
country_data = mycursor.fetchall()

# Convert SQL results into a DataFrame
df_country = pd.DataFrame(country_data, columns=mycursor.column_names)

# Display country-wise competitor count and average points
st.markdown("<h2 style='color: white;'>🌍COUNTRY-WISE ANALYSIS:</h2>", unsafe_allow_html=True)

st.dataframe(df_country, hide_index=True)


#Leaderboards

st.markdown("<h2 style='color: white;'>🏆 LEADERBOARDS</h2>", unsafe_allow_html=True)

# Create columns for layout
col1, col2 = st.columns([1,1])

# **Top-Ranked Competitors**
with col1:
    st.markdown("<h4 style='color: white;'>🎖️Top-Ranked Competitors</h4>", unsafe_allow_html=True)
    
    mycursor.execute("""
        SELECT c.name, c.country, r.ranks, r.points
        FROM competitors c 
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        ORDER BY r.ranks ASC
        LIMIT 10
    """)
    
    top_rank = mycursor.fetchall()
    top_rank_df = pd.DataFrame(top_rank, columns=["Name", "Country", "Ranks", "Points"])
    st.dataframe(top_rank_df, hide_index=True)

# **Competitors with the Highest Points**
with col2:
    st.markdown("<h4 style='color: white;'>💯 Highest Points Competitors</h4>", unsafe_allow_html=True)
    
    mycursor.execute("""
        SELECT c.name, c.country, r.ranks, r.points
        FROM competitors c 
        JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
        ORDER BY r.points DESC 
        LIMIT 10
    """)
    
    competitors_with_hp = mycursor.fetchall()
    top_points = pd.DataFrame(competitors_with_hp, columns=["Name", "Country", "Rank", "Points"])
    st.dataframe(top_points, hide_index=True)


# Sidebar - Query Selection

query_options = {
    "List all competitions along with their category": """
        SELECT c.competition_name, cat.category_name
        FROM competitions c 
        JOIN categories cat ON c.category_id = cat.category_id;
    """,
    "Count the number of competitions in each category": """
        SELECT cat.category_name, COUNT(c.competition_id) AS competition_count
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name;
    """,
    "Find all competitions of type 'doubles'": """
        SELECT competition_name, type 
        FROM Competitions 
        WHERE type = 'doubles';
    """,
    "Get competitions in a specific category (e.g., ITF Men)": """
        SELECT c.competition_name, cat.category_name
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        WHERE cat.category_name = 'ITF Men';
    """,
    "Identify parent competitions and their sub-competitions": """
        SELECT a.competition_id, a.parent_id, b.category_name
        FROM competitions a 
        JOIN categories b ON a.category_id = b.category_id;
    """,
    "Analyze competition types by category": """
        SELECT cat.category_name, c.type, COUNT(c.competition_id) AS count
        FROM Competitions c
        JOIN Categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name, c.type;
    """,
    "List all venues with complex names": """
        SELECT venue_name, complex_name
        FROM Venues
        JOIN Complexes ON Venues.complex_id = Complexes.complex_id;
    """,
    "Find competitors ranked in the top 5": """
        SELECT c.competitor_id, c.name, r.ranks, r.points
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
        WHERE r.ranks <= 5
        ORDER BY r.ranks;
    """,
    "List competitors with no rank movement": """
        SELECT c.competitor_id, c.name, r.ranks, r.movement
        FROM Competitors c
        JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
        WHERE r.movement = 0;
    """
}

st.sidebar.markdown("<h3 style='color: white;'>Select a query to run:</h3>", unsafe_allow_html=True)
selected_query = st.sidebar.selectbox("", list(query_options.keys()))

# Execute query and display results
if selected_query:
    query = query_options[selected_query]
    mycursor.execute(query)
    data = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    df = pd.DataFrame(data, columns=columns)

st.markdown(f"<h3 style='color: white;'>{selected_query}</h3>", unsafe_allow_html=True)

st.dataframe(df, hide_index=True)
