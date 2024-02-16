-- Create Database named as youtubescrapingsql
create database youtubescrapingsql;

-- Select Database youtubescrapingsql
Use youtubescrapingsql;


-- Create a table as Channel under database youtubescrapingsql
create table Channel(
	channel_id varchar(255) primary key,
    channel_name varchar(255),
    channel_type varchar(255),
    channel_views int,
    channel_description text,
    channel_status varchar(255)
);

-- Create a table as playlist under database youtubescrapingsql
create table playlist(
	playlist_id varchar(255) primary key,
    channel_id varchar(255),
    playlist_name varchar(255),
    foreign key (channel_id) references channel(channel_id)
);


-- Create a table as video under database youtubescrapingsql
create table video(
		video_id varchar(255) primary key,
        playlist_id varchar(255),
        video_name varchar(255),
        video_description text,
        published_date datetime,
        view_count int,
        like_count int,
        dislike_count int,
        favourite_count int,
        comment_count int,
        duration int,
        thumbnail varchar(255),
        caption_status varchar(255),
        foreign key (playlist_id) references playlist(playlist_id)
);


-- Create a table as comment under database youtubescrapingsql
create table comment(
	comment_id varchar(255) primary key,
    video_id varchar(255),
    comment_text text,
    comment_author varchar(255),
    comment_published_date datetime,
    foreign key (video_id) references video(video_id)
);
