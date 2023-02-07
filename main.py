import sys
from pathlib import Path

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QMainWindow, QApplication, QLayout, QPushButton, QMessageBox, QFileDialog
from display import main_window
from dependencies.app_config import get_list_files, get_paths_to_files, copy_file_to_files


class Application(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__enable_pdf_mode()

        self.__create_buttons(layout=self.layProLessons, folder_name="lessons", prefix="pro")
        self.__create_buttons(layout=self.layProExamples, folder_name="examples", prefix="pro")
        self.__create_buttons(layout=self.layLessons, folder_name="lessons", prefix="lesson")
        self.__create_buttons(layout=self.layExamples, folder_name="examples", prefix="example")

        # AUTH WINDOW START
        self.btnSuper.clicked.connect(lambda: self.__auth(login=self.ledtLogin.text()))
        self.btnStudent.clicked.connect(lambda: self.stackMain.setCurrentWidget(self.pgStudent))
        # AUTH WINDOW END
        # STUDENT WINDOW START
        self.stackStudent.setCurrentWidget(self.pgLessons)
        self.btnOpenExamples.clicked.connect(lambda: self.stackStudent.setCurrentWidget(self.pgExamples))
        self.btnOpenLessons.clicked.connect(lambda: self.stackStudent.setCurrentWidget(self.pgLessons))
        self.btnExit.clicked.connect(lambda: self.close())
        self.btnExit_2.clicked.connect(lambda: self.close())
        # STUDENT WINDOW END
        # TEACHER WINDOW START
        self.btnProAddExample.clicked.connect(lambda: self.__add_file_to_files(folder_name="examples"))
        self.btnProAddLesson.clicked.connect(lambda: self.__add_file_to_files(folder_name="lessons"))
        self.btnProDelExample.clicked.connect(lambda: self.__delete_file_from_files(folder_name="examples"))
        self.btnProDelLesson.clicked.connect(lambda: self.__delete_file_from_files(folder_name="lessons"))
        # TEACHER WINDOW END

    def __auth(self, login: str):
        import hashlib
        if hashlib.sha256(
                login.encode()).hexdigest() == "17c1532ca6cff8f6a3a8200028af6c2580bf37f39e10cb0966e8a573e3b24a1f":
            self.stackMain.setCurrentWidget(self.pgProfessor)
        else:
            QMessageBox.warning(self, "ОШИБКА ДОСТУПА", "Проверьте правильность ввода пароля преподавателя")

    def __create_buttons(self, *, layout: QLayout, folder_name: str, prefix: str):
        def add_func(*, index: int):
            paths: list[str] = get_paths_to_files(folder_name=folder_name)
            try:
                match prefix:
                    case "pro":
                        self.brProShow.setUrl(QUrl.fromLocalFile(f"{paths[index]}"))
                    case "example":
                        self.brExampleInfo.setUrl(QUrl.fromLocalFile(f"{paths[index]}"))
                    case "lesson":
                        self.brLessonInfo.setUrl(QUrl.fromLocalFile(f"{paths[index]}"))
            except IndexError:
                QMessageBox.critical(self, "КРИТИЧЕСКАЯ ОШИБКА", "Внутренняя ошибка индекса")

        files: list[str] = get_list_files(folder_name=folder_name)
        for i, file in enumerate(files):
            name, extension = file.split(".")
            button = QPushButton()
            button.setObjectName(f'btn{prefix.capitalize()}_{i}')
            button.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            button.setText(name.upper())
            button.clicked.connect(lambda ch, ind=i: add_func(index=ind))
            layout.addWidget(button)

    def __add_file_to_files(self, folder_name: str):
        def_folder: str = str(Path(Path.home()))
        try:
            cp_from: str = QFileDialog.getOpenFileName(self, "PDF файл",
                                                       directory=def_folder,
                                                       filter="PDF Файлы (*.pdf)")[0]
            copy_file_to_files(copy_from=cp_from, copy_to=folder_name)
        except FileNotFoundError:
            QMessageBox.critical(self, "КРИТИЧЕСКАЯ ОШИБКА", "ОКНО ЗАКРЫТО БЕЗ ВЫБОРА ФАЙЛА")

    def __delete_file_from_files(self, folder_name: str):
        import os
        def_folder: str = str(Path(Path.cwd(), "files", folder_name))
        try:
            deleting_file: str = QFileDialog.getOpenFileName(self, "PDF Файл",
                                                             directory=def_folder,
                                                             filter="PDF Файлы (*.pdf)")[0]
            os.remove(deleting_file)
        except FileNotFoundError:
            QMessageBox.critical(self, "КРИТИЧЕСКАЯ ОШИБКА", "ОКНО ЗАКРЫТО БЕЗ ВЫБОРА ФАЙЛА")

    def __enable_pdf_mode(self):
        self.brProShow.settings().setAttribute(self.brProShow.settings().WebAttribute.PluginsEnabled, True)
        self.brProShow.settings().setAttribute(self.brProShow.settings().WebAttribute.PdfViewerEnabled, True)

        self.brLessonInfo.settings().setAttribute(self.brLessonInfo.settings().WebAttribute.PluginsEnabled, True)
        self.brLessonInfo.settings().setAttribute(self.brLessonInfo.settings().WebAttribute.PdfViewerEnabled, True)

        self.brExampleInfo.settings().setAttribute(self.brExampleInfo.settings().WebAttribute.PluginsEnabled, True)
        self.brExampleInfo.settings().setAttribute(self.brExampleInfo.settings().WebAttribute.PdfViewerEnabled, True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Application()
    window.showMaximized()
    sys.exit(app.exec())
