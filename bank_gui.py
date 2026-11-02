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

    def build_accounts_panel(self) -> None:
        self.accounts_frame = ttk.LabelFrame(self, text='Contas')
        self.accounts_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        ttk.Label(self.accounts_frame, text="Contas do titular selecionado:").pack(anchor="w", padx=10, pady=(10,5))
    def selected_holder(self) -> Optional[Holder]:
        pass

    def selected_account(self) -> Optional[Account]:
        pass

    def save(self, message: str) -> None:
        if self.database and self.bank:
            self.database.save(self.bank)

        self.status.set(message)

    def create_holder(self) -> None:
        pass

    def create_account(self) -> None:
        pass

    def delete_account(self) -> None:
        pass

    def transaction(self, operation: Callable[[object, float], None]) -> None:
        pass

    def search_changed(self) -> None:
        pass

    def refresh_holders(self) -> None:
        pass

    def refresh_accounts(self, keep: Optional[int] = None) -> None:
        pass


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()