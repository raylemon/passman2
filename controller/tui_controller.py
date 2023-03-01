"""
TUI controller
"""

from model.data import DuplicateError, Vault, VaultItem, UserStorage
from view.tui import Tui


class TuiController:
    """
    TUI Controller
    """

    view: Tui
    storage: UserStorage
    vault: Vault

    def set_view(self, view: Tui) -> None:
        """
        Set view

        Arguments:
            view -- User Interface
        """
        self.view = view

    def set_storage(self, storage: UserStorage) -> None:
        """
        Set storage

        Arguments:
            storage -- User storage
        """
        self.storage = storage

    def start(self) -> None:
        """
        Start
        """
        while (choice := self.view.show_main_menu()) != 0:
            match choice:
                case 0:
                    exit()
                case 1:
                    self.login()
                case 2:
                    self.create_user()
                case 3:
                    self.remove_user()
                case _:
                    self.view.print_error("Choix invalide. Veuillez réessayer.")

    def login(self) -> None:
        """
        Log user
        """
        user_name = self.view.ask("Entrez un nom d’utilisateur: ")
        if (user := self.storage.get_user(user_name)) is not None:
            user_password = self.view.ask("Entrez votre mot de passe: ")
            if user.verify_password(user_password):
                try:
                    self.vault = self.storage.get_vault(user)
                    self.vault_menu()
                except KeyError:
                    self.view.print_error("L’utilisateur n’existe pas.")
        else:
            self.view.print_error("L’utilisateur n’existe pas.")

    def create_user(self) -> None:
        """
        Create user
        """
        user_name = self.view.ask("Entrez un nom d’utilisateur: ")
        if self.storage.get_user(user_name) is None:
            user_password = self.view.ask("Entrez votre mot de passe: ")
            user_confirm = self.view.ask("Confirmez votre mot de passe: ")
            if user_password == user_confirm:
                if self.storage.create_user(user_name, user_password):
                    self.view.print_message("Utilisateur créé avec succès.")
                else:
                    self.view.print_error(
                        "L’utilisateur existe déjà. Veuillez réessayer."
                    )
        else:
            self.view.print_error("L’utilisateur existe déjà. Veuillez réessayer.")

    def remove_user(self) -> None:
        """
        Remove a user
        """
        user_name = self.view.ask("Entrez un nom d’utilisateur: ")
        user_pass = self.view.ask("Entrez votre mot de passe: ")
        if self.storage.remove_user(user_name, user_pass):
            self.view.print_message("Utilisateur supprimé avec succès.")
        else:
            self.view.print_error("Nom d’utilisateur inexistant.")

    def vault_menu(self) -> None:
        """
        Vault menu
        """
        while (choice := self.view.show_vault_menu()) != 0:
            match choice:
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
                    self.view.print_error("Choix invalide. Veuillez réessayer.")

    def list_elements(self) -> None:
        """
        List all elements
        """
        for element in self.vault.list_elements():
            self.view.print_message(element)
        self.view.ask("Appuyez sur une touche pour continuer…")

    def show_details(self) -> None:
        """
        Show element’s details
        """
        element_name = self.view.ask("Entrez le nom d’un élément: ")
        try:
            element = self.vault.get_element(element_name)
            self.view.print_message(
                f"login: {element.login}, password: {element.password}"
            )
        except KeyError:
            self.view.print_error("Pas d’élément à ce nom. Veuillez réessayer.")

    def add_element(self) -> None:
        """
        Add an element in vault
        """
        element_name = self.view.ask("Entrez le nom d’un élément: ")
        try:
            element_login = self.view.ask("Entrez le login de l’élément: ")
            element_password = self.view.ask("Entrez le mot de passe de l’élément: ")

            v_item = VaultItem(element_name, element_login, element_password)
            self.vault.add_element(v_item)
            self.view.print_message("Élément ajouté avec succès.")
        except DuplicateError:
            self.view.print_error("L’élément existe déjà. Veuillez réessayer.")

    def edit_element(self) -> None:
        """
        Edit an element
        """
        element_name = self.view.ask("Entrez le nom d’un élément: ")
        try:
            old_item = self.vault.get_element(element_name)

            new_element_name = self.view.ask(
                "Entrez le nouveau nom de l’élément ou laissez vide pour le conserver.",
                old_item.name,
            )

            new_element_login = self.view.ask(
                "Entrez le nouveau login de l’élément ou laissez vide pour le conserver",
                old_item.login,
            )

            new_element_password = self.view.ask(
                "Entrez le nouveau mot de passe de l’élément ou laissez vide pour le conserver",
                old_item.password,
            )

            new_item = VaultItem(
                new_element_name, new_element_login, new_element_password
            )

            self.vault.edit_element(old_item, new_item)
        except KeyError:
            self.view.print_error("L’élément n’existe pas. Veuillez réessayer.")

    def remove_element(self) -> None:
        """
        Remove an element
        """
        element_name = self.view.ask("Entrez le nom de l’élément: ")
        try:
            v_item = self.vault.get_element(element_name)
            self.vault.remove_element(v_item)
        except KeyError:
            self.view.print_error("L’élément n’existe pas. Veuillez réessayer.")

    def search_by_name(self) -> None:
        """
        Search an element by it’s name
        """
        query = self.view.ask("Entrez le début du nom de l’élément: ")
        for element in self.vault.search_by_name(query):
            self.view.print_message(element.name)
