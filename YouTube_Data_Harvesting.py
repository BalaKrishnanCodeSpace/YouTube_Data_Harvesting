# Author:             Balakrishnan R

# Main Objective:     Scrape Channel Data from YouTube using API V3. 
#                     Store the data in MongoDB and migrate the data from MonogoDB to MySQL. 
#                     Analyse the channel data stored in MySQL using SQL Queries

# Uploaded On:        12/02/2024


from googleapiclient.discovery import build
from pymongo import MongoClient
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import re
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px

#___________________________Create Streamlit Page___________________________#

st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing",
                   page_icon= ':bar_chart:',
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )

st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #ADD8E6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#___________________________Create API Connection___________________________#
def API_Connection(API_Key):
    """
    Builds the YouTube API client using the provided API key.

    Args:
    API_Key: The API key to use for authentication.

    Returns:
    YouTube: The built YouTube API client.
    
    """
    Youtube = build('youtube','v3',developerKey = API_Key)
    API_Key = API_Key
    return Youtube

       
#___________________________Data Scraping___________________________#
def Channel_Detail_Scraping(Youtube,Channel_Id):
    """
    Retrieve Channel information about the given YouTube channel using the YouTube Data API v3.

    Returns:
    - Channel details of the given channel
    
    """
    Channel_Response = Youtube.channels().list(
                part = 'id,snippet,contentDetails,statistics',
                id = Channel_Id).execute()
        
    Channel_Details = dict(
        Channel_Name = Channel_Response['items'][0]['snippet']['title'],
        Channel_Id = Channel_Response['items'][0]['id'],
        Subscription_Count = Channel_Response['items'][0]['statistics']['subscriberCount'],
        Channel_Views = Channel_Response['items'][0]['statistics']['viewCount'],
        Channel_Description = Channel_Response['items'][0]['snippet']['description'],
        Playlist_Id = Channel_Response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],
        Thumbnail_URL = Channel_Response['items'][0]['snippet']['thumbnails']['default']['url']
    )
    return Channel_Details



def Video_Id_Scraping(Youtube,Channel_Id):
    """
    Retrieve Video Ids of the given YouTube channel.

    Returns:
    - Video Ids of the given channel
    
    """
    Video_Ids = []
    Playlist_Id = Channel_Detail_Scraping(Youtube,Channel_Id)['Playlist_Id']
    Next_Page_Token = None
    
    while True:
        Play_list_Response = Youtube.playlistItems().list(playlistId=Playlist_Id,
                                                       part = 'snippet',
                                                       maxResults = 50,
                                                       pageToken = Next_Page_Token).execute()
        for item in Play_list_Response['items']:
            Video_Ids.append(item['snippet']['resourceId']['videoId'])
        Next_Page_Token = Play_list_Response.get('nextPageToken')
        
        if Next_Page_Token is None:
            break
    return Video_Ids


def Comment_Details_Scraping(Video_Ids):
    """
    Retrieve Comments of the associated Videos in the given Youtube Channel.

    Returns:
    - Comment details of the associated videos in given channel
    
    """
    Comment_Details = []
    count = 1
    
    try:
        Next_Page_Token = None 
        
        while True:
            Comment_Response = Youtube.commentThreads().list(part = 'snippet',
                                               videoId = Video_Ids,
                                               maxResults=100,
                                               pageToken = Next_Page_Token).execute()
            
            for cmt in Comment_Response['items']:
                comment = cmt['snippet']['topLevelComment']['snippet']
                Comment_Detail = {"Comment_Id_" + str(count):{
                    "Comment_Id": cmt['snippet']['topLevelComment']['id'],
                    "Comment_Text": comment['textDisplay'],
                    "Comment_Author": comment['authorDisplayName'],
                    "Comment_PublishedAt": comment['publishedAt']
                }
                                  }
                Comment_Details.append(Comment_Detail)
                count = count + 1
            Next_Page_Token = Comment_Response.get('nextPageToken')

            if not Next_Page_Token:
                break
    
    except Exception as e:
    
        if 'commentsDisabled' in str(e):
            Comment_Details.append({"Comments":{}})
        else:
            st.error(f'An error occured while fetching the comments: {e}')
    
    return Comment_Details



def Video_Details_Scraping(Youtube,Channel_Id,Video_Ids):
    """
    Retrieve Videos of the given YouTube channel.

    Returns:
    - Video details of the given channel
    
    """
    Video_Details = []
    count = 1
    
    for item in range(0, len(Video_Ids), 50):
        Video_Response = Youtube.videos().list(
            id=','.join(Video_Ids[item:item + 50]),
            part='snippet,contentDetails,statistics'
        ).execute()
        
        for video in Video_Response['items']:
            playlist_id = Channel_Detail_Scraping(Youtube,Channel_Id)['Playlist_Id']  # Get the playlist ID from Channel Detail Scraping
            
            Video_Detail = {
                "Video_Id_" + str(count): {
                    "Channel_ID": video['snippet']['channelId'],
                    "Video_Id": video['id'],
                    "Video_Name": video['snippet']['title'],
                    "Video_Description": video['snippet']['description'],
                    "Tags": video['snippet'].get('tags'),
                    "PublishedAt": video['snippet']['publishedAt'],
                    "View_Count": video['statistics']['viewCount'],
                    "Like_Count": video['statistics'].get('likeCount'),
                    "Dislike_Count": video['statistics'].get('dislikeCount'),
                    "Favorite_Count": video['statistics'].get('favoriteCount'),
                    "Comment_Count": video['statistics'].get('commentCount'),
                    "Duration": video['contentDetails']['duration'],
                    "Thumbnail": video['snippet']['thumbnails']['default']['url'],
                    "Caption_Status": video['contentDetails']['caption'],
                    "Playlist_ID": playlist_id,  # Include Playlist ID
                    "Comments": Comment_Details_Scraping(video['id'])
                }
            }
            count += 1
            Video_Details.append(Video_Detail)
    
    return Video_Details


def Playlist_Detail_Scraping(Youtube,Channel_Id):
    """
    Retrieve Playlists of the given YouTube channel.
    
    Returns:
    - Playlist detail of the given channel
    """
    Next_Page_Token = None
    PlaylistDetail = []
    
    try:
        while True:
            Playlist_Response = Youtube.playlists().list(part = 'snippet,contentDetails,status',
                                               channelId = Channel_Id,
                                               maxResults=50,
                                               pageToken = Next_Page_Token).execute()
            for item in Playlist_Response['items']:
                Playlists = dict(
                    Playlist_Id = item['id'],
                    Channel_Id = Channel_Id,
                    Playlist_Name = item['snippet']['title']
                )
                PlaylistDetail.append(Playlists)
            Next_Page_Token = Playlist_Response.get('nextPageToken')
        
            if not Next_Page_Token:
                break
    except Exception as e:
        print(f'An error occured while fetching the playlists: {e}')
    return PlaylistDetail



#___________________________Create MongoDB Connection___________________________#

def Connect_To_MongoDB():
    """
    Establishes a connection to the MongoDB server and retrieves the collection for storing channel details.

    Returns:
    - Collection (pymongo.collection.Collection): The MongoDB collection for storing channel details.
    """
    
    client = MongoClient("mongodb://localhost:27017/")
    Database = client['YouTubeScrapingMongoDB']
    Collection = Database['ChannelDetailsCollection']
    return Collection


def Connect_To_TempdbMongoDB():
    """
    Establishes a connection to the MongoDB server and retrieves the temporary collection for temporary storage.

    Returns:
    - Collection_temp (pymongo.collection.Collection): The temporary MongoDB collection for temporary storage.
    """
    
    client = MongoClient("mongodb://localhost:27017/")
    temp_db = client['TemporaryDatabase']
    Collection_temp = temp_db['TemporaryCollection']
    return Collection_temp


#___________________________Insert/Update into MongoDB___________________________#
def store_data_in_temp_db(ChannelDetails, VideoDetails):
    """
    Stores video details in temporary database before uploading them to the main database.
    
    """
    try:
        Collection_temp = Connect_To_TempdbMongoDB()
        existing_channel = Collection_temp.find_one({"ChannelDetails.Channel_Id": ChannelDetails["Channel_Id"]})

        if existing_channel:
            query = {"ChannelDetails.Channel_Id": ChannelDetails["Channel_Id"]}
            Collection_temp.replace_one(query, {"ChannelDetails": ChannelDetails, "VideoDetails": VideoDetails})
        else:
            new_document = {"ChannelDetails": ChannelDetails, "VideoDetails": VideoDetails}
            Collection_temp.insert_one(new_document)
    
    except Exception as e:
        print(f"An error occurred: {e}")



def insert_playlist_details_to_mongodb(playlist_details):
    client = MongoClient("mongodb://localhost:27017/")
    temp_db = client['TemporaryDatabase']
    Collection_playlist_insert = temp_db['PlaylistCollection']
    
    try:
        playlist_insert_mongodb = {"PlaylistDetails": playlist_details}
        Collection_playlist_insert.insert_one(playlist_insert_mongodb)
        print("Playlist details inserted into MongoDB successfully.")
    except Exception as e:
        print(f'An error occurred while inserting playlist details into MongoDB: {e}')

        
        
def Move_from_tempdb_to_mongodb():
    
    try:
        temp_collection = Connect_To_TempdbMongoDB()
        final_collection = Connect_To_MongoDB()

        # Retrieve documents from the temporary collection
        documents_to_move = temp_collection.find()
        # Move documents to the final destination collection
        for document in documents_to_move:
            channel_id = document['ChannelDetails']['Channel_Id']
            existing_channel = final_collection.find_one({"ChannelDetails.Channel_Id": channel_id})

            if existing_channel:
                query = {"ChannelDetails.Channel_Id": channel_id}
                del document['_id']
                final_collection.update_one(query, {"$set": document})
                st.write(f"Updated document for channel ID: {channel_id}")
            else:
                final_collection.insert_one(document)
                st.write(f"Inserted new document for channel ID: {channel_id}")

        st.write('Data inserted or updated successfully')
    
    except Exception as e:
        print(f"An error occurred while moving data to the final destination database: {e}")
        

#___________________________Retrieve ChannelIDs stored in Temporary DB in MongoDB___________________________#
def Channel_Namelist_In_TempDB_In_MongoDB():
    channels = []
    client = MongoClient("mongodb://localhost:27017/")
    temp_db = client['TemporaryDatabase']
    temp_collection = temp_db['TemporaryCollection']

    documents_to_move = temp_collection.find()
   
    for document in documents_to_move:
        channel_id = document['ChannelDetails']['Channel_Id']
        channels.append(channel_id)
    return channels




#___________________________Clear Temporary DB in MongoDB___________________________#
def Clear_TempDB_In_MongoDB():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        client.drop_database('TemporaryDatabase')
        print("Temporary database dropped successfully")
    except Exception as e:
        print(f"An error occurred while dropping the temporary database: {e}")


#___________________________Store the Scraped data into Temporary DB in MongoDB___________________________#
def Main_Scraping(Youtube,_Unique,Channels_Id_List):

    st.write(f'You have entered {len(Channels_Id_List)} channel Id(s)')
    for Channel_Id in _Unique:
        ChannelDetails = Channel_Detail_Scraping(Youtube,Channel_Id)
        VideoIds = Video_Id_Scraping(Youtube,Channel_Id)
        VideoDetails = Video_Details_Scraping(Youtube,Channel_Id,VideoIds)
        playlist_details = Playlist_Detail_Scraping(Youtube,Channel_Id)
        store_data_in_temp_db(ChannelDetails, VideoDetails)
        insert_playlist_details_to_mongodb(playlist_details)


#___________________________Display the Scraped Channel Details in Streamlit page___________________________
def Channel_Scraping(_UniqueChannelIds):
    count = 1
    collection = Connect_To_TempdbMongoDB()
    st.write()
    st.divider()
    st.success(f'Successfully scraped {len(_UniqueChannelIds)} channel Id(s)')
    st.write()
    
    for unqch in _UniqueChannelIds:
        document_cursor = collection.find({'ChannelDetails.Channel_Id': unqch})
        document = next(document_cursor, None)

        if document:
            
            channel_details = document['ChannelDetails']
            video_details = document.get('VideoDetails',[])
            channel_id = channel_details['Channel_Id']
            channel_name = channel_details['Channel_Name']
            channel_views = channel_details['Channel_Views']
            subscription_count = channel_details['Subscription_Count']
            thumbnail_url = channel_details['Thumbnail_URL']
            
            st.write(f'<h3> <span style="color:#01aac8"><i><b> Channel : {count} </b></i></span></h3>', unsafe_allow_html=True)
            st.write(f'<b>Channel Name :</b> <span style="color:#c86401"><i><b>{channel_name}</b></i></span>', unsafe_allow_html=True)
            st.write(f'<b>Channel Id :</b> <span style="color:#c86401"><i><b>{channel_id}</b></i></span>', unsafe_allow_html=True)
            st.write(f'<b>Subscription Count :</b> <span style="color:#c86401"><i><b>{subscription_count}</b></i></span>', unsafe_allow_html=True)
            st.write(f'<b>Channel Views :</b> <span style="color:#c86401"><i><b>{channel_views}</b></i></span>', unsafe_allow_html=True)
            st.write(f'<b>Video Count :</b> <span style="color:#c86401"><i><b>{len(video_details)}</b></i></span>', unsafe_allow_html=True)
            st.image(thumbnail_url, width=200)
            st.divider()
            count +=1

#___________________________Connection to MySQL___________________________#
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='youtubescrapingsql'
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            st.error("Error: Access denied.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            st.error("Error: Database does not exist.")
        else:
            st.error(f"Error: {err}")
    
    
#___________________________Insert/Update into MySQL from MongoDB___________________________#
def insert_or_update_mysql(collection,Channel_Id):
    """
    Insert/Update the documents from mongodb to mysql as table.
    If data is already present in MySQL then update it otherwise insert data.
    
    """
    mysql_connection = connect_to_mysql()
    cursor = mysql_connection.cursor()
    document_cursor = collection.find({'ChannelDetails.Channel_Id': Channel_Id})
    document = next(document_cursor, None)
    count = 1
    CmtCount = 1

    if document:
        
        channel_details = document['ChannelDetails']
        video_details = document.get('VideoDetails',[])
        channel_id = channel_details['Channel_Id']
        channel_name = channel_details['Channel_Name']
        channel_type = 'Channel Type'
        channel_views = channel_details['Channel_Views']
        channel_description = channel_details['Channel_Description']
        channel_status = 'Active'
        st.write(f'Inserting/Updating for the "{channel_name}" channel')
        cursor.execute("""INSERT INTO Channel (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE
                            channel_name = VALUES(channel_name),
                            channel_views = VALUES(channel_views),
                            channel_description = VALUES(channel_description)
                        """,
                       (channel_id, channel_name, channel_type, channel_views, channel_description, channel_status))
        

    
        for video_data in video_details:
                Video_Id_ = 'Video_Id_' + str(count)
                count += 1
                CmtCount = 1
                
                video_id = video_data.get(Video_Id_,{}).get('Video_Id','')
                playlist_id = video_data.get(Video_Id_,{}).get('Playlist_ID','')
                video_name = video_data.get(Video_Id_,{}).get('Video_Name','')
                video_description = video_data.get(Video_Id_,{}).get('Video_Description','')
                try:
                    published_date = datetime.strptime(video_data.get(Video_Id_,{}).get('PublishedAt',''), "%Y-%m-%dT%H:%M:%SZ")
                except:
                    published_date = None
                view_count = int(video_data.get(Video_Id_,{}).get('View_Count',0))
                like_count = int(video_data.get(Video_Id_,{}).get('Like_Count',0))
                dislike_count = 0 if video_data.get(Video_Id_,{}).get('Dislike_Count','0') is None else int(video_data.get(Video_Id_, {}).get('Dislike_Count'))
                favorite_count = int(video_data.get(Video_Id_,{}).get('Favorite_Count',0))
                comment_count = int(video_data.get(Video_Id_,{}).get('Comment_Count',0))
                duration = sum(int(x[:-1]) * {"H": 3600, "M": 60, "S": 1}[x[-1]] for x in re.findall(r'\d+H|\d+M|\d+S', video_data.get(Video_Id_,{}).get('Duration','')))
                thumbnail = video_data.get(Video_Id_,{}).get('Thumbnail','')
                caption_status = video_data.get(Video_Id_,{}).get('Caption_Status','')
                Comments = video_data.get(Video_Id_,{}).get('Comments',[])

                try:
                    cursor.execute("""INSERT INTO video (video_id, playlist_id, video_name, video_description, 
                                                        published_date, view_count, like_count, dislike_count, 
                                                        favourite_count, comment_count, duration, thumbnail, caption_status)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        ON DUPLICATE KEY UPDATE
                                        video_name = VALUES(video_name),
                                        video_description = VALUES(video_description),
                                        published_date = VALUES(published_date),
                                        view_count = VALUES(view_count),
                                        like_count = VALUES(like_count),
                                        dislike_count = VALUES(dislike_count),
                                        favourite_count = VALUES(favourite_count),
                                        comment_count = VALUES(comment_count),
                                        duration = VALUES(duration),
                                        thumbnail = VALUES(thumbnail),
                                        caption_status = VALUES(caption_status)
                                    """,
                                    (video_id, channel_id, video_name, video_description, published_date,
                                     view_count, like_count, dislike_count, favorite_count, comment_count,
                                     duration, thumbnail, caption_status))
                except Exception as e:
                    st.error(f"An error occurred while inserting/updating video: {e}")

                    

                for Comment in Comments:
                    Comment_Id_ = 'Comment_Id_' + str(CmtCount)
                    CmtCount += 1
                    
                    comment_id = Comment.get(Comment_Id_,{}).get('Comment_Id','')
                    video_id = video_data.get(Video_Id_,{}).get('Video_Id','')
                    comment_text = Comment.get(Comment_Id_,{}).get('Comment_Text','')
                    comment_author = Comment.get(Comment_Id_,{}).get('Comment_Author','')
                    try:
                        comment_published_date = datetime.strptime(Comment.get(Comment_Id_,{}).get('Comment_PublishedAt',''), "%Y-%m-%dT%H:%M:%SZ")
                    except:
                        comment_published_date = None
                    try:
                        cursor.execute("""INSERT INTO comment (comment_id, video_id, comment_text, comment_author, 
                                                            comment_published_date)
                                            VALUES (%s, %s, %s, %s, %s)
                                            ON DUPLICATE KEY UPDATE
                                            comment_text = VALUES(comment_text),
                                            comment_author = VALUES(comment_author),
                                            comment_published_date = VALUES(comment_published_date)
                                        """,
                                        (comment_id, video_id, comment_text, comment_author, comment_published_date))
                    except Exception as e:
                        st.error(f"An error occurred while inserting/updating Comments: {e}")

        client = MongoClient("mongodb://localhost:27017/")
        temp_db = client['TemporaryDatabase']
        Collection_playlist = temp_db['PlaylistCollection']
        document_cursor = Collection_playlist.find({},{'_id':0})

        for document in document_cursor:
            playlist_details = document.get('PlaylistDetails',[])
            for playlist in playlist_details:
                playlist_id = playlist.get('Playlist_Id', '')
                channel_id = playlist.get('Channel_Id', '')
                playlist_name = playlist.get('Playlist_Name', '')

                cursor.execute("""INSERT INTO playlist (playlist_id, channel_id, playlist_name)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    playlist_name = VALUES(playlist_name)
                    """,
                    (playlist_id, channel_id, playlist_name))
        mysql_connection.commit()
        st.success('Successfully inserted or updated into mysql')
        cursor.close()
        mysql_connection.close()
        

#___________________________SQL Queries to display the answer to question___________________________#
def Question_1():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    SELECT C.channel_name AS 'Channel Name', V.video_name AS 'Video Name' 
    FROM Channel C 
    LEFT JOIN video V ON C.channel_id = V.playlist_id 
    ORDER BY C.channel_name;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name'])
    cursor.close()
    connection.close() 
    return df


def Question_2():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', count(V.video_name) as 'Video Count'
    from Channel C left join video V on C.channel_id = V.playlist_id group by 
    C.channel_name order by count(V.video_name) desc limit 1;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Count'])
    cursor.close()
    connection.close() 
    return df


def Question_3(Input_Top):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = f"""
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name',
    V.view_count As 'Video Count' from video V left join Channel C on
    V.playlist_id = C.channel_id order by view_count desc limit {Input_Top};
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'View Count'])
    cursor.close()
    connection.close() 
    return df


def Question_4():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name',
    V.comment_count As 'Comment Count' from video V left join Channel C
    on V.playlist_id = C.channel_id order by comment_count desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Comment Count'])
    cursor.close()
    connection.close() 
    return df


def Question_5():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name', V.like_count As 'Like Count'
    from video V left join Channel C on V.playlist_id = C.channel_id order by like_count desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Like Count'])
    cursor.close()
    connection.close() 
    return df


def Question_6():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name', V.like_count As 'Like Count',
    V.dislike_count As 'Dislike Count' from video V left join Channel C
    on V.playlist_id = C.channel_id order by like_count desc, dislike_count desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Like Count', 'Dislike Count'])
    cursor.close()
    connection.close() 
    return df
    

def Question_7():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name', V.view_count As 'View Count'
    from video V inner join Channel C on V.playlist_id = C.channel_id order by view_count desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'View Count'])
    cursor.close()
    connection.close() 
    return df


def Question_8(Input_Year):
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = f"""
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name',
    Date(V.published_date) As 'Published Date', Time_Format(V.published_date,'%H:%i:%s') As 'Published Time'
    from video V left join Channel C on V.playlist_id = C.channel_id where year(published_date) = {Input_Year};
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Published Date', 'Published Time'])
    cursor.close()
    connection.close() 
    return df


def Question_9():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name',
    cast(avg(V.duration) as unsigned) as 'Average Duration' from Channel C
    left join video V on C.channel_id = V.playlist_id group by C.channel_name,
    V.video_name order by avg(V.duration) desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Average Duration'])
    cursor.close()
    connection.close() 
    return df


def Question_10():
    connection = connect_to_mysql()
    cursor = connection.cursor()
    query = """
    select C.channel_name As 'Channel Name', V.video_name As 'Video Name',
    V.comment_count As 'Comment Count' from video V left join Channel C
    on V.playlist_id = C.channel_id order by comment_count desc;
    """
    cursor.execute(query)
    records = cursor.fetchall()
    df = pd.DataFrame(records, columns=['Channel Name', 'Video Name', 'Comment Count'])
    cursor.close()
    connection.close() 
    return df


#___________________________Sidebar Configuration___________________________#
def display_sidebar():
    with st.sidebar:
        image_url = 'https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/115303331/original/be04ab13d541f93b673a8b75a4cbc95da1795f1e/integrate-youtube-data-api.png'
        st.image(image_url, use_column_width=True)

        selected = option_menu(menu_title='', options=['Home','Data Scraping', 'Data Migration',
                                                 'SQL Queries'],
                         icons=['house-door-fill','youtube', 'database-add',  'pencil-square'],
                         default_index=0,
                         orientation = "vertical",
                         styles={"nav-link": {"font-size": "14px", "text-align": "centre", "margin": "10px", 
                                                "--hover-color": "#01aac8","font-weight": "normal"},
                                   "icon": {"font-size": "14px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#015ec8"}})
    return selected


# Call functions
if __name__ == "__main__":
    #display_image()
    pass


def init_session():
    return {'button_clicked':False}


selected = display_sidebar()

if selected == "Home":
    
    st.toast('Welcome to our YouTube Data Scraping Webpage !!!', icon='😍')
    st.title("Home Page")
    #st.write('Welcome to our YouTube Data Scraping Webpage !!!')
    
    marquee_html = """
    <div style="width: 100%; white-space: nowrap; overflow: hidden;">
    <marquee behavior="scroll" direction="left" scrollamount="15">
    <h4 style = "color:blue;">Welcome to our YouTube Data Scraping Webpage !!!</h4>
    </marquee>
    </div>
    """
    
    st.markdown(marquee_html, unsafe_allow_html=True)

    st.markdown("<span style='font-size:18px;'><u><b>Domain</b></u>:</span>", unsafe_allow_html=True)
    st.write("Social Media")
    st.write("")
    st.markdown("<span style='font-size:18px;'><u><b>Technologies Used</b></u>:</span>", unsafe_allow_html=True)
    st.write("Python, MongoDB, MySQL, and Streamlit")
    st.write("")
    st.markdown("<span style='font-size:18px;'><u><b>Overview</b></u>:</span>", unsafe_allow_html=True)
    st.write("Retrieving the Youtube channels data using YouTube API, storing it in a MongoDB as data lake, transfer data to MySQL database, then querying the data on Streamlit app")
    st.write("")
    st.markdown("<span style='font-size:18px;'><u><b>Author</b></u>:</span>", unsafe_allow_html=True)
    st.write("Balakrishnan R")


elif selected == 'Data Scraping':
    
    st.write('<h1><span style="color:black">You</span><span style="color:white;background-color:red">Tube</span> Data Scraping </h1>', unsafe_allow_html=True)
    st.write("""<hr style="height:3px;border:none;color:#333;background-color:#456;margin:0;padding:0;"/>""",unsafe_allow_html = True)
    st.write("")
    st.write("To retrieve data from YouTube, please enter your API Key and the Channel ID(s) you want to scrape.")    
    st.write("")

    try:
        global Channel_Ids
        API_Key = st.text_input("Enter Your API Key:", type='password', help="Your YouTube Data API v3 key")
        Channel_Ids = st.text_input("Enter the Channel ID(s): ", help="Enter one or more YouTube Channel IDs separated by commas")
        st.write('<span style="color:red; font-size: 13px;">Note: You can enter multiple Channel IDs separated by commas.</span>', unsafe_allow_html=True)

        if st.button("Scrape Data"):
            if API_Key or Channel_Ids:    
                Channels_Id_List = [channel_id.strip() for channel_id in Channel_Ids.split(',')]
                Youtube = API_Connection(API_Key)
                _Unique = []
                _Duplicate = []
                
                for ch_list in Channels_Id_List:
                    if ch_list not in _Unique:
                        _Unique.append(ch_list)
                    else:
                        _Duplicate.append(ch_list)
                if len(_Duplicate)>=1:
                    st.warning(f'Out of {len(Channels_Id_List)} Channel Id(s) you have entered {len(_Duplicate)} duplicate Channel Id(s): ' + ", ".join(_Duplicate))

                with st.spinner('Please wait while channels are being scraped...'):
                    Clear_TempDB_In_MongoDB()
                    Main_Scraping(Youtube,_Unique,Channels_Id_List)
                    Channel_Scraping(_Unique)
            else:
                st.warning("Please provide the **API Key** & **Channel ID/s**.")

    except Exception as e:
        st.error('Enter correct API Key & channel Id(s)')


elif selected == 'Data Migration':
    st.title('Data Migration')
    session_state = st.session_state
    if 'button_clicked' not in session_state:
        session_state.update(init_session())
    
    st.write("""<span style="color: #DAA520;">Click here to insert/update the scraped data into MongoDB</span>""",unsafe_allow_html = True)

    if st.button("Upload to MongoDB"):
        session_state['button_clicked'] = True
        with st.spinner('Data Uploading to MongoDB started...'):
            Move_from_tempdb_to_mongodb()

    st.write("")
    st.write("")
    st.write("""<span style="color: #DAA520;">Click here to insert/update the document from MongoDB to MySQL</span>""",unsafe_allow_html = True)
    if st.button("Upload to mysql"):
        if not session_state['button_clicked']:
            st.warning('First upload the data into mongodb then try uploading into mysql')
        else:
            with st.spinner('Data Migrating to mysql started...'):
                Channel_Ids_In_TempDB = Channel_Namelist_In_TempDB_In_MongoDB()
                collection = Connect_To_MongoDB()
                for channels in Channel_Ids_In_TempDB:
                    insert_or_update_mysql(collection,channels)
                Clear_TempDB_In_MongoDB()


elif selected == 'SQL Queries':
    
    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Questions',
    ['--Select your questions--',
    '1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in below year?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])

    if questions == '--Select your questions--':
        pass
    
    elif questions == '1. What are the names of all the videos and their corresponding channels?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question1 = Question_1()
            df_Question1.index += 1  # Starting index from 1
            df_Question1.index.name = 'S No.'
            st.dataframe(df_Question1)
        
    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question2 = Question_2()
            df_Question2.index += 1
            df_Question2.index.name = 'S No.'
            st.write('Below channel have most number of videos among other channels')
            st.dataframe(df_Question2)

    elif questions == '3. What are the top most viewed videos and their respective channels?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            try:
                Input_Top = st.text_input("Enter the top value: ", help="Enter in numbers")
                if Input_Top:
                    df_Question3 = Question_3(Input_Top)
                    df_Question3.index += 1
                    df_Question3.index.name = 'S No.'
                    st.write(f'Below are the top {Input_Top} most viewed videos and their respective channel names')
                    st.dataframe(df_Question3)
                    
                    chart = px.pie(df_Question3, values='View Count', names='Video Name',
                             title=f'Top {Input_Top} Most Viewed Videos')
                    #chart = px.bar(df_Question3, x = 'Video Name', y = 'View Count', color = 'Channel Name', title = f'Top {Input_Top} Most Viewed Videos by Channel')
                    st.plotly_chart(chart)
            except:
                st.warning('Enter number to limit data')
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question4 = Question_4()
            df_Question4.index += 1
            df_Question4.index.name = 'S No.'
            st.dataframe(df_Question4)
            chart = px.bar(df_Question4, x='Comment Count', y='Video Name', orientation='h',
                     title='Number of Comments on Each Video')
        
        # Display the Plotly figure using Streamlit
            st.plotly_chart(chart)
        
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question5 = Question_5()
            df_Question5.index += 1
            df_Question5.index.name = 'S No.'
            st.dataframe(df_Question5)
            
            chart = px.bar(df_Question5, x='Like Count', y='Video Name', color='Channel Name',
                     title='Videos with the Highest Number of Likes by Channel',
                     orientation='h')
            st.plotly_chart(chart)
        
    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question6 = Question_6()
            df_Question6.index += 1
            df_Question6.index.name = 'S No.'
            st.dataframe(df_Question6)
            st.info("Dislike count inaccessible due to security reasons; therefore dislike value set to 0.")
            chart = px.bar(df_Question6, x='Like Count', y='Video Name',
                     title='Total Number of Likes for Each Video')
            st.plotly_chart(chart)
        
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question7 = Question_7()
            df_Question7.index += 1
            df_Question7.index.name = 'S No.'
            st.dataframe(df_Question7)
            chart = px.bar(df_Question7, x='View Count', y='Channel Name',
                     title='Total Number of Views for Each Channel',
                     orientation='h')
            st.plotly_chart(chart)
        
    elif questions == '8. What are the names of all the channels that have published videos in below year?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            try:
                Input_Year = st.text_input("Enter the year: ", help="Enter the year in 4 digits")
                if Input_Year:
                    df_Question8 = Question_8(Input_Year)
                    df_Question8.index += 1
                    df_Question8.index.name = 'S No.'
                    Video_counts = df_Question8['Channel Name'].value_counts().reset_index()
                    Video_counts.columns = ['Channel Name', 'Video Count']
                    st.dataframe(df_Question8)
                    chart = px.bar(Video_counts, x='Video Count', y='Channel Name',
                             title=f'Number of Videos Published by Each Channel in {Input_Year}',
                             orientation='h')
                    st.plotly_chart(chart)
            except:
                st.warning('Enter the year in 4 digit number')
        
    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question9 = Question_9()
            df_Question9.index += 1
            df_Question9.index.name = 'S No.'
            st.dataframe(df_Question9)
            chart = px.bar(df_Question9, x='Average Duration', y='Channel Name',
                     title='Average Duration of Videos for Each Channel',
                     orientation='h')
            st.plotly_chart(chart)
         
    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        with st.spinner('Kindly await while we retrieve the outcome'):
            df_Question10 = Question_10()
            df_Question10.index += 1
            df_Question10.index.name = 'S No.'
            st.dataframe(df_Question10)

            Chart = px.bar(df_Question10, x = 'Video Name', y = 'Comment Count', color = 'Channel Name', title = 'Videos with highest number of comments by Channel')
            st.plotly_chart(Chart)
        
