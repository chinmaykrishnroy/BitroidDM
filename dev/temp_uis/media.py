import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog, QFileSystemModel
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl, QFileInfo

from UI.media_player_ui import Ui_media_player


class MediaPlayer (QMainWindow, Ui_media_player):

    current_directory = 'Qt_Media_Player/Audio_Files'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # initialises a media player
        self.player = QMediaPlayer()

        '''
            initialses a file system in a list view(init_folder)
            applies filters so only the listed formats are shown
            nameFilterDisables(False) sets the items without the listed formats are hidden
        '''
        self.model = QFileSystemModel()
        self.model.setNameFilters(['*.mp3', '*.wav', '*.aac', '*.flac'])
        self.model.setNameFilterDisables(False)
        self.init_folder()

        # allows the user to browse their files when file > browse is clicked
        self.actionBrowse.triggered.connect(self.browse_file)

        # exits the app when file > quit is selected
        self.actionQuit.triggered.connect(self.quit)

        # plays the currently selected song from the list when double clicked
        self.folder_view.doubleClicked.connect(self.list_select)

        # runs the player_timer when the track is playing
        self.player.positionChanged.connect(self.player_timer)

        # the playback is played/paused when the play/pause or stop buttons are pressed 
        self.pb_play_pause.clicked.connect(self.play_pause_button)

        # the playback is stopped and current track is cleared from player when stop is pressed
        self.pb_stop.clicked.connect(self.stop_button)

        # moves the track to the next in the list, if one is available when the forward button pressed
        self.pb_forward.clicked.connect(self.forward_button)

        # moves the track to the previous in the list, if one is available when the forward button pressed        
        self.pb_back.clicked.connect(self.back_button)

        # Controls the volume by signaling when the volume bar value is changed
        self.volume_slider.valueChanged.connect(self.volume_control)

    '''
        selected_file is set to the currently seleted item in the list view
        the file path is set to the file path of that file
    '''
    def list_select(self):
        selected_file = self.folder_view.currentIndex()
        self.file_path = self.model.filePath(selected_file)
        self.set_audio()
        self.song_name()

    '''
        Method that runs on startup and allows the user to choose an audio file
        file_filter lists the file types we want to show to the user
        file_path opens a window and lets us choose a file
        file_path returns a tuple with the file path and data types
        we set file_path[0] so we only retrieve the path
        the index of the selected file is set as a variable
        we set the index to be the index variable
    '''
    def browse_file(self):
        file_filter = '*.mp3 *.wav *.aac *.flac'
        self.file_path = QFileDialog.getOpenFileName(
            caption='Select a file', # shows what text appears at the top of the windw
            dir='Qt_Media_Player/Audio_Files', # initialises the directory we display
            filter=file_filter # uses the filter list from earlier to only show files of a certain type
        )
        self.file_path = self.file_path[0]
        selected_index = self.model.index(self.file_path)
        self.folder_view.setCurrentIndex(selected_index)
        self.set_audio()
        self.song_name()
        self.update_folder()

    # kills the program
    def quit(self):
        sys.exit()

    '''
        sets the initial display folder as the current_directory path
        sets the treeView up to follow the model of the directory
    '''
    def init_folder(self):
        self.model.setRootPath(MediaPlayer.current_directory)
        self.folder_view.setModel(self.model)
        self.folder_view.setRootIndex(self.model.index(MediaPlayer.current_directory))
        
    '''
        when you switch to a different directory than the default it will update the display
        this will show the new directory you selected by overridding the current_directory path
    '''
    def update_folder(self):
        file_info = QFileInfo(self.file_url.toLocalFile())
        MediaPlayer.current_directory = file_info.absolutePath()
        self.model.setRootPath(MediaPlayer.current_directory)
        self.folder_view.setModel(self.model)
        self.folder_view.setRootIndex(self.model.index(MediaPlayer.current_directory))
        
    '''
        Method that initialises audio
        If a file is loaded it will remove it with stop so other files can be played
        Sets the url to be the selected file path
        QAudioOutput represents an output channel for audio
        Sets the QMediaPlayer audio output to be the defined audio output
        Tells the player the source of the file is the file we selected in the browse_file method
        Sets the initial volume slider to be 50%
        Calls the volume control method to run which sets the output value
    '''
    def set_audio(self):
        self.player.stop()
        self.file_url = QUrl.fromLocalFile(self.file_path)
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(self.file_url)
        self.volume_slider.setSliderPosition(50)
        self.volume_percent.setText(f'{self.volume_slider.value} + %')
        self.volume_control()
        self.update_folder()
        self.player.play()

    '''
        Converts the file path to a QFileInfo object
        Gives us the name of the file from the QFileInfo object
        Sets the song title label to be the file name we just extracted
    '''
    def song_name(self):
        file_name_info = QFileInfo(self.file_path)
        file_name = file_name_info.fileName()
        self.lb_song_title.setText(file_name)

    '''
        Gets the player position in milliseconds
        Converts milliseconds into seconds and minutes with a // (floor operator)
        Sets the song_time label text to be a string with the minutes and seconds
    '''
    def player_timer(self):
        duration_milliseconds = self.player.duration()
        duration_seconds = duration_milliseconds // 1000
        duration_minutes = duration_seconds // 60
        duration_seconds %= 60  # Reset seconds to 0 when a minute is reached

        playing_milliseconds = self.player.position()
        playing_seconds = playing_milliseconds // 1000
        playing_minutes = playing_seconds // 60
        playing_seconds %= 60  # Reset seconds to 0 when a minute is reached

        # Format the time as mm:ss
        formatted_duration = f"{duration_minutes:02d}:{duration_seconds:02d}"
        formatted_playing = f"{playing_minutes:02d}:{playing_seconds:02d}"

        self.lb_song_time.setText(f"{formatted_playing}/{formatted_duration}")

    '''
        If the song title is '' (no song), the play button runs the list select method to play the selected song
        If the player is playing audio it will pause the player
        If the player is not playing audio it will play the currently active sound file
    '''
    def play_pause_button(self):
        if self.lb_song_title.text() == '':
            self.list_select()
        elif self.player.isPlaying() == True:
            self.player.pause()
        else:
            self.player.play()

    '''
        When the stop button is pressed stops playing and resets the play position to 0
        Sets the song title and song time text to nothing
    '''
    def stop_button(self):
        self.player.stop()
        self.lb_song_title.setText('')
        self.lb_song_time.setText('')

    '''
        Gets the current index of the selected item
        Gets the current row of the selected item
        Creates a sibling of the current item at the next row

        if there is a valid index (as in a file exists)
        the folder_view is set to the new index
        the path is set to the next file in the list
        the audio playback methods run
    '''   
    def forward_button(self):
        current_index = self.folder_view.currentIndex()
        current_row = current_index.row()
        next_row = current_row + 1
        next_index = current_index.siblingAtRow(next_row)

        if next_index.isValid():
            self.folder_view.setCurrentIndex(next_index)
            self.file_path = self.model.filePath(next_index)
            self.set_audio()
            self.song_name()

    def back_button(self):
        current_index = self.folder_view.currentIndex()
        current_row = current_index.row()
        previous_row = current_row - 1
        previous_index = current_index.siblingAtRow(previous_row)

        if previous_index.isValid():
            self.folder_view.setCurrentIndex(previous_index)
            self.file_path = self.model.filePath(previous_index)
            self.set_audio()
            self.song_name()

    '''
        Sets a variable volume to be the volume slider position / 100
        / 100 because the volume output is working on a 0 - 1 scale where 1 is 100%
        Sets the volume percentage text to equal the value of the slider
        Set the audio output to be equal to the volume variable

        Try/except block here to bypass the attribute error for changing the volume controls when no audio file has been setup
    '''
    def volume_control(self):
        try:
            self.volume = self.volume_slider.value() / 100
            self.volume_percent.setText(f'{self.volume_slider.value()}%')
            self.audio_output.setVolume(self.volume)
        except AttributeError:
            pass

# creates an instance of QApplication and executes the program
if __name__ == '__main__':
    app = QApplication(sys.argv)

    player = MediaPlayer()
    player.show()

    # terminates the program if it is exited
    sys.exit(app.exec())