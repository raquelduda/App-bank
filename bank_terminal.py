from database import Database
from holder import Holder
from exceptions import BankError


class BankTerminal:
    def __init__(self):
        self.database = Database()
        self.bank = self.database.load()

    def run(self):
        while True:
            print("\n1 - Cadastrar titular")
            print("2 - Buscar titular")
            print("0 - Sair")
            opcao = input("Opção: ")

            if opcao == "1":
                self.create_holder_screen()
            elif opcao == "2":
                self.search_holder_screen()
            elif opcao == "0":
                break

    def save(self):
        self.database.save(self.bank)

    def create_holder_screen(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        try:
            self.bank.create_holder(nome, cpf)
            self.save()
            print("Titular cadastrado.")
        except BankError as erro:
            print("Erro:", erro)

    def search_holder_screen(self):
        nome = input("Parte do nome (Enter lista todos): ")
        holder = self.choose(list(self.bank.filter_by_name(nome)))
        if holder is not None:
            self.holder_menu(holder)

    def holder_menu(self, holder):
        while True:
            print(f"\nTitular: {holder.name}")
            print("1 - Listar contas")
            print("2 - Criar conta")
            print("3 - Excluir conta")
            print("0 - Voltar")
            opcao = input("Opção: ")

            if opcao == "1":
                self.list_accounts_screen(holder)
            elif opcao == "2":
                conta = self.bank.create_account(holder)
                self.save()
                print(f"Conta {conta} criada.")
            elif opcao == "3":
                self.delete_account_screen(holder)
            elif opcao == "0":
                break

    def list_accounts_screen(self, holder):
        conta = self.choose(list(holder.accounts()))
        if conta is not None:
            self.account_menu(conta)

    def delete_account_screen(self, holder):
        try:
            numero = int(input("Número da conta: "))
            holder.delete_account(numero)
            self.save()
            print("Conta excluída.")
        except ValueError:
            print("Erro: digite um valor numérico.")
        except BankError as erro:
            print("Erro:", erro)

    def account_menu(self, account):
        while True:
            print(f"\nConta {account} - Saldo: R$ {account.balance:.2f}")
            print("1 - Depositar")
            print("2 - Sacar")
            print("0 - Voltar")
            opcao = input("Opção: ")

            if opcao == "1":
                self.transaction_screen(account.deposit, "depósito")
            elif opcao == "2":
                self.transaction_screen(account.withdraw, "saque")
            elif opcao == "0":
                break

    def transaction_screen(self, operation, label):
        try:
            valor = float(input(f"Valor do {label}: ").replace(",", "."))
            operation(valor)
            self.save()
            print(f"{label.capitalize()} realizado.")
        except ValueError:
            print("Erro: digite um valor numérico.")
        except BankError as erro:
            print("Erro:", erro)

    def choose[T](self, items: list[T]) -> T | None:
        for i, item in enumerate(items, start=1):
            if isinstance(item, Holder):
                print(f"{i} - {item.name} ({item.cpf})")
            else:
                print(f"{i} - Conta {item} - Saldo: R$ {item.balance:.2f}")

        escolha = input("Escolha (Enter volta): ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(items):
            return items[int(escolha) - 1]
        return None


if __name__ == "__main__":
    BankTerminal().run()