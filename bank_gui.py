import tkinter
from tkinter import messagebox
from bank import Bank
from database import Database
from exceptions import BankError
class BankApp(tkinter.Tk):
    def __init__(self, database, bank):
        super().__init__()
        self.title("Banco")
        self.configure(padx=10, pady=10)

        self.database = database
        self.bank = bank
        self.holders = []   

        self.build_holders_panel()
        self.build_accounts_panel()

        self.lbl_status = tkinter.Label(self, text="Pronto.")
        self.lbl_status.grid(row=1, column=0, columnspan=2, sticky="we", pady=(10, 0))

        self.refresh_holders()

    def build_holders_panel(self):
        frame = tkinter.Frame(self)
        frame.grid(row=0, column=0, sticky="n", padx=(0, 20))

        self.lbl_titulo_titulares = tkinter.Label(frame, text="TITULARES")
        self.lbl_titulo_titulares.grid(row=0, column=0, pady=(0, 10))

        self.lbl_busca = tkinter.Label(frame, text="Buscar:")
        self.txt_busca = tkinter.Entry(frame, width=30)
        self.lbl_busca.grid(row=1, column=0, sticky="w")
        self.txt_busca.grid(row=2, column=0, sticky="w", pady=(0, 10))
        self.txt_busca.bind("<KeyRelease>", self.search_changed)

        self.lst_titulares = tkinter.Listbox(frame, width=40, height=10, exportselection=False)
        self.lst_titulares.grid(row=3, column=0)
        self.lst_titulares.bind("<<ListboxSelect>>", self.refresh_accounts)

        self.lbl_nome = tkinter.Label(frame, text="Nome:")
        self.txt_nome = tkinter.Entry(frame, width=30)
        self.lbl_cpf = tkinter.Label(frame, text="CPF:")
        self.txt_cpf = tkinter.Entry(frame, width=30)
        self.btn_cadastrar = tkinter.Button(frame, text="Cadastrar titular", width=20)

        self.lbl_nome.grid(row=4, column=0, sticky="w", pady=(10, 0))
        self.txt_nome.grid(row=5, column=0, sticky="w")
        self.lbl_cpf.grid(row=6, column=0, sticky="w")
        self.txt_cpf.grid(row=7, column=0, sticky="w")
        self.btn_cadastrar.grid(row=8, column=0, pady=(10, 0))
        self.btn_cadastrar.configure(command=self.create_holder)

    def build_accounts_panel(self):
        frame = tkinter.Frame(self)
        frame.grid(row=0, column=1, sticky="n")

        self.lbl_titulo_contas = tkinter.Label(frame, text="CONTAS")
        self.lbl_titulo_contas.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.lst_contas = tkinter.Listbox(frame, width=35, height=10, exportselection=False)
        self.lst_contas.grid(row=1, column=0, columnspan=2)

        self.btn_nova = tkinter.Button(frame, text="Nova conta", width=15)
        self.btn_excluir = tkinter.Button(frame, text="Excluir conta", width=15)
        self.btn_nova.grid(row=2, column=0, pady=10)
        self.btn_excluir.grid(row=2, column=1, pady=10)
        self.btn_nova.configure(command=self.create_account)
        self.btn_excluir.configure(command=self.delete_account)

        self.lbl_valor = tkinter.Label(frame, text="Valor:")
        self.txt_valor = tkinter.Entry(frame, width=20)
        self.btn_depositar = tkinter.Button(frame, text="Depositar", width=15)
        self.btn_sacar = tkinter.Button(frame, text="Sacar", width=15)

        self.lbl_valor.grid(row=3, column=0, sticky="w")
        self.txt_valor.grid(row=4, column=0, columnspan=2, sticky="w")
        self.btn_depositar.grid(row=5, column=0, pady=(10, 0))
        self.btn_sacar.grid(row=5, column=1, pady=(10, 0))
        self.btn_depositar.configure(command=self.deposit)
        self.btn_sacar.configure(command=self.withdraw)

    def selected_holder(self):
        selecao = self.lst_titulares.curselection()
        if not selecao:
            return None
        return self.holders[selecao[0]]

    def selected_account(self):
        holder = self.selected_holder()
        selecao = self.lst_contas.curselection()
        if holder is None or not selecao:
            return None
        contas = list(holder.accounts())
        return contas[selecao[0]]

    def save(self, message):
        self.database.save(self.bank)
        self.lbl_status.configure(text=message)

    def create_holder(self):
        try:
            holder = self.bank.create_holder(self.txt_nome.get(), self.txt_cpf.get())
        except BankError as erro:
            messagebox.showerror(title="Erro", message=str(erro))
            return

        self.txt_nome.delete(0, "end")
        self.txt_cpf.delete(0, "end")
        self.refresh_holders()
        self.save(f"Titular {holder.name} cadastrado.")

    def create_account(self):
        holder = self.selected_holder()
        if holder is None:
            messagebox.showwarning(title="Aviso", message="Selecione um titular.")
            return

        account = self.bank.create_account(holder)
        self.refresh_accounts()
        self.save(f"Conta {account} criada.")

    def delete_account(self):
        holder = self.selected_holder()
        account = self.selected_account()
        if account is None:
            messagebox.showwarning(title="Aviso", message="Selecione uma conta.")
            return

        if messagebox.askyesno(title="Confirmar", message=f"Excluir a conta {account}?"):
            holder.delete_account(account.number)
            self.refresh_accounts()
            self.save(f"Conta {account} excluída.")

    def deposit(self):
        self.transaction("deposito")

    def withdraw(self):
        self.transaction("saque")

    def transaction(self, operation):
        account = self.selected_account()
        if account is None:
            messagebox.showwarning(title="Aviso", message="Selecione uma conta.")
            return

        try:
            valor = float(self.txt_valor.get().replace(",", "."))
        except ValueError:
            messagebox.showerror(title="Erro", message="Digite um valor numérico.")
            return

        try:
            if operation == "deposito":
                account.deposit(valor)
            else:
                account.withdraw(valor)
        except BankError as erro:
            messagebox.showerror(title="Erro", message=str(erro))
            return

        self.txt_valor.delete(0, "end")
        self.refresh_accounts()
        self.save(f"Conta {account}: saldo R$ {account.balance:.2f}")

    def search_changed(self, event=None):
        self.refresh_holders()

    def refresh_holders(self):
        self.lst_titulares.delete(0, "end")
        self.holders = list(self.bank.filter_by_name(self.txt_busca.get()))
        for holder in self.holders:
            self.lst_titulares.insert("end", f"{holder.name} - {holder.cpf}")
        self.lst_contas.delete(0, "end")

    def refresh_accounts(self, event=None):
        self.lst_contas.delete(0, "end")
        holder = self.selected_holder()
        if holder is None:
            return
        for account in holder.accounts():
            self.lst_contas.insert("end", f"Conta {account} - R$ {account.balance:.2f}")


database = Database()
app = BankApp(database, database.load())
app.mainloop()