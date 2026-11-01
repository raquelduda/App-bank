from holder import Holder
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