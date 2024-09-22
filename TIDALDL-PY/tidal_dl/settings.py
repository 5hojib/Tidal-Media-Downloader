#!/usr/bin/env python
"""
@File    :   settings.py
@Time    :   2020/11/08
@Author  :   Yaronzz
@Version :   3.0
@Contact :   yaronhuang@foxmail.com
@Desc    :
"""

from __future__ import annotations

import json
import base64

import aigpy
from enums import *
from lang.language import *


class Settings(aigpy.model.ModelBase):
    checkExist = True
    includeEP = True
    saveCovers = True
    language = 0
    lyricFile = False
    apiKeyIndex = 0
    showProgress = True
    showTrackInfo = True
    saveAlbumInfo = False
    downloadVideos = True
    multiThread = False
    downloadDelay = True

    downloadPath = "./download/"
    audioQuality = AudioQuality.Normal
    videoQuality = VideoQuality.P360
    usePlaylistFolder = True
    albumFolderFormat = R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
    playlistFolderFormat = R"Playlist/{PlaylistName} [{PlaylistUUID}]"
    trackFileFormat = R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
    videoFileFormat = R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"

    def getDefaultPathFormat(self, type: Type) -> str:
        if type == Type.Album:
            return R"{ArtistName}/{Flag} {AlbumTitle} [{AlbumID}] [{AlbumYear}]"
        if type == Type.Playlist:
            return R"Playlist/{PlaylistName} [{PlaylistUUID}]"
        if type == Type.Track:
            return R"{TrackNumber} - {ArtistName} - {TrackTitle}{ExplicitFlag}"
        if type == Type.Video:
            return R"{VideoNumber} - {ArtistName} - {VideoTitle}{ExplicitFlag}"
        return ""

    def getAudioQuality(self, value):
        for item in AudioQuality:
            if item.name == value:
                return item
        return AudioQuality.Normal

    def getVideoQuality(self, value):
        for item in VideoQuality:
            if item.name == value:
                return item
        return VideoQuality.P360

    def read(self, path) -> None:
        self._path_ = path
        txt = aigpy.file.getContent(self._path_)
        if len(txt) > 0:
            data = json.loads(txt)
            if aigpy.model.dictToModel(data, self) is None:
                return

        self.audioQuality = self.getAudioQuality(self.audioQuality)
        self.videoQuality = self.getVideoQuality(self.videoQuality)

        if self.albumFolderFormat is None:
            self.albumFolderFormat = self.getDefaultPathFormat(Type.Album)
        if self.trackFileFormat is None:
            self.trackFileFormat = self.getDefaultPathFormat(Type.Track)
        if self.playlistFolderFormat is None:
            self.playlistFolderFormat = self.getDefaultPathFormat(Type.Playlist)
        if self.videoFileFormat is None:
            self.videoFileFormat = self.getDefaultPathFormat(Type.Video)
        if self.apiKeyIndex is None:
            self.apiKeyIndex = 0

        LANG.setLang(self.language)

    def save(self) -> None:
        data = aigpy.model.modelToDict(self)
        data["audioQuality"] = self.audioQuality.name
        data["videoQuality"] = self.videoQuality.name
        txt = json.dumps(data)
        aigpy.file.write(self._path_, txt, "w+")


class TokenSettings(aigpy.model.ModelBase):
    userid = None
    countryCode = None
    accessToken = None
    refreshToken = None
    expiresAfter = 0

    def __encode__(self, string):
        sw = bytes(string, "utf-8")
        return base64.b64encode(sw)

    def __decode__(self, string):
        try:
            sr = base64.b64decode(string)
            return sr.decode()
        except:
            return string

    def read(self, path) -> None:
        self._path_ = path
        txt = aigpy.file.getContent(self._path_)
        if len(txt) > 0:
            data = json.loads(self.__decode__(txt))
            aigpy.model.dictToModel(data, self)

    def save(self) -> None:
        data = aigpy.model.modelToDict(self)
        txt = json.dumps(data)
        aigpy.file.write(self._path_, self.__encode__(txt), "wb")


# Singleton
SETTINGS = Settings()
TOKEN = TokenSettings()
