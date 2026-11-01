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
