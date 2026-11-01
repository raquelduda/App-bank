# 1. exceptions.py
# Primeiro, só as classes de exceção:
# 1. BankError
# 2. InvalidDataError
# 3. InvalidAmountError
# 4. InsufficientFundsError
# 5. DuplicateHolderError
# 6. DuplicateAccountError
# 7. HolderNotFoundError
# 8. AccountNotFoundError


# KAREN
# 2. account.py
# Classe Account:
# 1. __init__(number, balance=0.0)
# 2. number — property
# 3. balance — property
# 4. deposit(amount)
# 5. withdraw(amount)
# 6. __str__()
from exceptions import InvalidDataError, InvalidAmountError, InsufficientFundsError

class Account:
    def __init__(self, number: int, balance: float = 0.0):
        if number <= 0:
            raise InvalidDataError("O número da conta deve ser positivo.")

        if balance < 0:
            raise InvalidDataError("O saldo inicial não pode ser negativo.")

        self.__number = number
        self.__balance = balance

    @property
    def number(self) -> int:
        return self.__number

    @property
    def balance(self) -> float:
        return self.__balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError("O valor do depósito deve ser positivo.")

        self.__balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise InvalidAmountError("O valor do saque deve ser positivo.")

        if amount > self.__balance:
            raise InsufficientFundsError("Saldo insuficiente para realizar o saque.")

        self.__balance -= amount

    def __str__(self) -> str:
        return f"{self.__number:04d}"



# FERNANDA
#  3. holder.py
# Classe Holder:
# 1. __init__(name, cpf)
# 2. name — property + setter
# 3. cpf — property + setter
# 4. add_account(account)
# 5. delete_account(account_number)
# 6. get_account(account_number)
# 7. accounts()
from account import Account
from exceptions import InvalidDataError, DuplicateAccountError, AccountNotFoundError

class Holder:
    def __init__(self, name: str, cpf: str):
        self._accounts = {} 
        self.name = name     
        self.cpf = cpf       

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise InvalidDataError("O nome do titular não pode ser vazio.")
        self._name = value.strip()

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        if not value or not value.strip():
            raise InvalidDataError("O CPF do titular não pode ser vazio.")
        self._cpf = value.strip()

    def add_account(self, account: Account):
        if account.number in self._accounts:
            raise DuplicateAccountError(f"O titular já possui uma conta com o número {account.number}.")
        self._accounts[account.number] = account

    def delete_account(self, account_number: int):
        if account_number not in self._accounts:
            raise AccountNotFoundError(f"Conta número {account_number} não encontrada para este titular.")
        del self._accounts[account_number]

    def get_account(self, account_number: int) -> Account:
        if account_number not in self._accounts:
            raise AccountNotFoundError(f"Conta número {account_number} não encontrada para este titular.")
        return self._accounts[account_number]

    def accounts(self):
        yield from self._accounts.values()



# FERNANDA
# 4. bank.py
# Classe Bank:
# 1. __init__()
# 2. create_holder(name, cpf)
# 3. create_account(holder)
# 4. add_account(holder, account)
# 5. holders()
# 6. filter_by_name(name)
# 7. __next_account_number()
from account import Account
from exceptions import DuplicateHolderError, HolderNotFoundError, DuplicateAccountError

class Bank:
    def __init__(self):
        self._holders = []

    def create_holder(self, name: str, cpf: str) -> Holder:
        for holder in self._holders:
            if holder.cpf == cpf:
                raise DuplicateHolderError(f"Já existe um titular cadastrado com o CPF {cpf}.")
        
        holder = Holder(name, cpf)
        self._holders.append(holder)
        return holder

    def _next_account_number(self) -> int:
        max_num = 0
        for holder in self.holders():
            for account in holder.accounts():
                if account.number > max_num:
                    max_num = account.number
        return max_num + 1

    def create_account(self, holder: Holder) -> Account:
        number = self._next_account_number()
        account = Account(number, balance=0.0)
        self.add_account(holder, account)
        return account

    def add_account(self, holder: Holder, account: Account):
        if holder not in self._holders:
            raise HolderNotFoundError("O titular informado não pertence a este banco.")
        
        for h in self._holders:
            for acc in h.accounts():
                if acc.number == account.number:
                    raise DuplicateAccountError(f"A conta de número {account.number} já existe no banco.")
        
        holder.add_account(account)

    def holders(self):
        yield from self._holders

    def filter_by_name(self, name: str):
        search_term = name.strip().lower()
        for holder in self._holders:
            if not search_term or search_term in holder.name.lower():
                yield holder




# KAREN
# 5. database.py
# Classe Database:
# 1. __init__(path=DEFAULT_PATH)
# 2. path — property
# 3. load()
# 4. save(bank)




# RAFA
# 6. bank_terminal.py
# Classe BankTerminal:
# 1. __init__()
# 2. run()
# 3. save()
# 4. create_holder_screen()
# 5. search_holder_screen()
# 6. holder_menu(holder)
# 7. list_accounts_screen(holder)
# 8. create_account()
# 9. delete_account_screen(holder)
# 10. account_menu(account)
# 11. transaction(operation)
# 12. transaction_screen(operation, label)
# 13. choose(items)
from pathlib import Path
from typing import Callable, TypeVar, Optional, List, Generator
import tkinter as tk
from tkinter import ttk, messagebox

T = TypeVar('T')

class BankTerminal:
    def __init__(self, database=None, bank=None):
        self.database = database
        self.bank = bank

    def run(self) -> None:
        pass

    def save(self) -> None:
        if self.database and self.bank:
            self.database.save(self.bank)

    def create_holder_screen(self) -> None:
        pass

    def search_holder_screen(self) -> None:
        pass

    def holder_menu(self, holder) -> None:
        pass

    def list_accounts_screen(self, holder) -> None:
        pass

    def delete_account_screen(self, holder) -> None:
        pass

    def account_menu(self, account) -> None:
        pass

    def transaction_screen(self, operation: Callable[[float], None], label: str) -> None:
        pass

    def choose(self, items: List[T]) -> Optional[T]:
    
        pass

# RAFA
# 7. bank_gui.py
# Classe BankApp:
# 1. __init__()
# 2. build_holders_panel()
# 3. build_accounts_panel()
# 4. selected_holder()
# 5. selected_account()
# 6. create_holder()
# 7. create_account()
# 8. delete_account()
# 9. transaction(operation)
# 10. transaction_screen(operation, label)
# 11. search_changed()
# 12. refresh_holders()
# 13. refresh_accounts(keep=None)
# 14. save(message)
class BankApp(tk.Tk):
    def __init__(self, database=None, bank=None):
        super().__init__()
        self.database = database
        self.bank = bank
        self.holders: List = []

        self.title("Bank Application")
        self.geometry("800x600")

        self.build_holders_panel()
        self.build_accounts_panel()

    def build_holders_panel(self) -> None:
        pass

    def build_accounts_panel(self) -> None:
        pass

    def selected_holder() -> Optional[object]:
        pass

    def selected_account() -> Optional[object]:
        pass

    def save(self, message: str) -> None:
        if self.database and self.bank:
            self.database.save(self.bank)

    def create_holder(self) -> None:
        pass

    def create_account(self) -> None:
        pass

    def delete_account(self) -> None:
        pass

    def transaction(self, operation: Callable[[object, float], None]) -> None:
        pass

    def search_changed() -> None:
        pass

    def refresh_holders(self) -> None:
        pass

    def refresh_accounts(self, keep: Optional[int] = None) -> None:
        pass





