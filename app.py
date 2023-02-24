"""
Main script.
"""
from model.data import Vault, VaultItem, User
import pickle
import os


class MainApp:
    """
    Main App class
    """

    active_vault: Vault

    def __init__(self) -> None:
        """
        Constructor
        """
        self.users: dict[User, Vault] = (
            self.load() if os.path.exists("data.dat") else {}
        )

    def save(self) -> None:
        """
        Save data
        """
        with open("data.dat", "bw") as file:
            pickle.dump(self.users, file)

    @staticmethod
    def load() -> dict[User, Vault]:
        """
        load data

        Returns:
            dict with user and associated vault
        """
        with open("data.dat", "br") as file:
            return pickle.load(file)

    @staticmethod
    def ask(prompt: str) -> int:
        """
        Ask the user to input an integer value based on a given prompt.

        Args:
            prompt (str): The prompt displayed to the user.

        Returns:
            int: The integer value entered by the user.
        """
        choice: str = ""
        while not choice.isdigit():
            choice = input(prompt)
        return int(choice)

    def list_elements(self):
        """
        List all the elements stored in the active vault
        """
        for element in self.active_vault.list_elements():
            print(element)

    def show_details(self):
        """
        Display the login and password of a given element from the active vault.
        """
        element_name = input("Entrez le nom d’un élément: ")
        if self.active_vault.element_exists(element_name):
            element = self.active_vault.get_element(element_name)
            print(f"login: {element.login}, password: {element.password}")
        else:
            print("Pas d’élément à ce nom. Veuillez réessayer.")

    def add_element(self):
        """
        Add a new element to the active vault.
        """
        element_name = input("Entrez le nom de l’élément: ")
        if not self.active_vault.element_exists(element_name):
            element_login = input("Entrez le login de l’élément")
            element_password = input("Entrez le password de l’élément")

            vault_item = VaultItem(element_name, element_login, element_password)
            self.active_vault.add_element(vault_item)

        else:
            print("L’élément existe déjà. Veuillez réessayer.")

    def edit_element(self):
        """
        Edit the name, login or password of a given element in the active vault.
        """
        element_name = input("Entrez le nom de l’élément: ")
        if self.active_vault.element_exists(element_name):
            vault_item = self.active_vault.get_element(element_name)

            new_element_name = (
                input(
                    "Entrez le nouveau nom de l’élément ou laissez vide pour le conserver: "
                )
                or vault_item.name
            )
            new_element_login = (
                input(
                    "Entrez le nouveau login de l’élément ou laissez vide pour le conserver: "
                )
                or vault_item.login
            )
            new_element_password = (
                input(
                    "Entrez le nouveau mot de passe de l’élément ou laissez vide pour le conserver: "
                )
                or vault_item.password
            )

            nvi = VaultItem(new_element_name, new_element_login, new_element_password)
            self.active_vault.edit_element(vault_item, nvi)
        else:
            print("L’élément n’existe pas. Veuillez entrer un nom valide.")

    def remove_element(self):
        """
        Remove an element from the active vault.
        """
        element_name = input("Entrez le nom de l’élément: ")
        if self.active_vault.element_exists(element_name):
            vault_item = self.active_vault.get_element(element_name)
            self.active_vault.remove_element(vault_item)
        else:
            print("L’élément n’existe pas. Veuillez indiquer un nom valide.")

    def search_by_name(self):
        """
        Search for an element in the active vault by its name.
        """
        query = input("Entrez le début du nom de l’élément: ")
        for element in self.active_vault.search_by_name(query):
            print(f"{element.name}")

    def vault_menu(self):
        """
        Display the menu of the active vault and handle user’s choices.
        """
        while choice := -1 != 0:
            print("Votre coffre-fort".center(100, "#"))
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
                    print("Choix invalide. Veuillez réessayer.")

    def user_check(self, login: str) -> bool:
        """
        TODO

        Arguments:
            login -- _description_

        Returns:
            _description_
        """
        for user in self.users:
            if user.login == login:
                return True
        return False

    def do_login(self):
        """
        Prompts the user for a username and checks if it exists in the vault.
        If the username is found, sets the active vault to that user and displays the vault menu.
        If the username is not found, prompts the user to register.
        """
        user_name = input("Entrez un nom d’utilisateur: ")
        if self.user_check(user_name):
            user_password = input("Entrez votre mot de passe: ")
            for user, u_vault in self.users.items():
                if user.verify_password(user_password):
                    self.active_vault = u_vault
                    break
            self.vault_menu()
        else:
            print("L’utilisateur n’existe pas. Veuillez vous enregistrer.")

    def create_user(self):
        """
        Prompts the user for a username and creates a new user in the vault if it does not already exist.
        If the username already exists, prompts the user to log in or choose a different username.
        """
        user_name = input("Entrez un nom d’utilisateur: ")
        if not self.user_check(user_name):
            user_password = input("Entrez votre mot de passe: ")
            confirm_password = input("Confirmez votre mot de passe: ")
            if user_password == confirm_password:
                user = User(user_name, user_password)
                self.users[user] = Vault()
            else:
                print("Les mots de passe ne correspondent pas. Veuillez réessayer.")
        else:
            print(
                "L’utilisateur existe déjà. Veuillez vous reconnecter ou choisir un autre nom d’utilisateur."
            )

    def remove_user(self):
        """
        Prompts the user for a username and removes that user from the vault if it exists.
        If the username does not exist, prints a message stating that it does not exist.
        """
        user_name = input("Entrez un nom d’utilisateur: ")
        user_pass = input("Entrez votre mot de passe: ")
        for user, _ in self.users.items():
            if self.user_check(user_name) and user.verify_password(user_pass):
                del self.users[user]
                return
            else:
                print("Nom d’utilisateur inexistant.")

    def show_main_menu(self):
        """
        Displays the main menu and prompts the user to make a selection.
        If the user selects 0, exits the program.
        If the user selects 1, calls the do_login() function.
        If the user selects 2, calls the create_user() function.
        If the user selects 3, calls the remove_user() function.
        If the user selects any other number, prints a message stating that the choice is invalid and prompts the user to try again.ODO
        """
        while choice := -1 != 0:
            print("PASSMAN - PASSword MANager".center(100, "#"))
            print(
                """
                \r1. Connexion.
                \r2. Nouvel utilisateur.
                \r3. Supprimer un utilisateur.
                
                \r0. Quitter.
                """
            )
            choice = self.ask("Votre choix: ")
            match choice:
                case 0:
                    self.save()
                    exit()
                case 1:
                    self.do_login()
                case 2:
                    self.create_user()
                case 3:
                    self.remove_user()
                case _:
                    print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    app = MainApp()
    app.show_main_menu()
