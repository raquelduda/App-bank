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
        pass

    def build_accounts_panel(self) -> None:
        pass

    def selected_holder() -> Optional[object]:
        pass

    def selected_account() -> Optional[object]:
        pass

    def save(self, message: str) -> None:
        if self.database and self.bank:
            self.database.save(self.bank)

    def create_holder(self) -> None:
        pass

    def create_account(self) -> None:
        pass

    def delete_account(self) -> None:
        pass

    def transaction(self, operation: Callable[[object, float], None]) -> None:
        pass

    def search_changed() -> None:
        pass

    def refresh_holders(self) -> None:
        pass

    def refresh_accounts(self, keep: Optional[int] = None) -> None:
        pass