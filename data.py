"""
Data classes
"""


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
        ODO

                Returns:
                    Returns a sorted list of the names of all elements stored in the vault. description
        """
        return sorted(self.elements.keys())

    def get_element(self, element_name: str) -> VaultItem:
        """
        Returns the VaultItem with the given name, if it exists in the vault.

        Arguments:
            element_name -- name of the VaultItem to retrieve

        Returns:
            The VaultItem with the given name, if it exists in the vault.
        """
        if element_name in self.elements:
            return self.elements[element_name]
        else:
            pass  # TODO error

    def add_element(self, item: VaultItem) -> None:
        """
        Adds a VaultItem to the vault, using its name as the key.

        Arguments:
            item -- The VaultItem to add to the vault.
        """
        if item.name not in self.elements:
            self.elements[item.name] = item
        else:
            pass  #  TODO error

    def edit_element(self, old_item: VaultItem, new_item: VaultItem) -> None:
        """
        Replaces an old VaultItem with a new one.

        Arguments:
            old_item -- The VaultItem to be replaced.
            new_item -- The VaultItem to replace it with.
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
        else:
            pass  # TODO error

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
        return sorted(els)

    def element_exists(self, name: str) -> bool:
        """
        Checks if a VaultItem with the given name exists in the vault.

        Arguments:
            name -- The name to check for in the vault.

        Returns:
            True if a VaultItem with the given name exists in the vault, False otherwise.
        """
        return name in self.elements


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
        self.password = password

    def verify_password(self, password: str) -> bool:
        """
        Verify if the given password matches the user's password.

        Arguments:
            password -- The password to verify.

        Returns:
            True if the given password matches the user's password, False otherwise.
        """
        return password == self.password

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
