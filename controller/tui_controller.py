"""
TUI controller
"""
from __future__ import annotations
from model.data import DuplicateError, Vault, VaultItem, UserStorage

from view.tui import Tui


class TuiController:
    """
    TUI Controller
    """
    def __init__(self,view:Tui,storage:UserStorage):
        self.view = view
        self.storage = storage
        self.vault = Vault()

    def start(self) -> None:
        """
        Start
        """
        self.view.show_main_menu()

    def login(self, user_name: str, user_password: str) -> bool:
        """
        Log user
        """
        if (user := self.storage.get_user(user_name)) is not None:
            if user.verify_password(user_password):
                try:
                    self.vault = self.storage.get_vault(user)
                    return True
                except KeyError:
                    self.view.show_error("L’utilisateur n’existe pas.")
                    return False
        else:
            self.view.show_error("L’utilisateur n’existe pas.")
        return False

    def create_user(self, user_name: str, user_password: str) -> None:
        """
        Create user
        """
        if self.storage.get_user(user_name) is None:
            if self.storage.create_user(user_name, user_password):
                self.view.show_message("Utilisateur créé avec succès.")
            else:
                self.view.show_error("L’utilisateur existe déjà. Veuillez réessayer.")
        else:
            self.view.show_error("L’utilisateur existe déjà. Veuillez réessayer.")

    def remove_user(self, user_name: str, user_password: str) -> None:
        """
        Remove a user
        """
        if self.storage.remove_user(user_name, user_password):
            self.view.show_message("Utilisateur supprimé avec succès.")
        else:
            self.view.show_error("Nom d’utilisateur inexistant.")

    def list_elements(self) -> list[str]:
        """
        List all elements
        """
        return self.vault.list_elements()

    def show_details(self, element_name: str) -> tuple[str,str,str]:
        """
        Show element’s details
        """
        try:
            element = self.vault.get_element(element_name)
            return (element.name,element.login,element.password)
        except KeyError:
            self.view.show_error("Pas d’élément à ce nom. Veuillez réessayer.")
            return ("","","")
        
    def add_element(
        self, element_name: str, element_login: str, element_password: str
    ) -> None:
        """
        Add an element in vault
        """
        try:
            v_item = VaultItem(element_name, element_login, element_password)
            self.vault.add_element(v_item)
            self.view.show_message("Élément ajouté avec succès.")
        except DuplicateError:
            self.view.show_error("L’élément existe déjà. Veuillez réessayer.")

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
            self.view.show_error("L’élément n’existe pas. Veuillez réessayer.")

    def remove_element(self, element_name: str) -> None:
        """
        Remove an element
        """
        try:
            v_item = self.vault.get_element(element_name)
            self.vault.remove_element(v_item)
        except KeyError:
            self.view.show_error("L’élément n’existe pas. Veuillez réessayer.")

    def search_by_name(self, query: str) -> list[str]:
        """
        Search an element by it’s name
        """
        lst = []
        for element in self.vault.search_by_name(query):
            lst.append(element.name)
        return lst

    def exit(self) -> None:
        """
        Exit application
        """
        exit()
