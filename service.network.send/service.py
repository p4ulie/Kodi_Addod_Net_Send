# -*- coding: utf-8 -*-
import time
import xbmc
import xbmcgui
import xbmcaddon

addon = xbmcaddon.Addon()

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

    def onPlayBackStarted(self):
        # turn light switch off
        if self.enabled_global_toggle:
            self.now_playing('1')
            if self.movie_playing and self.active_for_movies_toggle:
                pass
            if self.tv_show_playing and self.active_for_tvshows_toggle:
                pass
        xbmcgui.Dialog().ok('Netsend','Playback start')
        xbmc.log("NetSend addon - Playback started at %s" % time.time(), level=xbmc.LOGINFO)

    def onPlayBackStopped(self):
        # turn light switch on
        self.now_playing('0')
        xbmc.log("NetSend addon - Playback stopped at %s" % time.time(), level=xbmc.LOGINFO)

    def onPlayBackEnded(self):
        # turn light switch on
        self.now_playing('0')
        xbmc.log("NetSend addon - Playback ended at %s" % time.time(), level=xbmc.LOGINFO)

    def onPlayBackPaused(self):
        # turn light switch on
        self.now_playing('1')
        xbmc.log("NetSend addon - Playback paused at %s" % time.time(), level=xbmc.LOGINFO)

    def onPlayBackResumed(self):
        # turn light switch off
        self.now_playing('1')
        xbmc.log("NetSend addon - Playback resumed at %s" % time.time(), level=xbmc.LOGINFO)

    def now_playing(self, event):
        # check media type when a video starts, pauses, or resumes
        if event == '1':
            query = {'jsonrpc': '2.0', 'method': 'Player.GetItem', 'params': { 'properties': ['showtitle', 'season', 'episode', 'duration', 'streamdetails'], 'playerid': 1 }, 'id': 'VideoGetItem'}
            response = json.loads(xbmc.executeJSONRPC(json.dumps(query)))
            if response['result']['item']['type'] == 'movie':
                self.movie_playing = True
                self.tv_show_playing = False
                log(response, 'DEBUG')
            elif response['result']['item']['type'] == 'episode':
                self.movie_playing = False
                self.tv_show_playing = True
                log(response, 'DEBUG')
            else:
                self.movie_playing = False
                self.tv_show_playing = False
                log(response, 'DEBUG')

    def update_settings(self):
        # update variables
        self.enabled_global_toggle = addon.getSetting('enabledGlobal_toggle')
        self.active_for_movies_toggle = addon.getSetting('activeForMovies_toggle')
        self.active_for_tvshows_toggle = addon.getSetting('activeForTVshows_toggle')

        self.enabled_group_01_toggle = addon.getSetting('enabledGroup01_toggle')
        self.host_list_01 = addon.getSetting('hostList10')
        self.command_on_01 = addon.getSetting('command10On')
        self.command_off_01 = addon.getSetting('command10Off')

        self.enabled_group_02_toggle = addon.getSetting('enabledGroup02_toggle')
        self.host_list_02 = addon.getSetting('hostList20')
        self.command_on_02 = addon.getSetting('command20On')
        self.command_off_02 = addon.getSetting('command20Off')


def main():

    player = Player_Monitor()
    settings = Settings_Monitor(player)
    monitor = xbmc.Monitor()

    xbmc.log("NetSend addon starting at %s" % time.time(), level=xbmc.LOGINFO)

    while not monitor.abortRequested():
        if monitor.waitForAbort(1):
            # Abort was requested while waiting. We should exit
            break
        # xbmc.log("NetSend addon periodic notice at %s" % time.time(), level=xbmc.LOGINFO)

    xbmc.log("NetSend addon ending at %s" % time.time(), level=xbmc.LOGINFO)

if __name__ == '__main__':

    xbmc.log("NetSend addon initialized at %s" % time.time(), level=xbmc.LOGINFO)

    main()
