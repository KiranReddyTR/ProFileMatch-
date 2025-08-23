import requests
import os
import streamlit as st

# YouTube Data API v3 key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "your-youtube-api-key")

def get_youtube_recommendations(skill, max_results=6):
    """Get YouTube video recommendations for a specific skill"""
    
    if not YOUTUBE_API_KEY or YOUTUBE_API_KEY == "your-youtube-api-key":
        # Return more comprehensive placeholder data if no API key is available
        return [
            {
                "title": f"Learn {skill} - Complete Tutorial",
                "url": f"https://youtube.com/search?q=learn+{skill.replace(' ', '+')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            },
            {
                "title": f"{skill} for Beginners - Full Course",
                "url": f"https://youtube.com/search?q={skill.replace(' ', '+')}+tutorial",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            },
            {
                "title": f"Advanced {skill} Techniques",
                "url": f"https://youtube.com/search?q=advanced+{skill.replace(' ', '+')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            },
            {
                "title": f"{skill} Crash Course - 2024",
                "url": f"https://youtube.com/search?q={skill.replace(' ', '+')}+crash+course",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            },
            {
                "title": f"Master {skill} in 30 Days",
                "url": f"https://youtube.com/search?q=master+{skill.replace(' ', '+')}",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            },
            {
                "title": f"{skill} Best Practices & Tips",
                "url": f"https://youtube.com/search?q={skill.replace(' ', '+')}+best+practices",
                "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
            }
        ]
    
    try:
        # Search for videos related to the skill
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "snippet",
            "q": f"learn {skill} tutorial programming",
            "type": "video",
            "maxResults": max_results,
            "key": YOUTUBE_API_KEY,
            "order": "relevance",
            "regionCode": "US"
        }
        
        response = requests.get(search_url, params=search_params)
        
        if response.status_code == 200:
            data = response.json()
            recommendations = []
            
            for item in data.get("items", []):
                video_info = {
                    "title": item["snippet"]["title"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
                }
                recommendations.append(video_info)
            
            return recommendations
        else:
            # Silently fail - don't show technical errors to users
            return []
            
    except Exception as e:
        # Silently handle errors - provide fallback or no recommendations
        return []

def get_skill_learning_videos(skills_list):
    """Get YouTube recommendations for a list of skills"""
    all_recommendations = {}
    
    for skill in skills_list:
        recommendations = get_youtube_recommendations(skill)
        if recommendations:
            all_recommendations[skill] = recommendations
    
    return all_recommendations
