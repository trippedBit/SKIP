from unittest import TestCase

import os
import shutil

import SKIP


class TestClassSKIP(TestCase):
    def setUp(self) -> None:
        shutil.copy("unittests/unittest_game/movies/movie_01.bik.bak",
                    "unittests/unittest_game/movies/movie_01.bik")
        shutil.copy("unittests/unittest_game/movies/movie_02.mp4.bak",
                    "unittests/unittest_game/movies/movie_02.mp4")
        return super().setUp()

    def tearDown(self) -> None:
        if os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip"):
            os.remove("unittests/unittest_game/movies/movie_01.bik.skip")
        if os.path.exists("unittests/unittest_game/movies/movie_01.bik"):
            os.remove("unittests/unittest_game/movies/movie_01.bik")
        if os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip"):
            os.remove("unittests/unittest_game/movies/movie_02.mp4.skip")
        if os.path.exists("unittests/unittest_game/movies/movie_02.mp4"):
            os.remove("unittests/unittest_game/movies/movie_02.mp4")
        return super().tearDown()

    def test_getFolderFromRegistry(self):
        returnedString = SKIP.getFolderFromRegistry(hkeyType="HKEY_LOCAL_MACHINE",
                                                    path="SOFTWARE/Microsoft/MediaPlayer",
                                                    name="Installation Directory")
        assert returnedString != "", \
            "Could not read registry key value."

    def test_renameFile_folder_given_no_dryRun(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game",
                                      folder="movies",
                                      file="movie_01.bik",
                                      dryRun=False)
        assert returnValue is True, \
            "renameFile returned False."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is False, \
            "File to rename still exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is True, \
            "Renamed file does not exist."

    def test_renameFile_folder_given_dryRun(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game",
                                      folder="movies",
                                      file="movie_01.bik",
                                      dryRun=True)
        assert returnValue is False, \
            "renameFile returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is True, \
            "File to rename does not exist."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is False, \
            "Renamed file does exist."

    def test_renameFile_no_folder_given_no_dryRun(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game/movies",
                                      folder="",
                                      file="movie_01.bik",
                                      dryRun=False)
        assert returnValue is True, \
            "renameFile returned False."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is False, \
            "File to rename still exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is True, \
            "Renamed file does not exist."

    def test_renameFile_no_folder_given_dryRun(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game/movies",
                                      folder="",
                                      file="movie_01.bik",
                                      dryRun=True)
        assert returnValue is False, \
            "renameFile returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is True, \
            "File to rename does not exist."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is False, \
            "Renamed file does exist."

    def test_renameFile_folder_does_not_exist(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game/movies",
                                      folder="videos",
                                      file="movie_01.bik",
                                      dryRun=False)
        assert returnValue is False, \
            "renameFile returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is True, \
            "File to rename does not exist."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is False, \
            "Renamed file does exist."

    def test_renameFile_file_does_not_exist(self):
        returnValue = SKIP.renameFile(installationFolder="unittests/unittest_game/movies",
                                      folder="movies",
                                      file="movie_99.bik",
                                      dryRun=False)
        assert returnValue is False, \
            "renameFile returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik") is True, \
            "File to rename does not exist."
        assert os.path.exists("unittests/unittest_game/movies/movie_01.bik.skip") is False, \
            "Renamed file does exist."

    def test_copyReplacement(self):
        os.rename("unittests/unittest_game/movies/movie_02.mp4",
                  "unittests/unittest_game/movies/movie_02.mp4.skip")
        returnValue = SKIP.copyReplacement(installationFolder="unittests/unittest_game",
                                           folder="movies",
                                           file="movie_02.mp4",
                                           replacement="black_pixel.mp4",
                                           dryRun=False)
        assert returnValue is True, \
            "copyReplacement returned False."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4") is True, \
            "Replaced file exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip") is True, \
            "File backup does not exist."

    def test_copyReplacement_dryRun(self):
        os.rename("unittests/unittest_game/movies/movie_02.mp4",
                  "unittests/unittest_game/movies/movie_02.mp4.skip")
        returnValue = SKIP.copyReplacement(installationFolder="unittests/unittest_game",
                                           folder="movies",
                                           file="movie_02.mp4",
                                           replacement="black_pixel.mp4",
                                           dryRun=True)
        assert returnValue is True, \
            "copyReplacement returned False."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4") is False, \
            "Replaced file exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip") is True, \
            "File backup does not exist."

    def test_copyReplacement_file_does_not_exist(self):
        os.rename("unittests/unittest_game/movies/movie_02.mp4",
                  "unittests/unittest_game/movies/movie_02.mp4.skip")
        returnValue = SKIP.copyReplacement(installationFolder="unittests/unittest_game",
                                           folder="movies",
                                           file="movie_99.mp4",
                                           replacement="black_pixel.mp4",
                                           dryRun=False)
        assert returnValue is False, \
            "copyReplacement returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4") is False, \
            "Replaced file exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip") is True, \
            "File backup does not exist."

    def test_copyReplacement_folder_does_not_exist(self):
        os.rename("unittests/unittest_game/movies/movie_02.mp4",
                  "unittests/unittest_game/movies/movie_02.mp4.skip")
        returnValue = SKIP.copyReplacement(installationFolder="unittests/unittest_game",
                                           folder="videos",
                                           file="movie_02.mp4",
                                           replacement="black_pixel.mp4",
                                           dryRun=False)
        assert returnValue is False, \
            "copyReplacement returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4") is False, \
            "Replaced file exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip") is True, \
            "File backup does not exist."

    def test_copyReplacement_replacement_does_not_exist(self):
        os.rename("unittests/unittest_game/movies/movie_02.mp4",
                  "unittests/unittest_game/movies/movie_02.mp4.skip")
        returnValue = SKIP.copyReplacement(installationFolder="unittests/unittest_game",
                                           folder="movies",
                                           file="movie_02.mp4",
                                           replacement="black_pixel_99.mp4",
                                           dryRun=False)
        assert returnValue is False, \
            "copyReplacement returned True."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4") is False, \
            "Replaced file exists."
        assert os.path.exists("unittests/unittest_game/movies/movie_02.mp4.skip") is True, \
            "File backup does not exist."
