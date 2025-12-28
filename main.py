import flet as ft
import os
from database import AsgardSystem
from ui import AsgardUI

def main(page: ft.Page):
    page.title = "ASGARD SYSTEM"
    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    page.update()

    def route_change(route):
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    try:
        system = AsgardSystem()
        app = AsgardUI(page, system)
        page.go("/login")
        app.show_login()
    except Exception as e:
        page.add(ft.Text(f"Error: {e}", color="red"))
        page.update()

# هذا هو التغيير الجذري: تصدير التطبيق لمحرك Uvicorn
app = ft.app(target=main, view=ft.AppView.WEB_BROWSER, export_asgi_app=True)
