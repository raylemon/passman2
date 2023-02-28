"""
Data classes
"""
from hashlib import sha512
import pickle
import os
from typing import Optional


class DuplicateError(Exception):
    """
    Duplicate Error
    """

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class VaultItem:
    """
    Vault Item
    """

    def __init__(self, name: str, login: str, password: str) -> None:
        """
        Constructor

        Arguments:
            name -- name of element
            login -- login to store
            password -- password to store
        """
        self.name = name
        self.login = login
        self.password = password


class Vault:
    """
    Vault
    """

    def __init__(self) -> None:
        """
        Constructor
        """
        self.elements: dict[str, VaultItem] = {}

    def list_elements(self) -> list[str]:
        """
        Returns a sorted list of the names of all elements stored in the vault.

        Returns:
            Returns a sorted list of the names of all elements stored in the vault. description
        """
        return sorted(self.elements.keys())

    def get_element(self, element_name: str) -> VaultItem:
        """
        Returns the VaultItem with the given name, if it exists in the vault.

        Arguments:
            element_name -- name of the VaultItem to retrieve

        Raises:
            KeyError: if item does’nt exists

        Returns:
            The VaultItem with the given name, if it exists in the vault.
        """
        if element_name in self.elements:
            return self.elements[element_name]

        raise KeyError(f"{element_name} not found")

    def add_element(self, item: VaultItem) -> None:
        """
        Adds a VaultItem to the vault, using its name as the key.

        Arguments:
            item -- The VaultItem to add to the vault.

        Raises:
            DuplicateError: if item already exists
        """
        if item.name not in self.elements:
            self.elements[item.name] = item
        raise DuplicateError(f"{item} already exists")

    def edit_element(self, old_item: VaultItem, new_item: VaultItem) -> None:
        """
        Replaces an old VaultItem with a new one.

        Arguments:
            old_item -- The VaultItem to be replaced.
            new_item -- The VaultItem to replace it with.

        Raises:
            KeyError: if item are not found
        """
        self.remove_element(old_item)
        self.add_element(new_item)

    def remove_element(self, item: VaultItem) -> None:
        """
        Removes a VaultItem from the vault.

        Arguments:
            item -- The VaultItem to remove from the vault.
        """
        if item.name in self.elements:
            del self.elements[item.name]
        raise KeyError(f"{item} not found")

    def search_by_name(self, search_string: str) -> list[VaultItem]:
        """
        Searches for VaultItems whose name starts with the given search string.

        Arguments:
            search_string -- The string to search for in VaultItem names.

        Returns:
            A sorted list of VaultItems whose name starts with the given search string.
        """
        els = []
        for element, item in self.elements.items():
            if element.startswith(search_string):
                els.append(item)
        return sorted(els, key=lambda it: it.name)


class User:
    """
    Simple User Class
    """

    def __init__(self, login: str, password: str) -> None:
        """
        Constructor

        Arguments:
            login -- login of user. Must be unique
            password -- password of user
        """
        self.login = login
        self.password = sha512(password.encode("utf-8")).hexdigest()

    def verify_password(self, password: str) -> bool:
        """
        Verify if the given password matches the user's password.

        Arguments:
            password -- The password to verify.

        Returns:
            True if the given password matches the user's password, False otherwise.
        """
        return sha512(password.encode("utf-8")).hexdigest() == self.password

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
            A string containing the user's login and password.
        """
        return f"User login = {self.login}, user password = {self.password}"

    def __hash__(self) -> int:
        """
        Return a hash value for the user.

        Returns:
            A hash value computed from the user's login.
        """
        return hash(self.login)


class UserStorage:
    """
    User Storage

    Raises:
        KeyError: Error when User not exists

    Returns:
        Storage class
    """

    users: dict[User, Vault]

    def load(self, filename: str) -> None:
        """
        Load data

        Arguments:
            filename -- file path
        """
        if os.path.exists(filename):
            with open(filename, "br") as file:
                self.users = pickle.load(file)
        else:
            self.users = {}

    def save(self, filename: str) -> None:
        """
        Save data to file

        Arguments:
            filename -- file path
        """
        with open(filename, "wb") as file:
            pickle.dump(self.users, file)

    def get_user(self, username: str) -> Optional[User]:
        """
        Get user from data

        Arguments:
            username -- User name to find

        Returns:
            an User
        """
        for user in self.users:
            if user.login == username:
                return user

        return None

    def remove_user(self, username: str, userpass: str) -> bool:
        """
        Remove user from data

        Arguments:
            username -- user’s name
            userpass -- user’s password

        Returns:
            True if success, False elsewhere
        """
        user = self.get_user(username)
        if user is not None and user.verify_password(userpass):
            del self.users[user]
            return True
        else:
            return False

    def create_user(self, username: str, userpass: str) -> bool:
        """
        Create user and his associated vault

        Arguments:
            username -- user’s name
            userpass -- user’s password

        Returns:
            True if User is successfully created, False elsewhere
        """
        if (user := self.get_user(username)) is not None:
            self.users[user] = Vault()
            return True
        else:
            return False

    def get_vault(self, user: User) -> Vault:
        """
        Get associated vault

        Arguments:
            user -- User associated to vault

        Raises:
            KeyError: if user not exists

        Returns:
            Vault associated to User
        """
        if user is not None:
            return self.users[user]
        raise KeyError(f"{user} not found")
