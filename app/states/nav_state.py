import reflex as rx


class NavState(rx.State):
    """State for managing navigation and mobile menu."""

    is_menu_open: bool = False

    @rx.event
    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def close_menu(self):
        self.is_menu_open = False

    @rx.var
    def current_path(self) -> str:
        return self.router.page.path