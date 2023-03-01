"""
    Terminal User Interface
"""
import colorama
from colorama import Fore, Style


class Tui:
    """
    Terminal User Interface
    """

    def __init__(self) -> None:
        """
        Constructor. Initializes colorama
        """
        colorama.init(autoreset=True)

    @staticmethod
    def print_message(message: str) -> None:
        """
        Print a message to screen

        Arguments:
            message -- Message to print
        """
        print(message)

    @staticmethod
    def print_error(message: str) -> None:
        """
        Print error message to screen

        Arguments:
            message -- message to print. Appears in RED
        """
        print(Fore.RED + message)  # type: ignore

    def show_main_menu(self) -> int:
        """
        Show main menu

        Returns:
            A number between 0 and 3
        """
        print(Style.BRIGHT + "PASSMAN - PASSword MANager".center(100, "#"))  # type: ignore

        print(
            """
                \r1. Connexion.
                \r2. Nouvel utilisateur.
                \r3. Supprimer un utilisateur.
                
                \r0. Quitter.
                """
        )

        choice = ""
        while not choice.isdigit() and choice not in ["0", "1", "2", "3"]:
            choice = self.ask("Votre choix: ")
        return int(choice)

    def show_vault_menu(self) -> int:
        """
        Show vault menu

        Returns:
            A number between 0 and 6
        """
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
        choice = ""
        while not choice.isdigit() and choice not in [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        ]:
            choice = self.ask("Votre choix: ")
        return int(choice)

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
