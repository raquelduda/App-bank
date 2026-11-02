import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, List

from holder import Holder
from account import Account
from exceptions import BankError

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
        self.holders_frame = ttk.LabelFrame(self, text="Titulares")
        self.holders_frame.pack(side = "left", fill="both", expand="True", padx=10, pady=10)

        ttk.Label(self.holders_frame,text="Pesquisar:").pack(anchor="w",padx=10, pady=(10,2))

        self.search_entry = ttk.Entry(self.holders_frame)
        self.search_entry.pack(fill="x",padx=10)
        self.search_entry.bind("<KeyRelease>",lambda event: self.search_changed())
        self.holders_list = tk.Listbox(self.holders_frame)
        self.holders_list.pack(fill="both",expand=True,padx=10,pady=10)
        self.holders_list.bind("<<ListboxSelect>>", lambda event: self.refresh_accounts())
        ttk.Label(self.holders_frame, text="Nome:").pack(anchor="w", padx=10)
        self.name_entry = ttk.Entry(self.holders_frame)
        self.name_entry.pack(fill="x", padx=10, pady=(0,5))
        ttk.Label(self.holders_frame, text="CPF:").pack(anchor="w", padx=10)
        self.cpf_entry = ttk.Entry(self.holders_frame)
        self.cpf_entry.pack(fill="x", padx=10, pady=(0,5))
        ttk.Button(self.holders_frame,text="Cadastrar titular",command=self.create_holder).pack(padx=10,pady=10)


    def build_accounts_panel(self) -> None:
        self.accounts_frame = ttk.LabelFrame(self, text='Contas')
        self.accounts_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ttk.Label(self.accounts_frame, text="Contas do titular selecionado:").pack(anchor="w", padx=10, pady=(10,5))
        self.accounts_list = tk.Listbox(self.accounts_frame)
        self.accounts_list.pack(fill="both",expand=True,padx=10,pady=10)
        ttk.Button(self.accounts_frame, text="Nova conta", command=self.create_account).pack(padx=10, pady=5)
        ttk.Button(self.accounts_frame, text="Excluir conta", command=self.delete_account).pack(padx=10, pady=5)
        ttk.Label(self.accounts_frame,text="Valor").pack(anchor="w", padx=10, pady=(10,2))

        self.amount_entry = ttk.Entry(self.accounts_frame)
        self.amount_entry.pack(fill="x", padx=10)

        ttk.Button(self.accounts_frame, text="Depositar", command=lambda: self.transaction(lambda account, amount: account.deposit(amount))).pack(padx=10, pady=5)
        ttk.Button(self.accounts_frame, text="Sacar", command=lambda: self.transaction(lambda account, amount: account.withdraw(amount))).pack(padx=10, pady=5)
    def selected_holder(self) -> Optional[Holder]:
        selection = self.holders_list.curselection()

        if not selection:
            return None

        index = selection [0]
        return self.holders[index]
    

    def selected_account(self) -> Optional[Account]:
        pass


    def save(self, message: str) -> None:
        if self.database and self.bank:
            self.database.save(self.bank)

        self.status.set(message)


    def create_holder(self) -> None:
        name = self.name_entry.get()
        cpf = self.cpf_entry.get()
        try:
            holder = self.bank.create_holder(name,cpf)
            print('Titular cadastrado:', holder.name)
            self.name_entry.delete(0, tk.END)
            self.cpf_entry.delete(0, tk.END)

            self.refresh_holders()

        except BankError as error:
            messagebox.showerror("Erro", str(error))


    def create_account(self) -> None:
        holder = self.selected_holder()

        if holder is None:
            messagebox.showerror("Erro", "Selecione um titular primeiro")
            return
        try:
            account = self.bank.crea_account(holder)

            self.refresh_accounts()
            messagebox.showinfo("Sucesso", f"Conta {account.number:04d} criada com sucesso")
        except BankError as error:
            messagebox.showerror("Erro", str(error))
    def delete_account(self) -> None:
        holder = self.selected_holder()
        if holder is None:
            messagebox.showerror("Erro", "Selecione um titular primeiro")
            return
        selection = self.accounts_list.curselection()
        if not selection:
            messagebox.showerror("Erro", "Selecione uma conta")
            return
        index = selection[0]
        accounts = list(holder.accounts())
        account = accounts[index]

        confirm = messagebox.askyesno("Confirmar", f"Deseja excluir a conta {account.number:04d}?")
        if not confirm:
            return
        try:
            holder.delete_account(account.number)
            self.refresh_accounts()
            messagebox.showinfo("Sucesso", "Conta excluída com sucesso.")
        except BankError as error:
            messagebox.showerror("Erro", str(error))
    def transaction(self, operation: Callable[[object, float], None]) -> None:
        pass

    def search_changed(self) -> None:
        pass


    def refresh_holders(self) -> None:
        self.holders_list.delete(0, tk.END)

        self.holders = list(self.bank.holders())

        for holder in self.bank.holders():
            self.holders_list.insert(tk.END, holder.name)


    def refresh_accounts(self, keep: Optional[int] = None) -> None:
        self.accounts_list.delete(0, tk.END)

        holder = self.selected_holder()

        if holder is None:
            return

        for account in holder.accounts():
            self.accounts_list.insert(
                tk.END,
                f"Conta {account.number:04d} - R$ {account.balance:.2f}"
            )


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()