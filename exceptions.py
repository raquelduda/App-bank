# BEATRIZ
class BankError(Exception):
    pass


class InvalidDataError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


class DuplicateHolderError(BankError):
    pass


class DuplicateAccountError(BankError):
    pass


class HolderNotFoundError(BankError):
    pass


class AccountNotFoundError(BankError):
    pass