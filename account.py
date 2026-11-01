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