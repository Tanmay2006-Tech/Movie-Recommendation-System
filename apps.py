import streamlit as st
import os
import random
from movie_recommendations import get_movie_recommendations

# Page configuration
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 24px;
        font-style: italic;
        color: #424242;
        text-align: center;
        margin-bottom: 30px;
    }
    .description {
        font-size: 16px;
        line-height: 1.5;
        text-align: center;
        margin-bottom: 30px;
    }
    .movie-card {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #FF4B4B;
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
        color: #1E1E1E;
        margin-bottom: 10px;
    }
    .movie-meta {
        font-size: 16px;
        color: #757575;
        margin-bottom: 15px;
    }
    .movie-reason {
        font-size: 16px;
        line-height: 1.5;
    }
    .recommendation-header {
        background-color: #F0F2F6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
        text-align: center;
        font-weight: bold;
        color: #1E1E1E;
        font-size: 28px;
    }
    .footer {
        text-align: center;
        color: #757575;
        padding: 20px;
        font-size: 14px;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #E03B3B;
    }
    .input-section {
        background-color: #F8F9FA;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .genre-button {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 20px;
        padding: 10px 15px;
        margin: 5px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .genre-button:hover {
        background-color: #F0F2F6;
        border-color: #CCCCCC;
    }
    .genre-button.selected {
        background-color: #FF4B4B;
        color: white;
        border-color: #FF4B4B;
    }
    .mood-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 5px;
        cursor: pointer;
        text-align: center;
        transition: all 0.3s ease;
    }
    .mood-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .mood-emoji {
        font-size: 24px;
        margin-bottom: 5px;
    }
    .how-it-works {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
        margin-bottom: 30px;
    }
    .how-it-works-header {
        font-size: 20px;
        font-weight: bold;
        color: #1E1E1E;
        margin-bottom: 15px;
        text-align: center;
    }
    .step-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .step-number {
        background-color: #FF4B4B;
        color: white;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Movie emojis for random selection
movie_emojis = ["🎬", "🍿", "🎭", "🎞️", "📽️", "🎦", "🎪", "🎟️"]

# Main header with animation effect
st.markdown(f'<div class="main-header">🎬 AI Movie Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Discover your next favorite film with AI-powered recommendations</div>', unsafe_allow_html=True)

# Introduction text
st.markdown("""
<div class="description">
Select a genre or mood, or tell us about a movie you recently enjoyed. 
Our AI will analyze your preferences and recommend films tailored just for you!
</div>
""", unsafe_allow_html=True)

# Input section with styling
st.markdown('<div class="input-section">', unsafe_allow_html=True)

# Two tabs for different input methods
tab1, tab2 = st.tabs(["Quick Selection", "Custom Description"])

# Tab 1: Genre and Mood Selection
with tab1:
    st.subheader("Choose a Genre")
    
    # Genre selection buttons in a grid layout
    genres = {
        "Action": "🔫", 
        "Comedy": "😂", 
        "Drama": "🎭", 
        "Horror": "😱",
        "Sci-Fi": "🚀", 
        "Romance": "💑", 
        "Thriller": "🔍", 
        "Fantasy": "🧙",
        "Animation": "🧸", 
        "Documentary": "🎥"
    }
    
    # Create a 5x2 grid for genres
    genre_cols = st.columns(5)
    selected_genre = st.session_state.get('selected_genre', None)
    
    # Initialize session state for tracking selections
    if 'selected_genre' not in st.session_state:
        st.session_state.selected_genre = None
    
    # Display genre buttons
    for i, (genre, emoji) in enumerate(genres.items()):
        with genre_cols[i % 5]:
            if st.button(f"{emoji} {genre}", key=f"genre_{genre}", 
                         use_container_width=True, 
                         type="primary" if st.session_state.selected_genre == genre else "secondary"):
                st.session_state.selected_genre = genre if st.session_state.selected_genre != genre else None
                st.session_state.selected_mood = None  # Clear mood when genre is selected
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Or Select a Mood")
    
    # Mood cards in a grid layout
    moods = {
        "Happy": "😊", 
        "Sad": "😢", 
        "Excited": "🤩", 
        "Relaxed": "😌",
        "Tense": "😰", 
        "Inspired": "✨", 
        "Nostalgic": "🕰️", 
        "Curious": "🧐"
    }
    
    # Create a 4x2 grid for moods
    mood_cols = st.columns(4)
    selected_mood = st.session_state.get('selected_mood', None)
    
    # Initialize session state for mood
    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None
    
    # Display mood cards
    for i, (mood, emoji) in enumerate(moods.items()):
        with mood_cols[i % 4]:
            mood_card_style = "background-color: #FF4B4B; color: white;" if st.session_state.selected_mood == mood else ""
            st.markdown(f"""
            <div class="mood-card" style="{mood_card_style}" onclick="this.classList.toggle('selected')">
                <div class="mood-emoji">{emoji}</div>
                <div>{mood}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{mood}", key=f"mood_{mood}", use_container_width=True,
                        type="primary" if st.session_state.selected_mood == mood else "secondary"):
                st.session_state.selected_mood = mood if st.session_state.selected_mood != mood else None
                st.session_state.selected_genre = None  # Clear genre when mood is selected

# Tab 2: Custom Text Input
with tab2:
    user_input = st.text_area(
        "Describe what you're looking for",
        height=150,
        placeholder="Examples:\n• I'm feeling down and need something uplifting\n• I love sci-fi movies with philosophical themes\n• I recently enjoyed 'The Grand Budapest Hotel' and want similar recommendations\n• Looking for a movie like Inception but more emotional"
    )

# Create a button container outside the tabs
st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    submit_button = st.button("Get Recommendations", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Construct the input query based on selections
query = ""
if submit_button:
    if st.session_state.get('selected_genre'):
        query = f"I'm looking for {st.session_state.selected_genre} movies"
    elif st.session_state.get('selected_mood'):
        query = f"I'm feeling {st.session_state.selected_mood.lower()}, suggest some movies that match this mood"
    elif user_input.strip():
        query = user_input
    
    if not query:
        st.error("Please select a genre, mood, or describe what you're looking for before submitting.")
    else:
        # Check for API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        else:
            # Show loading spinner with custom message
            loading_messages = [
                "Searching the cinematic universe...", 
                "Consulting with AI film critics...",
                "Analyzing your preferences...",
                "Finding the perfect movie matches...",
                "Curating your personalized watchlist..."
            ]
            with st.spinner(random.choice(loading_messages)):
                try:
                    recommendations = get_movie_recommendations(query)
                    
                    # Display recommendations with styled header
                    st.markdown(f'<div class="recommendation-header">{random.choice(movie_emojis)} Your Personalized Movie Recommendations</div>', unsafe_allow_html=True)
                    
                    # Create three columns for recommendations
                    if len(recommendations) >= 3:
                        cols = st.columns(3)
                        for i, recommendation in enumerate(recommendations[:3]):
                            with cols[i]:
                                st.markdown(f"""
                                <div class="movie-card">
                                    <div class="movie-title">{recommendation['title']}</div>
                                    <div class="movie-meta">{recommendation.get('year', '')} • {recommendation.get('genre', '')}</div>
                                    <div class="movie-reason"><strong>Why you might like it:</strong> {recommendation['reasoning']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # If more than 3 recommendations, display the rest in a row below
                        if len(recommendations) > 3:
                            remaining_cols = st.columns(min(3, len(recommendations) - 3))
                            for i, recommendation in enumerate(recommendations[3:6]):
                                with remaining_cols[i]:
                                    st.markdown(f"""
                                    <div class="movie-card">
                                        <div class="movie-title">{recommendation['title']}</div>
                                        <div class="movie-meta">{recommendation.get('year', '')} • {recommendation.get('genre', '')}</div>
                                        <div class="movie-reason"><strong>Why you might like it:</strong> {recommendation['reasoning']}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                    else:
                        # If fewer than 3 recommendations, use a single column layout
                        for recommendation in recommendations:
                            st.markdown(f"""
                            <div class="movie-card">
                                <div class="movie-title">{recommendation['title']}</div>
                                <div class="movie-meta">{recommendation.get('year', '')} • {recommendation.get('genre', '')}</div>
                                <div class="movie-reason"><strong>Why you might like it:</strong> {recommendation['reasoning']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Add a suggestion to try again
                    st.markdown("""
                    <div style="text-align: center; margin-top: 30px; margin-bottom: 30px;">
                        <em>Not quite what you're looking for? Try being more specific or explore a different genre!</em>
                    </div>
                    """, unsafe_allow_html=True)
                                
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

# How it works section
st.markdown('<div class="how-it-works">', unsafe_allow_html=True)
st.markdown('<div class="how-it-works-header">How It Works</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="step-card">
        <span class="step-number">1</span> <strong>Input Your Preferences</strong>
        <p>Select a genre, mood, or describe what kind of movie you're looking for. You can mention specific films you enjoyed, themes that interest you, or how you're feeling today.</p>
    </div>
    <div class="step-card">
        <span class="step-number">2</span> <strong>AI Analysis</strong>
        <p>Our system uses OpenAI's GPT-3.5 language model to analyze your preferences and understand your movie taste. The AI has been trained on a vast database of films and their characteristics.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step-card">
        <span class="step-number">3</span> <strong>Personalized Curation</strong>
        <p>Based on your input, the AI generates a custom list of movie recommendations that match your preferences, complete with reasons why each film was selected for you.</p>
    </div>
    <div class="step-card">
        <span class="step-number">4</span> <strong>Discover New Favorites</strong>
        <p>Explore your personalized recommendations and discover new films you might love. Each suggestion includes information about the movie and why it might resonate with you.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add fancy footer with additional info
st.markdown("""
<div class="footer">
    <div style="margin-bottom: 10px;">
        Powered by OpenAI's GPT-3.5 • Created with Streamlit • © 2025 AI Movie Recommender
    </div>
</div>
""", unsafe_allow_html=True)
