"""A video player class."""

from video_library import VideoLibrary

import random
import pickle
import os

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currently_playing = None
        self.play_status = False

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        print("Here is a list of all available videos:")
        for vid in self._video_library.get_all_videos():
            print (getattr(vid,"title"),
                   "(",getattr(vid,"video_id"),")",
                   list(getattr(vid,"tags")))

    def play_video(self, video_id):
        #Plays the respective video.
        try:
            vid = self._video_library.get_video(video_id)
            getattr(vid, "title")
        except:
            print("Cannot play video: Video does not exist.")
            return
        else:
            if self.currently_playing is None:
                self.currently_playing = vid
                print("Playing video: " + getattr(vid,"title") )
                self.play_status = True
            else:
                print("Stopping video: " + getattr(self.currently_playing,"title"))
                self.currently_playing = vid
                print("Playing video:"  + self.currently_playing)




    def stop_video(self):
        if self.currently_playing is not None :
            print("Stopping video: " + getattr(self.currently_playing,"title"))
            self.currently_playing = None
            self.play_status = False
        else:
            print("Cannot stop video: No video is currently playing.")


    def play_random_video(self):
        choice = random.choice(self._video_library.get_all_videos())
        self.play_video(getattr(choice,"video_id"))
        """Plays a random video from the video library."""


    def pause_video(self):
        if self.currently_playing is None :
            print ("Cannot pause video: No video is currently playing.")
        else:
            if self.play_status :
                print ("Pausing video: "+ getattr(self.currently_playing,"title"))
                self.play_status = False
            else:
                print ("Video already paused: "+ self.currently_playing)


    def continue_video(self):
        """Resumes playing the current video."""
        if self.currently_playing is None :
            print ("Cannot continue video: No video is currently playing.")
        else:
            if not self.play_status :
                print ("Playing video: "+ getattr(self.currently_playing,"title"))
                self.play_status = True
            else:
                print ("Cannot continue video: Video is not paused.")

    def show_playing(self):
        """Displays video currently playing."""
        if self.currently_playing is None:
            print("No video is currently playing")
        else:
            print (getattr(self.currently_playing,"title"),
                   "(",getattr(self.currently_playing,"video_id"),")",
                   list(getattr(self.currently_playing,"tags")))


    def create_playlist(self, playlist_name):
        new_playlist_path = os.getcwd() + "\playlists\\"+playlist_name + ".pkl"
        if os.path.exists(new_playlist_path):
            print ("Cannot create playlist: A play list with the same name already exists")

        else:
            new_playlist = open(new_playlist_path, "x")
            new_playlist.close()
            print("Successfully created new playlist " + playlist_name)


    def add_to_playlist(self, playlist_name, video_id):
        playlist_path = os.getcwd() + "\playlists\\" + playlist_name + ".pkl"
        try:
            the_playlist = open(playlist_path, "rb")
        except:
            print("Cannot add video to " + playlist_name + ": The playlist does not exist")
            return
        try:
            videos_within = pickle.load(the_playlist)
        except:
            videos_within = []
        try :
            video_to_be_added = self._video_library.get_video(video_id)
            this_vid_title = getattr(video_to_be_added,"title")
            this_vid_id = getattr(video_to_be_added,"video_id")
        except:
            print("Cannot add video to " + playlist_name + ": Video does not exist")

        else:
            vid_ids = [getattr(vid, "video_id") for vid in videos_within]

            if this_vid_id in vid_ids:
                print("Cannot add video to " + playlist_name + ": Video already added")
            else:
                videos_within.append(video_to_be_added)
                the_playlist = open(playlist_path, "wb")
                pickle.dump(videos_within, the_playlist)
                the_playlist.close()
                print("Added video to " + playlist_name + ": " + this_vid_title)


    def show_all_playlists(self):
        playlist_path = os.getcwd() + "\playlists"
        playlist_names =[]
        try:
            for playlist in os.listdir(playlist_path):
                name,extension = playlist.split(".")
                playlist_names.append(name)
        except:
            print("No playlist exists yet")

        else:
            print("Showing all playlists: " )
            for name in playlist_names:
                print("\t" +name)

    def show_playlist(self, playlist_name):
        playlist_path = os.getcwd() + "\playlists\\" + playlist_name + ".pkl"
        try:
            the_playlist = open(playlist_path, "rb")
        except:
            print("Cannot show playlist " + playlist_name + ": The playlist does not exist")
            return
        try:
            videos_within = pickle.load(the_playlist)
        except:
            print("Showing playlist: " + playlist_name + "\n\t No videos here yet")
            return
        else:
            print ("Showing playlist: " + playlist_name)
            for vid in videos_within:
                print ("\t", getattr(vid,"title"),
                       "(",getattr(vid,"video_id"),")",
                       list(getattr(vid,"tags")))



    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        print("deletes_playlist needs implementation")

    def search_videos(self, search_term):
        potential_option = []
        for vids in self._video_library.get_all_videos():
            title = getattr(vids,"title").lower()
            if search_term.lower() in title:
                potential_option.append(vids)

        if len(potential_option) == 0:
            print("No search results for "+ search_term)
        else :
            print("Here are the results for "+ search_term )
            for item in potential_option:
                print(potential_option.index(item)+1,")",
                      getattr(item, "title"),
                      "(", getattr(item, "video_id"), ")"
                      ,list(getattr(item,"tags")))
            choice = int(input("Would you like to play any of the above? If yes, specify the number of the video. \n"
                               "If your answer is not a valid number we will assume it's a no. "))
            try:
                vid = potential_option[choice-1]
            except:
                return
            else:
                self.play_video(getattr(vid,"video_id"))



    def search_videos_tag(self, video_tag):
        potential_option = []
        for vids in self._video_library.get_all_videos():
            tag = list(getattr(vids,"tags"))
            if video_tag.lower() in tag:
                potential_option.append(vids)

        if len(potential_option) == 0:
            print("No search results for " + video_tag)
        else:
            print("Here are the results for " + video_tag)
            for item in potential_option:
                print(potential_option.index(item) + 1, ")",
                      getattr(item, "title"),
                      "(", getattr(item, "video_id"), ")"
                      , list(getattr(item, "tags")))
            choice = int(input("Would you like to play any of the above? If yes, specify the number of the video. \n"
                               "If your answer is not a valid number we will assume it's a no. "))
            try:
                vid = potential_option[choice - 1]
            except:
                return
            else:
                self.play_video(getattr(vid, "video_id"))


    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
