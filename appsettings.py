from PyQt5.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self.settings = QSettings('Tuxtas', 'MyQueryTutor')

    def has_settings(self):
        if self.settings.contains('MainWindow/geometry'):
            return True
        else:
            return False

    def set_geometry(self, main_win, splitter_1, splitter_2):
        self.settings.setValue("MainWindow/geometry", main_win)
        self.settings.setValue("MainWindow/splitter_1", splitter_1)
        self.settings.setValue("MainWindow/splitter_2", splitter_2)

    def get_geometry(self):
        return self.settings.value("MainWindow/geometry")

    def get_splitter_1_geometry(self):
        return self.settings.value('MainWindow/splitter_1', [], int)

    def get_splitter_2_geometry(self):
        return self.settings.value('MainWindow/splitter_2', [], int)
