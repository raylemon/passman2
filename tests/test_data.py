"""
Testing classes    
"""
from hashlib import sha512
import pytest
from model.data import DuplicateError, User, UserStorage, Vault, VaultItem


class TestUser:
    """
    _summary_

    Returns:
        _description_
    """

    @pytest.fixture
    def password(self) -> str:
        """
        _summary_

        Returns:
            _description_
        """
        password = sha512("test".encode("utf-8")).hexdigest()
        return password

    @pytest.fixture
    def user(self) -> User:
        """
        _summary_

        Returns:
            _description_
        """
        user = User("test", "test")
        return user

    def test_constructor(self, user, password):
        """
        _summary_

        Arguments:
            user -- _description_
            password -- _description_
        """
        assert user.login == "test" and user.password == password

    def test_verify_password_is_true(self, user):
        """
        _summary_

        Arguments:
            user -- _description_
        """
        assert user.verify_password("test") is True

    def test_verify_password_is_false(self, user):
        """
        _summary_

        Arguments:
            user -- _description_
        """
        assert user.verify_password("1234") is False

    def test_str(self, user, password):
        """
        _summary_

        Arguments:
            user -- _description_
            password -- _description_
        """
        assert str(user) == f"User login = test, user password = {password}"

    def test_hash(self, user):
        """
        _summary_

        Arguments:
            user -- _description_
        """
        assert hash(user) == hash("test")


class TestVaultItem:
    """
    _summary_
    """

    def test_constructor(self):
        """
        _summary_
        """
        vault_item = VaultItem("test", "test", "test")
        assert (
            vault_item.login == "test"
            and vault_item.name == "test"
            and vault_item.password == "test"
        )


class TestVault:
    """
    _summary_

    Returns:
        _description_
    """

    @pytest.fixture
    def items(self) -> list[VaultItem]:
        """
        _summary_

        Returns:
            _description_
        """
        vi1 = VaultItem("item3", "it3", "1234")
        vi2 = VaultItem("item2", "it2", "1234")
        vi3 = VaultItem("item1", "it1", "1234")

        return [vi1, vi2, vi3]

    @pytest.fixture
    def one_item(self, items) -> VaultItem:
        """
        _summary_

        Arguments:
            items -- _description_

        Returns:
            _description_
        """
        vi1 = items[0]
        return vi1

    @pytest.fixture
    def item4(self) -> VaultItem:
        """
        _summary_

        Returns:
            _description_
        """
        vi4 = VaultItem("item4", "it4", "1234")
        return vi4

    @pytest.fixture
    def empty_vault(self) -> Vault:
        """
        _summary_

        Returns:
            _description_
        """
        vault = Vault()
        return vault

    @pytest.fixture
    def filled_vault(self, empty_vault, items) -> Vault:
        """
        _summary_

        Arguments:
            empty_vault -- _description_
            items -- _description_

        Returns:
            _description_
        """
        for i in items:
            empty_vault.elements[i.name] = i
        return empty_vault

    def test_constructor_len(self, filled_vault):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
        """
        assert len(filled_vault.elements) == 3

    def test_constructor_items(self, filled_vault, items):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            items -- _description_
        """
        vi1, vi2, vi3 = items
        assert filled_vault.elements["item3"] == vi1
        assert filled_vault.elements["item2"] == vi2
        assert filled_vault.elements["item1"] == vi3

    def test_list_elements(self, filled_vault):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
        """
        assert filled_vault.list_elements() == ["item1", "item2", "item3"]

    def test_list_elements_empty(self, empty_vault):
        """
        _summary_

        Arguments:
            empty_vault -- _description_
        """
        assert empty_vault.list_elements() == []

    def test_get_element(self, filled_vault, one_item):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            one_item -- _description_
        """
        assert filled_vault.get_element("item3") == one_item

    @pytest.mark.xfail(raises=KeyError)
    def test_get_wrong_element(self, filled_vault):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
        """
        filled_vault.get_element("item4")

    @pytest.mark.xfail(raises=DuplicateError)
    def test_add_element(self, empty_vault, item4):
        """
        _summary_

        Arguments:
            empty_vault -- _description_
            item4 -- _description_
        """
        empty_vault.add_element(item4)
        assert len(empty_vault.elements) == 1 and empty_vault.elements["item4"] == item4

    @pytest.mark.xfail(raises=DuplicateError)
    def test_add_element_2(self, filled_vault, item4):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            item4 -- _description_
        """
        filled_vault.add_element(item4)
        assert (
            len(filled_vault.elements) == 4 and filled_vault.elements["item4"] == item4
        )

    @pytest.mark.xfail(raises=DuplicateError)
    def test_add_duplicate_element(self, filled_vault, one_item):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            one_item -- _description_
        """
        filled_vault.add_element(one_item)
        assert len(filled_vault.elements) == 3

    @pytest.mark.xfail(raises=KeyError)
    def test_edit_element(self, filled_vault, one_item, item4):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            one_item -- _description_
            item4 -- _description_
        """
        filled_vault.edit_element(one_item, item4)
        assert (
            filled_vault.elements[item4.name] == item4
            and one_item.name not in filled_vault.elements
        )

    @pytest.mark.xfail(raises=KeyError)
    def test_remove_element(self, filled_vault, one_item):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            one_item -- _description_
        """
        filled_vault.remove_element(one_item)
        assert (
            one_item.name not in filled_vault.elements
            and one_item not in filled_vault.elements
        )

    @pytest.mark.xfail(raises=KeyError)
    def test_remove_wrong_element(self, filled_vault, item4):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            item4 -- _description_
        """
        filled_vault.remove_element(item4)
        assert len(filled_vault.elements) == 3

    def test_search_by_name(self, filled_vault, items):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            items -- _description_
        """
        lst = filled_vault.search_by_name("ite")
        assert lst == sorted(items, key=lambda it: it.name)

    def test_search_by_name_2(self, filled_vault, one_item):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
            one_item -- _description_
        """
        lst = filled_vault.search_by_name("item3")
        assert lst == [one_item]

    def test_search_not_found(self, filled_vault):
        """
        _summary_

        Arguments:
            filled_vault -- _description_
        """
        assert filled_vault.search_by_name("test") == []


class TestUserStorage:
    """
    _summary_
    """

    @pytest.fixture
    def storage(self) -> UserStorage:
        """
        _summary_

        Returns:
            _description_
        """
        storage = UserStorage()
        storage.users = {}
        return storage

    @pytest.fixture
    def user(self) -> User:
        """
        _summary_

        Returns:
            _description_
        """
        return User("test", "test")

    @pytest.fixture
    def items(self) -> list[VaultItem]:
        """
        _summary_

        Returns:
            _description_
        """
        vi1 = VaultItem("item1", "it1", "1234")
        vi2 = VaultItem("item2", "it2", "3456")
        return [vi1, vi2]

    @pytest.fixture
    def vault(self, items) -> Vault:
        """
        _summary_

        Arguments:
            items -- _description_

        Returns:
            _description_
        """

        vault = Vault()
        vault.elements[items[0].name] = items[0]
        vault.elements[items[1].name] = items[1]
        return vault

    @pytest.fixture
    def full_storage(self, storage, user, vault) -> UserStorage:
        """
        _summary_

        Arguments:
            storage -- _description_

        Returns:
            _description_
        """
        storage.users = {}
        storage.users[user] = vault
        return storage

    def test_load_empty(self, storage):
        """
        _summary_

        Arguments:
            storage -- _description_
        """
        storage.load("")
        assert storage.users == {}

    def test_load_non_empty(self, storage):
        """
        _summary_

        Arguments:
            storage -- _description_
        """
        pass

    def test_save(self, storage):
        """
        _summary_

        Arguments:
            storage -- _description_
        """
        pass

    def test_get_user(self, full_storage, user):
        """
        _summary_

        Arguments:
            storage -- _description_
        """
        assert full_storage.get_user("test") == user

    def test_get_wrong_user(self, full_storage):
        """
        _summary_

        Arguments:
            full_storage -- _description_
        """
        assert full_storage.get_user("toto") is None

    def test_remove_user_ok(self, full_storage, user):
        """
        _summary_

        Arguments:
            full_storage -- _description_
        """
        assert full_storage.remove_user("test", "test") is True
        assert user not in full_storage.users

    def test_remove_wrong_user(self, full_storage):
        """
        _summary_

        Arguments:
            full_storage -- _description_
        """
        assert full_storage.remove_user("toto", "toto") is False
        assert len(full_storage.users) == 1

    def test_create_user(self, storage):
        """
        _summary_

        Arguments:
            storage -- _description_
        """
        assert storage.create_user("test", "test") is True
        assert len(storage.users) == 1

    def test_create_duplicate_user(self, full_storage):
        """
        _summary_

        Arguments:
            full_storage -- _description_
            user -- _description_
        """
        assert full_storage.create_user("test", "test") is False

    @pytest.mark.xfail(raises=KeyError)
    def test_get_vault(self, full_storage, user, vault):
        """
        _summary_

        Arguments:
            full_storage -- _description_
            user -- _description_
            vault -- _description_
        """
        assert full_storage.get_vault(user) == vault

    @pytest.mark.xfail(raises=KeyError)
    def test_get_wrong_vault(self, storage, user):
        """
        _summary_

        Arguments:
            storage -- _description_
            user -- _description_
        """
        storage.get_vault(user)

    @pytest.mark.xfail(raises=KeyError)
    def test_get_wrong_vault_2(self, full_storage):
        """
        _summary_

        Arguments:
            full_storage -- _description_
        """
        full_storage.get_vault(User("toto", "toto"))
