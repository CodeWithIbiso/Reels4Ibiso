import os
import requests

PAGE_ID = os.getenv("REELS_PAGE_ID")
NEVER_ENDING_TOKEN = os.getenv("NEVER_ENDING_REELS_TOKEN")

# POSTS
def create_post_url(id):
    post_id = id.replace(f"{PAGE_ID}_", "")
    return f"https://www.facebook.com/750382501472199/posts/{post_id}"

def get_posts():
    response = requests.get(f'https://graph.facebook.com/v19.0/{PAGE_ID}/posts?access_token={NEVER_ENDING_TOKEN}')
    response = response.json()
        
    data = response.get("data") if response and response.get("data") else []
    posts = [ 
        {  
            "id": i + 1,
            "title": data.get("message", ""),
            "created_time": data.get("created_time", ""),
            "url": create_post_url(data.get("id")),
        } for i, data in enumerate(data) ] 

    return posts

# REELS
def create_reel_url(id):
    return f"https://www.facebook.com/reel/{id}/"

def get_video_thumbnail(video_id):
    response = requests.get(f'https://graph.facebook.com/v19.0/{video_id}/thumbnails?access_token={NEVER_ENDING_TOKEN}')
    response = response.json()
    return response.get("data",[])[0].get("uri")

def get_reels():
    try:
        return [
            {
                "id": 1,
                "title": "Check out this awesome Reel! #Reels #Automation",
                "created_time": "2025-08-02T15:49:03+0000",
                "url": "https://www.facebook.com/reel/2905333442987598/",
                "thumbnail": "https://scontent.fabb1-3.fna.fbcdn.net/v/t15.5256-10/522837159_1935202333920838_6410916083619147843_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=e3495b&_nc_eui2=AeG-d3SS0T8R_m9ofuEr3eKie-D0-rgpmXJ74PT6uCmZcgjWb3nc3z1B2spQ9osvZ71kd41mp6kkUgoGAHbwqHb8&_nc_ohc=aX36RAyjZikQ7kNvwHAoOPi&_nc_oc=AdlDtTskf4qDR_M-NlmIOxxYWLqMwSzkFkxOhHqp7hOnuBgFHq7K06hSR2fdFEkY0_U&_nc_zt=23&_nc_ht=scontent.fabb1-3.fna&edm=AF0wKlEEAAAA&_nc_gid=hzlvd5XNr4bBJWbzN1UXlg&oh=00_AfRloh8inF28RbU3Z12tIV6_dwTJVuDgPFgVXlFDTsKa5w&oe=68941A79"
            }
        ]
        response = requests.get(f'https://graph.facebook.com/v19.0/{PAGE_ID}/video_reels?access_token={NEVER_ENDING_TOKEN}')
        response = response.json()
            
        data = response.get("data") if response and response.get("data") else []

        reels = []

        for i, reel in enumerate(data):
            reel_id = reel.get("id")
            reel_url = create_reel_url(reel_id)
            thumbnail_url = get_video_thumbnail(reel_id)

            reel_dict = {  
                "id": i + 1,
                "thumbnail": thumbnail_url,
                "title": reel.get("description", ""),
                "created_time": reel.get("updated_time", ""),
                "url": reel_url,
            }
            
            reels.append(reel_dict)

        return reels
    except Exception as e:
        print("Error fetching reel ",e)
        return []



