import flet as ft
import os
from database import AsgardSystem
from ui import AsgardUI
def main(page: ft.Page):
    page.title = "ASGARD SYSTEM"
    page.bgcolor, page.theme_mode, page.padding = "black", ft.ThemeMode.DARK, 0
    def rc(r): page.update()
    def vp(v): page.views.pop(); top = page.views[-1]; page.go(top.route)
    page.on_route_change = rc; page.on_view_pop = vp
    try: s = AsgardSystem(); app = AsgardUI(page, s); page.go("/login"); app.show_login()
    except Exception as e: page.add(ft.Text(f"ERR: {e}", color="red"))
if __name__ == "__main__": ft.app(target=main, port=int(os.getenv("PORT", 8080)), host="0.0.0.0")
