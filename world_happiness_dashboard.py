import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define the directory where your files are stored
data_directory = r"C:\M2DS\S3\Data_Viz\World-Happiness-Dashboard\Data\cleaned"

# Get a list of CSV files in the directory
csv_files = [f for f in os.listdir(data_directory) if f.endswith('.csv')]

# Extract years from filenames (assuming filenames are in the format 'cleaned_YYYY.csv')
years = [f.split('_')[1].split('.')[0] for f in csv_files]

# Custom CSS for full dark theme styling
st.markdown("""
    <style>
    /* Dark theme for entire dashboard */
    body {
        background-color: #2e3b4e; /* Dark background */
        color: #f0f0f0; /* Light text color */
    }

    /* Styling for headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ecf0f1; /* Light color for headers */
    }

    /* Styling for the main content */
    .intro-text {
        font-size: 20px;
        font-family: 'Arial', sans-serif;
        color: #ecf0f1;
        text-align: center;
        padding: 20px;
        background-color: #34495e; /* Dark background for intro text */
        border-radius: 10px;
        margin-bottom: 10px; /* Reduced margin */
    }

    /* Footer styling */
    .footer-text {
        font-size: 14px;
        color: #bdc3c7;
        text-align: center;
        margin-top: 10px; /* Reduced margin */
    }

    /* Styling for links */
    a {
        color: #1abc9c; /* Light green for links */
        text-decoration: none;
    }
    a:hover {
        color: #16a085; /* Darker green on hover */
    }

    /* Styling for Streamlit buttons and other elements */
    .stButton>button {
        background-color: #1abc9c;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #16a085; /* Darker green on hover */
    }

    /* Styling for Streamlit widgets */
    .stTextInput, .stNumberInput, .stSelectbox, .stMultiselect, .stTextArea {
        background-color: #34495e;
        color: #ecf0f1;
        border-radius: 5px;
        border: 1px solid #7f8c8d;
    }

    .stTextInput:focus, .stNumberInput:focus, .stSelectbox:focus, .stMultiselect:focus, .stTextArea:focus {
        border-color: #1abc9c;
    }

    </style>
""", unsafe_allow_html=True)

# Introduction message
st.markdown('<div class="intro-text">Welcome to the World Happiness Dashboard. This dashboard provides insights into global happiness rankings based on various factors.</div>', unsafe_allow_html=True)

# Data source as a clickable link
st.markdown('<div class="footer-text">Data source: <a href="https://www.kaggle.com/datasets/unsdsn/world-happiness/data" target="_blank">World Happiness Report Dataset</a></div>', unsafe_allow_html=True)

# Sidebar title with emoji
st.sidebar.markdown("## 🌍 World Happiness Dashboard")

# Scrollable menu to select the year in the sidebar
selected_year = st.sidebar.selectbox("Select a year:", years)

# Add a theme toggle for light/dark mode
theme = st.sidebar.radio("Select theme:", ("Dark", "Light"))

if theme == "Light":
    st.markdown('<style>body {background-color: #f0f0f0; color: #333;} .intro-text {background-color: #ecf0f1; color: #333;} .stButton>button {background-color: #16a085;} .stButton>button:hover {background-color: #1abc9c;}</style>', unsafe_allow_html=True)
else:
    st.markdown('<style>body {background-color: #2e3b4e; color: #f0f0f0;} .intro-text {background-color: #34495e; color: #ecf0f1;} .stButton>button {background-color: #1abc9c;} .stButton>button:hover {background-color: #16a085;}</style>', unsafe_allow_html=True)

# Load the dataframe for the selected year
file_path = os.path.join(data_directory, f"cleaned_{selected_year}.csv")
df = pd.read_csv(file_path)

# Display the head of the dataframe
st.write(f"### Data for the year {selected_year}:")
st.write(df.head())

# Display a message if required columns are missing
required_columns = ['Country', 'Happiness Score','Happiness Rank','Region','GDP per capita','Social support'
                    ,'Healthy life expectancy','Generosity','Dystopia Residual']
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"The following required columns are missing in the dataset: {', '.join(missing_columns)}")
else:
    col1, col2 = st.columns([4, 2])  # Create two columns with a 4:2 width ratio

    # Create a world map heatmap based on the Happiness Score
    with col1:
        fig = px.choropleth(
            df,
            locations="Country",
            locationmode="country names",
            color="Happiness Score",
            hover_name="Country",
            hover_data={  # Adding additional data to show when hovering
                "Region": True,  # Show Region
                "Happiness Rank": True,  # Show Happiness Rank
                "Happiness Score": True,  # Show Happiness Score
                "GDP per capita": True,  # Show GDP per Capita
                "Social support": True,  # Example of other columns
                "Healthy life expectancy": True,  # Example of another column
                "Generosity": True,  # Example of another column
                "Dystopia Residual": True,  # Example of another column
            },
            title=f"World Happiness Heatmap for {selected_year}",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        fig.update_geos(
            visible=True,
            resolution=50,
            showcountries=True,
            showocean=True,
            oceancolor="#0E1117",
            landcolor="#0E1117",
            lakecolor="#0E1117",
            bgcolor="#0E1117"
        )
        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            geo=dict(
                showframe=False,
                showcoastlines=False
            )
        )
        st.plotly_chart(fig)

    # Add space between the two columns
    st.empty()  # Empty space to avoid overlap

    # Display happiest countries with a progress bar for Happiness Score
    with col2:
        top_5_countries = df.nlargest(5, 'Happiness Score')[['Country', 'Happiness Score']]
        st.write(f"### Happiest Countries in {selected_year}")

        for _, row in top_5_countries.iterrows():
            progress = row['Happiness Score'] / 10  # Assuming the happiness score is out of 10
            st.progress(progress, text=f"{row['Country']} - {row['Happiness Score']}")

    # Secondary visualization based on GDP if available
    if 'GDP per capita' in df.columns:
        gdp_chart = px.scatter(
            df,
            x='GDP per capita',
            y='Happiness Score',
            size='Happiness Score',
            color='Region' if 'Region' in df.columns else None,
            hover_name='Country',
            title=f"GDP per capita vs Happiness Score ({selected_year})",
            color_continuous_scale=px.colors.sequential.Viridis
        )
        gdp_chart.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="white",
            xaxis_title="GDP per capita",
            yaxis_title="Happiness Score",
        )
        st.plotly_chart(gdp_chart)

    # Freedom comparison section
    if 'Freedom' in df.columns:
        col_free1, col_free2 = st.columns(2)  # Create two side-by-side blocks

        # Get the countries with the highest and lowest freedom scores
        most_free = df.loc[df['Freedom'].idxmax()]
        least_free = df.loc[df['Freedom'].idxmin()]

        # Calculate the difference
        freedom_diff = most_free['Freedom'] - least_free['Freedom']

        # Display the most free country in a block
        with col_free1:
            st.markdown(
                f"""
                <div style="background-color:#2ecc71; padding: 10px; border-radius: 5px;">
                    <h4 style="color:white;">Most Free Country</h4>
                    <p style="color:white;">{most_free['Country']} with a Freedom score of {most_free['Freedom']}</p>
                </div>
                """,
                unsafe_allow_html=True)

        # Display the least free country in a block
        with col_free2:
            st.markdown(
                f"""
                <div style="background-color:#e74c3c; padding: 10px; border-radius: 5px;">
                    <h4 style="color:white;">Least Free Country</h4>
                    <p style="color:white;">{least_free['Country']} with a Freedom score of {least_free['Freedom']}</p>
                </div>
                """,
                unsafe_allow_html=True)

    # Create the Happiness Scores Distribution Histogram
    st.write("### Distribution of Happiness Scores")
    fig_hist = px.histogram(df, x="Happiness Score", nbins=20, title="Happiness Score Distribution")
    fig_hist.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        xaxis_title="Happiness Score",
        yaxis_title="Frequency"
    )
    st.plotly_chart(fig_hist)

    # Create the Line Plot for Happiness Scores Over Time
    st.write(f"### Happiness Scores Over Time (for all countries) in {selected_year}")
    fig_line = px.line(df, x='Country', y='Happiness Score', title=f"Happiness Scores for {selected_year}")
    fig_line.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        xaxis_title="Country",
        yaxis_title="Happiness Score"
    )
    st.plotly_chart(fig_line)

    # Top 5 Countries with the Highest Happiness Scores (Bar Plot)
    st.write(f"### Top 5 Happiest Countries in {selected_year}")
    top_5_countries = df.nlargest(5, 'Happiness Score')[['Country', 'Happiness Score']]
    fig_bar = px.bar(top_5_countries, x='Country', y='Happiness Score', title=f"Top 5 Happiest Countries in {selected_year}")
    fig_bar.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        xaxis_title="Country",
        yaxis_title="Happiness Score"
    )
    st.plotly_chart(fig_bar)

    # Optional: Add data download button
    st.download_button(
        label="Download Data for the Selected Year",
        data=df.to_csv(index=False),
        file_name=f"world_happiness_{selected_year}.csv",
        mime="text/csv",
    )
