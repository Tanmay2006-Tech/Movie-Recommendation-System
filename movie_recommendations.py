import os
import json
from openai import OpenAI

def get_movie_recommendations(user_input):
    """
    Get movie recommendations based on user input using OpenAI's GPT-3.5.
    
    Args:
        user_input (str): User's input about their mood, genre preference, or recently liked movie
        
    Returns:
        list: List of movie recommendation dictionaries
    """
    # Initialize OpenAI client
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    
    client = OpenAI(api_key=api_key)
    
    # Create the prompt for OpenAI
    system_prompt = """
    You are an expert film critic and recommendation system. Based on the user's input about their mood, 
    genre preferences, or recently enjoyed movies, recommend 3-5 movies they might enjoy.
    
    For each movie recommendation, include:
    - Title (string)
    - Year (string, format: "YYYY")
    - Genre (string)
    - Reasoning (string): A brief, personalized explanation of why they might enjoy this movie based on their input
    
    Format your response as a JSON array of recommendation objects, like this:
    [
        {
            "title": "Movie Title",
            "year": "YYYY",
            "genre": "Movie Genre",
            "reasoning": "Reason why they would enjoy this movie"
        },
        ...
    ]
    
    Ensure each recommendation is relevant to their input, diverse, and well-explained.
    """
    
    try:
        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and parse the response
        response_content = response.choices[0].message.content
        recommendations = json.loads(response_content)
        
        # Ensure we have the recommendations array
        if "recommendations" in recommendations:
            return recommendations["recommendations"]
        else:
            # If the model returned a different structure than expected
            return recommendations
            
    except Exception as e:
        raise Exception(f"Error getting movie recommendations: {str(e)}")
