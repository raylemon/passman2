"""
Testing classes    
"""
from hashlib import sha512
import pytest
from model.data import User, Vault, VaultItem


class TestUser:
    """
    User test class
    """

    @pytest.fixture
    def password(self) -> str:
        """
        fixture - Generate controlled password

        Yields:
            "test" encoded with sha512
        """
        password = sha512("test".encode("utf-8")).hexdigest()
        return password

    @pytest.fixture
    def user(self) -> User:
        user = User("test", "test")
        return user

    def test_constructor(self, user, password):
        assert user.login == "test" and user.password == password

    def test_verify_password_is_true(self, user):
        assert user.verify_password("test") is True

    def test_verify_password_is_false(self, user):
        assert user.verify_password("1234") is False

    def test_str(self, user, password):
        assert str(user) == f"User login = test, user password = {password}"

    def test_hash(self, user):
        assert hash(user) == hash("test")


class TestVaultItem:
    def test_constructor(self):
        vault_item = VaultItem("test", "test", "test")
        assert (
            vault_item.login == "test"
            and vault_item.name == "test"
            and vault_item.password == "test"
        )


class TestVault:
    @pytest.fixture
    def items(self) -> list[VaultItem]:
        vi1 = VaultItem("item3", "it3", "1234")
        vi2 = VaultItem("item2", "it2", "1234")
        vi3 = VaultItem("item1", "it1", "1234")

        return [vi1, vi2, vi3]

    @pytest.fixture
    def one_item(self, items) -> VaultItem:
        vi1 = items[0]
        return vi1

    @pytest.fixture
    def item4(self) -> VaultItem:
        vi4 = VaultItem("item4", "it4", "1234")
        return vi4

    @pytest.fixture
    def empty_vault(self) -> Vault:
        vault = Vault()
        return vault

    @pytest.fixture
    def filled_vault(self, empty_vault, items) -> Vault:
        for i in items:
            empty_vault.elements[i.name] = i
        return empty_vault

    def test_constructor_len(self, filled_vault):
        assert len(filled_vault.elements) == 3

    def test_constructor_items(self, filled_vault, items):
        vi1, vi2, vi3 = items
        assert filled_vault.elements["item3"] == vi1
        assert filled_vault.elements["item2"] == vi2
        assert filled_vault.elements["item1"] == vi3

    def test_list_elements(self, filled_vault):
        assert filled_vault.list_elements() == ["item1", "item2", "item3"]

    def test_list_elements_empty(self, empty_vault):
        assert empty_vault.list_elements() == []

    def test_get_element(self, filled_vault, one_item):
        assert filled_vault.get_element("item3") == one_item

    def test_get_wrong_element(self, filled_vault):
        assert filled_vault.get_element("item4") == None
        # TODO raise Error later

    def test_add_element(self, empty_vault, item4):
        empty_vault.add_element(item4)
        assert len(empty_vault.elements) == 1 and empty_vault.elements["item4"] == item4

    def test_add_element_2(self, filled_vault, item4):
        filled_vault.add_element(item4)
        assert (
            len(filled_vault.elements) == 4 and filled_vault.elements["item4"] == item4
        )

    def test_add_duplicate_element(self, filled_vault, one_item):
        filled_vault.add_element(one_item)
        assert len(filled_vault.elements) == 3

    def test_edit_element(self, filled_vault, one_item, item4):
        filled_vault.edit_element(one_item, item4)
        assert (
            filled_vault.elements[item4.name] == item4
            and one_item.name not in filled_vault.elements
        )

    def test_remove_element(self, filled_vault, one_item):
        filled_vault.remove_element(one_item)
        assert (
            one_item.name not in filled_vault.elements
            and one_item not in filled_vault.elements
        )

    def test_remove_wrong_element(self, filled_vault, item4):
        filled_vault.remove_element(item4)
        assert len(filled_vault.elements) == 3
        # TODO raise error later

    def test_search_by_name(self, filled_vault, items):
        lst = filled_vault.search_by_name("ite")
        assert lst == sorted(items, key=lambda it: it.name)

    def test_search_by_name_2(self, filled_vault, one_item):
        lst = filled_vault.search_by_name("item3")
        assert lst == [one_item]

    def test_search_not_found(self, filled_vault):
        assert filled_vault.search_by_name("test") == []

    def test_element_exists(self, filled_vault):
        assert filled_vault.element_exists("item3") is True

    def test_element_not_exists(self, filled_vault):
        assert filled_vault.element_exists("test") is False
