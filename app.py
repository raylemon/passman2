"""
TODO
"""


def ask(prompt: str) -> int:
    """
    TODO

    Args:
        prompt (str): _description_

    Returns:
        int: _description_
    """
    choice: str = ""
    while not choice.isdigit():
        choice = input(prompt)
    return int(choice)


def list_elements():
    """
    TODO
    """
    for element in active_vault:
        print(element)


def show_details():
    """
    TODO
    """
    element_name = input("Entrez le nom d’un élément: ")
    if element_name in active_vault:
        element_login, element_password = active_vault[element_name]
        print(f"login: {element_login}, password: {element_password}")
    else:
        print("Pas d’élément à ce nom. Veuillez réessayer.")


def add_element():
    """
    TODO
    """
    element_name = input("Entrez le nom de l’élément: ")
    if element_name not in active_vault:
        element_login = input("Entrez le login de l’élément")
        element_password = input("Entrez le password de l’élément")

        active_vault[element_name] = (element_login, element_password)
    else:
        print("L’élément existe déjà. Veuillez réessayer.")


def edit_element():
    """
    TODO
    """
    element_name = input("Entrez le nom de l’élément: ")
    if element_name in active_vault:
        element_login, element_password = active_vault[element_name]

        new_element_name = input(
            "Entrez le nouveau nom de l’élément ou laissez vide pour le conserver: "
        )
        new_element_login = input(
            "Entrez le nouveau login de l’élément ou laissez vide pour le conserver: "
        )
        new_element_password = input(
            "Entrez le nouveau mot de passe de l’élément ou laissez vide pour le conserver: "
        )

        del active_vault[element_name]
        active_vault[new_element_name] = (new_element_login, new_element_password)
    else:
        print("L’élément n’existe pas. Veuillez entrer un nom valide.")


def remove_element():
    """
    TODO
    """
    element_name = input("Entrez le nom de l’élément: ")
    if element_name in active_vault:
        del active_vault[element_name]
    else:
        print("L’élément n’existe pas. Veuillez indiquer un nom valide.")


def search_by_name():
    """
    TODO
    """
    query = input("Entrez le début du nom de l’élément: ")
    for element in active_vault:
        if element.startswith(query):
            print(element)


def vault_menu():
    """
    TODO
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

        choice = ask("Votre choix: ")

        match choice:
            case 0:
                return
            case 1:
                list_elements()
            case 2:
                show_details()
            case 3:
                add_element()
            case 4:
                edit_element()
            case 5:
                remove_element()
            case 6:
                search_by_name()
            case _:
                print("Choix invalide. Veuillez réessayer.")


def do_login():
    """
    TODO
    """
    user_name = input("Entrez un nom d’utilisateur: ")
    if user_name in vault:
        global active_vault
        active_vault = vault[user_name]
        vault_menu()
    else:
        print("L’utilisateur n’existe pas. Veuillez vous enregistrer.")


def create_user():
    """
    TODO
    """
    user_name = input("Entrez un nom d’utilisateur: ")
    if user_name not in vault:
        vault[user_name] = {}
    else:
        print(
            "L’utilisateur existe déjà. Veuillez vous reconnecter ou choisir un autre nom d’utilisateur."
        )


def remove_user():
    """
    TODO
    """
    user_name = input("Entrez un nom d’utilisateur: ")
    if user_name in vault:
        del vault[user_name]
    else:
        print("Nom d’utilisateur inexistant.")


def show_main_menu():
    """
    TODO
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
        choice = ask("Votre choix: ")
        match choice:
            case 0:
                exit()
            case 1:
                do_login()
            case 2:
                create_user()
            case 3:
                remove_user()
            case _:
                print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    vault: dict[str, dict] = {}
    active_vault: dict[str, tuple[str, str]] = {}

    show_main_menu()
