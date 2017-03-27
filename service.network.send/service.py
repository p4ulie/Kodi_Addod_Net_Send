# -*- coding: utf-8 -*-
import json
import time
import xbmc
import xbmcgui
import xbmcaddon
import requests

addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

class Settings_Monitor(xbmc.Monitor):
    def __init__(self, player):
        self.player = player
        self.movie_playing = None
        self.tv_show_playing = None

    def onSettingsChanged(self):
        self.player.update_settings()

class Player_Monitor(xbmc.Player):
    def __init__(self):
        self.update_settings()
        self.movie_playing = None
        self.tv_show_playing = None
        self.other_playing = None

    def send_command_on(self):

        xbmc.log("%s: Toggle Group 01: %s" % (addonname, self.enabled_group_01_toggle), level=xbmc.LOGNOTICE)
        xbmc.log("%s: Toggle Group 02: %s" % (addonname, self.enabled_group_02_toggle), level=xbmc.LOGNOTICE)

        if self.enabled_group_01_toggle == "true":
            if self.url_list_01 != "":
                url_list = self.url_list_01.split(';')
                for url in url_list:
                    xbmc.log("%s: Group 01, sending %s to %s" % (addonname, self.command_on_01, url), level=xbmc.LOGNOTICE)
                    r = requests.put(url, data=self.command_on_01)

        if self.enabled_group_02_toggle == "true":
            if self.url_list_02 != "":
                url_list = self.url_list_02.split(';')
                for url in url_list:
                    xbmc.log("%s: Group 02, sending %s to %s" % (addonname, self.command_on_02, url), level=xbmc.LOGNOTICE)
                    r = requests.put(url, data=self.command_on_01)


    def send_command_off(self):

        xbmc.log("%s: Toggle Group 01: %s" % (addonname, self.enabled_group_01_toggle), level=xbmc.LOGNOTICE)
        xbmc.log("%s: Toggle Group 02: %s" % (addonname, self.enabled_group_02_toggle), level=xbmc.LOGNOTICE)

        if self.enabled_group_01_toggle == "true":
            if self.url_list_01 != "":
                url_list = self.url_list_01.split(';')
                for url in url_list:
                    xbmc.log("%s: Group 01, sending %s to %s" % (addonname, self.command_off_01, url), level=xbmc.LOGNOTICE)
                    r = requests.put(url, data=self.command_off_01)

        if self.enabled_group_02_toggle == "true":
            if self.url_list_02 != "":
                url_list = self.url_list_02.split(';')
                for url in url_list:
                    xbmc.log("%s: Group 02, sending %s to %s" % (addonname, self.command_off_02, url), level=xbmc.LOGNOTICE)
                    r = requests.put(url, data=self.command_off_01)

    def onPlayBackStarted(self):
        # turn light switch off

        xbmc.log("NetSend addon - Playback started at %s" % time.time(), level=xbmc.LOGNOTICE)

        if self.enabled_global_toggle == "true":
            self.now_playing()
            if self.movie_playing and self.active_for_movies_toggle == "true":
                self.send_command_off()
            if self.tv_show_playing and self.active_for_tvshows_toggle == "true":
                self.send_command_off()
            if self.other_playing and self.active_for_other_toggle == "true":
                self.send_command_off()

    def onPlayBackStopped(self):
        # turn light switch on

        xbmc.log("NetSend addon - Playback stopped at %s" % time.time(), level=xbmc.LOGNOTICE)

        if self.enabled_global_toggle == "true":
            if self.movie_playing and self.active_for_movies_toggle == "true":
                self.send_command_on()
            if self.tv_show_playing and self.active_for_tvshows_toggle == "true":
                self.send_command_on()
            if self.other_playing and self.active_for_other_toggle == "true":
                self.send_command_on()

    def onPlayBackEnded(self):
        # turn light switch on

        xbmc.log("NetSend addon - Playback ended at %s" % time.time(), level=xbmc.LOGNOTICE)

        if self.enabled_global_toggle == "true":
            if self.movie_playing and self.active_for_movies_toggle == "true":
                self.send_command_on()
            if self.tv_show_playing and self.active_for_tvshows_toggle == "true":
                self.send_command_on()
            if self.other_playing and self.active_for_other_toggle == "true":
                self.send_command_on()

    def onPlayBackPaused(self):
        # turn light switch on

        xbmc.log("NetSend addon - Playback paused at %s" % time.time(), level=xbmc.LOGNOTICE)

        if self.enabled_global_toggle == "true":
            self.now_playing()
            if self.movie_playing and self.active_for_movies_toggle == "true":
                self.send_command_on()
            if self.tv_show_playing and self.active_for_tvshows_toggle == "true":
                self.send_command_on()
            if self.other_playing and self.active_for_other_toggle == "true":
                self.send_command_on()

    def onPlayBackResumed(self):
        # turn light switch off

        xbmc.log("NetSend addon - Playback resumed at %s" % time.time(), level=xbmc.LOGNOTICE)

        if self.enabled_global_toggle == "true":
            self.now_playing()
            if self.movie_playing and self.active_for_movies_toggle == "true":
                self.send_command_off()
            if self.tv_show_playing and self.active_for_tvshows_toggle == "true":
                self.send_command_off()
            if self.other_playing and self.active_for_other_toggle == "true":
                self.send_command_off()

    def now_playing(self):
        # check media type when a video starts, pauses, or resumes
        query = {'jsonrpc': '2.0', 'method': 'Player.GetItem', 'params': { 'properties': ['showtitle', 'season', 'episode', 'duration', 'streamdetails'], 'playerid': 1 }, 'id': 'VideoGetItem'}
        response_json = xbmc.executeJSONRPC(json.dumps(query))
        response = json.loads(response_json)

        xbmc.log("%s: Media info: %s" % (addonname, response_json), level=xbmc.LOGNOTICE)

        if response['result']['item']['type'] == 'movie':
            self.movie_playing = True
            self.tv_show_playing = False
            self.other_playing = False
        elif response['result']['item']['type'] == 'episode':
            self.movie_playing = False
            self.tv_show_playing = True
            self.other_playing = False
        else:
            self.movie_playing = False
            self.tv_show_playing = False
            self.other_playing = True

    def update_settings(self):
        # update variables
        self.enabled_global_toggle = addon.getSetting('enabledGlobal_toggle')
        self.active_for_movies_toggle = addon.getSetting('activeForMovies_toggle')
        self.active_for_tvshows_toggle = addon.getSetting('activeForTVshows_toggle')
        self.active_for_other_toggle = addon.getSetting('activeForOther_toggle')

        self.enabled_group_01_toggle = addon.getSetting('enabledGroup01_toggle')
        self.url_list_01 = addon.getSetting('urlList10')
        self.command_on_01 = addon.getSetting('command10On')
        self.command_off_01 = addon.getSetting('command10Off')

        self.enabled_group_02_toggle = addon.getSetting('enabledGroup02_toggle')
        self.url_list_02 = addon.getSetting('urlList20')
        self.command_on_02 = addon.getSetting('command20On')
        self.command_off_02 = addon.getSetting('command20Off')


def main():

    player = Player_Monitor()
    settings = Settings_Monitor(player)
    monitor = xbmc.Monitor()

    xbmc.log("%s: Starting" % (addonname, ), level=xbmc.LOGNOTICE)

    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        # xbmc.log("NetSend addon periodic notice at %s" % time.time(), level=xbmc.LOGNOTICE)

    xbmc.log("%s: Ending" % (addonname, ), level=xbmc.LOGNOTICE)

if __name__ == '__main__':

    xbmc.log("%s: Initialized" % (addonname, ), level=xbmc.LOGNOTICE)

    main()
