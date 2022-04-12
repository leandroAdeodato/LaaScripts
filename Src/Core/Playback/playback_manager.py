# -*- coding: utf-8 -*-
"""
=============================================================================
MODULE: channels_filter.py
-----------------------------------------------------------------------------
This module manages the channelbox selection.
-----------------------------------------------------------------------------
AUTHOR:   Leandro Adeodato
VERSION:  v1.0.0 | Maya 2020 | Python 2
=============================================================================
"""
import maya.cmds as cmd
import maya.mel as mel

import PySide2.QtCore as cor

from LaaScripts.Src.Constants import constants as c
from LaaScripts.Src.Utils import info_utils as info
from LaaScripts.Src.Utils.timeline_utils import TimelineUtils
from LaaScripts.Src.Data.user_data import UserData


class PlaybackManager(object):

    def __init__(self):
        self._user_data = UserData.read_user_data()
        self._next_frame_timer = cor.QTimer()
        self._prev_frame_timer = cor.QTimer()
        self._next_frame_timer.timeout.connect(self.on_next_frame_timeout)
        self._prev_frame_timer.timeout.connect(self.on_prev_frame_timeout)

    def go_to_the_next_frame(self):
        """
        Goes to the next frame time depending on the playback_mode behaviour.
        """
        i = self._user_data[c.TIME_INCREMENT]
        playback_start_time = TimelineUtils.get_playback_range()[0]
        playback_end_time = TimelineUtils.get_playback_range()[1]
        animation_end_time = TimelineUtils.get_animation_range()[1]
        next_time = TimelineUtils.get_current_time() + i

        if next_time > animation_end_time and not self._user_data[c.PLAYBACK_MODE] == c.LOOP:
            return

        if next_time > playback_end_time:
            if self._user_data[c.PLAYBACK_MODE] == c.STOP:
                return
            elif self._user_data[c.PLAYBACK_MODE] == c.LOOP:
                next_time = playback_start_time
            elif self._user_data[c.PLAYBACK_MODE] == c.MOVE:
                TimelineUtils.set_playback_range(playback_start_time + time_increment,
                                                 playback_end_time + time_increment)
            elif self._user_data[c.PLAYBACK_MODE] == c.EXPAND:
                TimelineUtils.set_playback_range(playback_start_time, playback_end_time + time_increment)

        TimelineUtils.set_current_time(next_time)
        info.show_info('Frame >> {0}'.format(int(next_time)))

    def go_to_the_prev_frame(self):
        """
        Goes to the previous frame time depending on the playback_mode behaviour.
        """
        i = self._user_data[c.TIME_INCREMENT]
        playback_start_time = TimelineUtils.get_playback_range()[0]
        playback_end_time = TimelineUtils.get_playback_range()[1]
        animation_start_time = TimelineUtils.get_animation_range()[0]
        prev_time = TimelineUtils.get_current_time() - i

        if prev_time < animation_start_time and not self._user_data[c.PLAYBACK_MODE] == c.LOOP:
            return

        if prev_time < playback_start_time:
            if self._user_data[c.PLAYBACK_MODE] == c.STOP:
                return
            elif self._user_data[c.PLAYBACK_MODE] == c.LOOP:
                prev_time = playback_end_time
            elif self._user_data[c.PLAYBACK_MODE] == c.MOVE:
                TimelineUtils.set_playback_range(playback_start_time - i, playback_end_time - i)
            elif self._user_data[c.PLAYBACK_MODE] == c.EXPAND:
                TimelineUtils.set_playback_range(playback_start_time - i, playback_end_time)

        TimelineUtils.set_current_time(prev_time)
        info.show_info('{0} << Frame'.format(int(prev_time)))

    def next_frame_playback_press(self):
        self.go_to_the_next_frame()
        self._next_frame_timer.start(c.TIMEOUT)

    def prev_frame_playback_press(self):
        self.go_to_the_prev_frame()
        self._prev_frame_timer.start(c.TIMEOUT)

    def next_frame_playback_release(self):
        TimelineUtils.stop_timeline()
        self._next_frame_timer.stop()

    def prev_frame_playback_release(self):
        TimelineUtils.stop_timeline()
        self._prev_frame_timer.stop()

    def on_next_frame_timeout(self):
        TimelineUtils.play_timeline_forward()
        self._next_frame_timer.stop()

    def on_prev_frame_timeout(self):
        TimelineUtils.play_timeline_back()
        self._prev_frame_timer.stop()










