import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi

# Replace with your YouTube API Key
api_key = "AIzaSyAlHrrRRow3jgnGbBTx8qSQPFhq5I_YbWk"

def get_latest_ethereum_transcript():
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    channel_id = "UC4R8DWoMoI7CAwX8_LjQHig"

    MAX_RETRIES = 3
    retries = 0

    while retries < MAX_RETRIES:
        try:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                type="video",
                order="date",
                maxResults=1  
            )
            response = request.execute()


            if 'items' in response and len(response['items']) > 0: 
                video_id = response['items'][0]['id']['videoId']
                video_title = response['items'][0]['snippet']['title']
                video_description = response['items'][0]['snippet']['description']

                try:
                    transcript = YouTubeTranscriptApi.get_transcript(video_id)
                    full_transcript = ""
                    for text in transcript:
                        full_transcript += text['text'] + " "
                    print(full_transcript)

                except: 
                    print("Transcript not available.")

                return video_id, video_title, video_description 
            else:
                print("No videos found from the channel.")
                return None, None, None 

        except googleapiclient.errors.HttpError as error:
            if error.resp.reason == 'quotaExceeded':
                print("Daily YouTube Data API quota exceeded. Please try again later.")
                return None, None, None 
            elif retries < MAX_RETRIES: 
                retries += 1
                print(f"Error occurred. Retrying (attempt {retries})")
                print(error)  # Print the detailed error object

            else:
                raise error 
            

# Placeholder for your Farcaster/Neynar bot logic
def summarize_and_post_to_farcaster(video_id, video_title, full_transcript):
    # 1. Use OpenAI GPT-3 API to summarize the transcript
    # 2. Use Neynar to post the summary as a Farcaster thread
    print(f"Would summarize and post the transcript of '{video_title}' to Farcaster")

# Main Execution
def main():
    video_id, video_title, video_description = get_latest_ethereum_transcript()

    if video_id is not None:  
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = ""
            for text in transcript:
                full_transcript += text['text'] + " "
            
            summarize_and_post_to_farcaster(video_id, video_title, full_transcript)

        except: 
            print("Transcript not available for this video.")
    else:
        print("Unable to retrieve video (quota exceeded or no videos found)")

if __name__ == "__main__":
    main() 

# Call the function to print the results
video_id, video_title, video_description = get_latest_ethereum_transcript()
