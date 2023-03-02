"""
TUI controller
"""
from __future__ import annotations
from model.data import DuplicateError, Vault, VaultItem, UserStorage
#from view.tui import Tui
import view.tui as tui

class TuiController:
    """
    TUI Controller
    """

    _view: tui.Tui
    _storage: UserStorage
    vault: Vault

    @property
    def view(self) -> tui.Tui:
        """
        Get view

        Returns:
            User Interface
        """
        return self._view

    @view.setter
    def view(self, view: tui.Tui) -> None:
        """
        Set view

        Arguments:
            view -- User Interface
        """
        self._view = view

    @property
    def storage(self) -> UserStorage:
        """
        Get storage

        Returns:
            User storage
        """
        return self._storage

    @storage.setter
    def storage(self, storage: UserStorage) -> None:
        """
        Set storage

        Arguments:
            storage -- User storage
        """
        self._storage = storage

    def start(self) -> None:
        """
        Start
        """
        self.view.show_main_menu()

    def login(self, user_name: str, user_password: str) -> None:
        """
        Log user
        """
        if (user := self.storage.get_user(user_name)) is not None:
            if user.verify_password(user_password):
                try:
                    self.vault = self.storage.get_vault(user)
                    self.view.show_vault_menu()
                except KeyError:
                    self.view.print_error("L’utilisateur n’existe pas.")
        else:
            self.view.print_error("L’utilisateur n’existe pas.")

    def create_user(self, user_name: str, user_password: str) -> None:
        """
        Create user
        """
        if self.storage.get_user(user_name) is None:
            if self.storage.create_user(user_name, user_password):
                self.view.print_message("Utilisateur créé avec succès.")
            else:
                self.view.print_error("L’utilisateur existe déjà. Veuillez réessayer.")
        else:
            self.view.print_error("L’utilisateur existe déjà. Veuillez réessayer.")

    def remove_user(self, user_name: str, user_password: str) -> None:
        """
        Remove a user
        """
        if self.storage.remove_user(user_name, user_password):
            self.view.print_message("Utilisateur supprimé avec succès.")
        else:
            self.view.print_error("Nom d’utilisateur inexistant.")

    def list_elements(self) -> None:
        """
        List all elements
        """
        for element in self.vault.list_elements():
            self.view.print_message(element)
        self.view.ask("Appuyez sur une touche pour continuer…")

    def show_details(self, element_name: str) -> None:
        """
        Show element’s details
        """
        try:
            element = self.vault.get_element(element_name)
            self.view.print_message(
                f"login: {element.login}, password: {element.password}"
            )
        except KeyError:
            self.view.print_error("Pas d’élément à ce nom. Veuillez réessayer.")

    def add_element(
        self, element_name: str, element_login: str, element_password: str
    ) -> None:
        """
        Add an element in vault
        """
        try:
            v_item = VaultItem(element_name, element_login, element_password)
            self.vault.add_element(v_item)
            self.view.print_message("Élément ajouté avec succès.")
        except DuplicateError:
            self.view.print_error("L’élément existe déjà. Veuillez réessayer.")

    def get_element(self, element_name: str) -> tuple[str, str, str]:
        """
        _summary_

        Arguments:
            element_name -- _description_

        Returns:
            _description_
        """
        item = self.vault.get_element(element_name)
        return (item.name, item.login, item.password)

    def edit_element(
        self,
        element_name: str,
        new_element_name: str,
        new_element_login: str,
        new_element_password: str,
    ) -> None:
        """
        Edit an element
        """
        try:
            old_item = self.vault.get_element(element_name)
            new_item = VaultItem(
                new_element_name, new_element_login, new_element_password
            )
            self.vault.edit_element(old_item, new_item)
        except KeyError:
            self.view.print_error("L’élément n’existe pas. Veuillez réessayer.")

    def remove_element(self, element_name: str) -> None:
        """
        Remove an element
        """
        try:
            v_item = self.vault.get_element(element_name)
            self.vault.remove_element(v_item)
        except KeyError:
            self.view.print_error("L’élément n’existe pas. Veuillez réessayer.")

    def search_by_name(self, query: str) -> None:
        """
        Search an element by it’s name
        """
        for element in self.vault.search_by_name(query):
            self.view.print_message(element.name)

    def exit(self) -> None:
        """
        Exit application
        """
        exit()
