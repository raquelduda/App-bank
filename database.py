import json
from pathlib import Path

from bank import Bank
from account import Account


DEFAULT_PATH = Path(__file__).with_name("bank.json")


class Database:

    def __init__(self, path: Path = DEFAULT_PATH):
        self.__path = Path(path)

    @property
    def path(self) -> Path:
        return self.__path

    def load(self) -> Bank:
        bank = Bank()

        if not self.__path.exists():
            return bank

        with self.__path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        for holder_data in data:
            holder = bank.create_holder(
                holder_data["name"],
                holder_data["cpf"]
            )

            for account_data in holder_data["accounts"]:
                account = Account(
                    account_data["number"],
                    account_data["balance"]
                )

                bank.add_account(holder, account)

        return bank

    def save(self, bank: Bank):
        data = []

        for holder in bank.holders():
            holder_data = {
                "name": holder.name,
                "cpf": holder.cpf,
                "accounts": []
            }

            for account in holder.accounts():
                holder_data["accounts"].append({
                    "number": account.number,
                    "balance": account.balance
                })

            data.append(holder_data)

        with self.__path.open("w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )