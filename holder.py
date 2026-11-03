from account import Account
from exceptions import InvalidDataError, DuplicateAccountError, AccountNotFoundError

class Holder:
    def __init__(self, name: str, cpf: str):
        self.__accounts = {} 
        self.name = name     
        self.cpf = cpf       

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise InvalidDataError("O nome do titular não pode ser vazio.")
        self.__name = value.strip()

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, value: str):
        if not value or not value.strip():
            raise InvalidDataError("O CPF do titular não pode ser vazio.")
        self.__cpf = value.strip()

    def add_account(self, account: Account):
        if account.number in self.__accounts:
            raise DuplicateAccountError(f"O titular já possui uma conta com o número {account.number}.")
        self.__accounts[account.number] = account

    def delete_account(self, account_number: int):
        if account_number not in self.__accounts:
            raise AccountNotFoundError(f"Conta número {account_number} não encontrada para este titular.")
        del self.__accounts[account_number]

    def get_account(self, account_number: int) -> Account:
        if account_number not in self.__accounts:
            raise AccountNotFoundError(f"Conta número {account_number} não encontrada para este titular.")
        return self.__accounts[account_number]

    def accounts(self):
        yield from self.__accounts.values()