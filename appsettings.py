from PyQt5.QtCore import QSettings


class AppSettings:
    def __init__(self):
        self.settings = QSettings('Tuxtas', 'MyQueryTutor')

    def databases_set(self):
        if self.settings.contains('MainWindow/geometry'):
            return True
        return False

    def set_geometry(self, byte_array):
        self.settings.setValue("MainWindow/geometry", byte_array)

    def get_geometry(self):
        return self.settings.value("MainWindow/geometry")
