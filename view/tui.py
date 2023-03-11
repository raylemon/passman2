"""
    Terminal User Interface
"""
from __future__ import annotations
import colorama
from colorama import Fore, Style

import controller.tui_controller as ctrl


class Tui:
    """
    Terminal User Interface
    """

    __controller: ctrl.TuiController

    def __init__(self) -> None:
        """
        Constructor. Initializes colorama
        """
        colorama.init(autoreset=True)

    @property
    def controller(self) -> ctrl.TuiController:
        """
        Getter - Get controller

        Returns:
            Tui Controller
        """
        try:
            return self.__controller
        except AttributeError:
            self.show_error("Contrôleur non assigné")
            exit(-1)

    @controller.setter
    def controller(self, value: ctrl.TuiController) -> None:
        """
        Setter

        Arguments:
            value -- Controller
        """
        self.__controller = value

    @staticmethod
    def show_message(message: str) -> None:
        """
        Print a message to screen

        Arguments:
            message -- Message to print
        """
        print(message)

    @staticmethod
    def show_error(message: str) -> None:
        """
        Print error message to screen

        Arguments:
            message -- message to print. Appears in RED
        """
        print(Fore.RED + message)  # type: ignore

    def show_main_menu(self) -> None:
        """
        Show main menu
        """

        while (choice := "") != "0":
            colorama.ansi.clear_screen()
            print(Style.BRIGHT + "PASSMAN - PASSword MANager".center(100, "#"))  # type: ignore

            print(
                """
                    \r1. Connexion.
                    \r2. Nouvel utilisateur.
                    \r3. Supprimer un utilisateur.
                    
                    \r0. Quitter.
                    """
            )
            while not choice.isdigit() and choice not in ["0", "1", "2", "3"]:
                choice = self.ask("Votre choix: ")

                match int(choice):
                    case 0:
                        self.controller.exit()
                    case 1:
                        self.login()
                    case 2:
                        self.create_user()
                    case 3:
                        self.remove_user()
                    case _:
                        self.show_error("Choix invalide. Veuillez réessayer.")

    def show_vault_menu(self) -> None:
        """
        Show vault menu

        """
        choice = ""
        while choice != "0":
            colorama.ansi.clear_screen()
            print(Style.BRIGHT + "Votre coffre-fort".center(100, "#"))  # type: ignore

            print(
                """
                \r1. Voir les éléments.
                \r2. Voir les détails d’un élément.
                \r3. Ajouter un élément.
                \r4. Modifier un élément.
                \r5. Supprimer un élément.
                \r6. Rechercher un élément par son nom.
                
                \r0. Fermer le coffre-fort.
            """
            )
            choice = self.ask("Votre choix: ")
            while not choice.isdigit() and choice not in [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
            ]:
                match int(choice):
                    case 0:
                        return
                    case 1:
                        self.list_elements()
                    case 2:
                        self.show_details()
                    case 3:
                        self.add_element()
                    case 4:
                        self.edit_element()
                    case 5:
                        self.remove_element()
                    case 6:
                        self.search_by_name()
                    case _:
                        self.show_error("Choix invalide. Veuillez réessayer.")

    @staticmethod
    def ask(prompt: str, default: str = "") -> str:
        """
        Ask user

        Arguments:
            prompt -- Message to print

        Keyword Arguments:
            default -- default value (default: {""})

        Returns:
            Answer or default value
        """
        if default != "":
            return input(f"{prompt} ({default}): ")
        else:
            return input(prompt)

    def login(self) -> None:
        """
        _summary_
        """
        user_name = self.ask("Entrez le nom d’utilisateur: ")
        user_password = self.ask("Entrez votre mot de passe: ")
        if self.controller.login(user_name, user_password):
            self.show_vault_menu()

    def create_user(self) -> None:
        """
        _summary_
        """
        user_name = self.ask("Entrez le nom d’utilisateur: ")
        user_password = self.ask("Entrez votre mot de passe: ")
        password_confirm = self.ask("Confirmez votre mot de passe: ")
        if user_password == password_confirm:
            self.controller.create_user(user_name, user_password)

    def remove_user(self) -> None:
        """
        _summary_
        """
        user_name = self.ask("Entrez le nom d’utilisateur: ")
        user_password = self.ask("Entrez votre mot de passe: ")
        self.controller.remove_user(user_name, user_password)

    def show_details(self) -> None:
        """
        _summary_
        """
        element_name = self.ask("Entrez le nom d’un élément: ")
        _, login, password = self.controller.show_details(element_name)
        self.show_message(f"Login: {login}, mot de passe: {password}")

    def add_element(self) -> None:
        """
        _summary_
        """
        element_name = self.ask("Entrez le nom d’un élément: ")
        element_login = self.ask("Entrez le login de l’élément: ")
        element_password = self.ask("Entrez le mot de passe de l’élément: ")
        self.controller.add_element(element_name, element_login, element_password)

    def edit_element(self) -> None:
        """
        _summary_
        """
        element_name = self.ask("Entrez le nom d’un élément: ")
        oen, oel, oep = self.controller.get_element(element_name)

        nen = self.ask(
            "Entrez le nouveau nom de l’élément ou laissez vide pour le conserver.", oen
        )
        nel = self.ask(
            "Entrez le nouveau login de l’élément ou laissez vide pour le conserver.",
            oel,
        )
        nep = self.ask(
            "Entrez le nouveau nom de l’élément ou laissez vide pour le conserver.", oep
        )

        self.controller.edit_element(element_name, nen, nel, nep)

    def remove_element(self) -> None:
        """
        _summary_
        """
        element_name = self.ask("Entrez le nom de l’élément: ")
        self.controller.remove_element(element_name)

    def search_by_name(self) -> None:
        """
        _summary_
        """
        query = self.ask("Entrez le début du nom de l’élément: ")
        for item in self.controller.search_by_name(query):
            self.show_message(item)

    def list_elements(self) -> None:
        """
        _summary_
        """
        for item in self.controller.list_elements():
            self.show_message(item)
        self.ask("Appuyez sur une touche pour continuer.")
