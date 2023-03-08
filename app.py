"""
Main script.
"""
from controller.tui_controller import TuiController
from model.data import UserStorage
from view.tui import Tui


if __name__ == "__main__":
    controller = TuiController()
    view = Tui()
    storage = UserStorage()

    F_NAME = "data.dat"

    storage.load(F_NAME)

    view.controller = controller
    controller.view = view
    controller.storage = storage
    controller.start()

    storage.save(F_NAME)
