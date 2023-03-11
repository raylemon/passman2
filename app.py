"""
Main script.
"""
from controller.tui_controller import TuiController
from model.data import UserStorage
from view.tui import Tui

if __name__ == "__main__":
    view = Tui()
    storage = UserStorage()
    controller = TuiController(view,storage)

    F_NAME = "data.dat"

    storage.load(F_NAME)

    view.controller = controller
    controller.start()

    storage.save(F_NAME)
