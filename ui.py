import flet as ft
import re
BLUE, RED, BG, CARD_BG = "#00a8ff", "#ff003c", "#0a0a0a", "#151515"
class AsgardUI:
    def __init__(self, page, system):
        self.page, self.system = page, system
        self.page_num, self.media_type, self.country, self.loading = 1, "MANGA", "KR", False
        self.grid = None
    def clean_html(self, raw):
        if not raw: return "No description."
        return re.sub(re.compile('<.*?>'), '', raw).replace("&quot;", '"').replace("&#039;", "'")
    def show_login(self):
        self.page.views.clear()
        u = ft.TextField(label="EMAIL", width=300, bgcolor="#111", border_color=BLUE)
        p = ft.TextField(label="PASS", password=True, width=300, bgcolor="#111", border_color=BLUE, can_reveal_password=True)
        st = ft.Text("", color=RED)
        def log(e):
            st.value = "CONNECTING..."
            self.page.update()
            if self.system.login(u.value, p.value) == "SUCCESS": self.show_home()
            else: st.value = "DENIED"; self.page.update()
        self.page.views.append(ft.View("/login", [ft.Container(content=ft.Column([ft.Text("ASGARD SYSTEM", size=30, color="white"), u, p, st, ft.ElevatedButton("ENTER", width=300, bgcolor=BLUE, color="white", on_click=log)], alignment="center", horizontal_alignment="center"), alignment=ft.alignment.center, expand=True, bgcolor=BG)], padding=0))
        self.page.update()
    def show_home(self):
        if not self.grid:
            self.grid = ft.GridView(expand=True, runs_count=2, child_aspect_ratio=0.7, spacing=10, padding=10)
            self.grid.on_scroll = self.on_s
        tabs = ft.Tabs(selected_index=0, indicator_color=BLUE, label_color=BLUE, on_change=self.ch_tab, tabs=[ft.Tab(text="MANHWA"), ft.Tab(text="MANGA"), ft.Tab(text="ANIME")])
        self.page.views.append(ft.View("/home", [ft.Container(padding=15, bgcolor="#111", content=ft.Text("DATABASE", color=BLUE)), tabs, ft.Container(content=self.grid, expand=True, bgcolor=BG)], padding=0, bgcolor=BG))
        self.page.update()
        if not self.grid.controls: self.load()
    def ch_tab(self, e):
        i = e.control.selected_index
        self.media_type = ["MANGA", "MANGA", "ANIME"][i]
        self.country = ["KR", "JP", None][i]
        self.page_num = 1; self.grid.controls.clear(); self.loading = False; self.page.update(); self.load()
    def on_s(self, e):
        if e.pixels >= e.max_scroll_extent - 200: self.load()
    def load(self):
        if self.loading: return
        self.loading = True
        try:
            items = self.system.fetch_media(self.page_num, self.media_type, self.country)
            for i in items:
                try:
                    t = i['title']['english'] or i['title']['romaji'] or "N/A"
                    im = i['coverImage']['extraLarge']
                    self.grid.controls.append(ft.Container(bgcolor=CARD_BG, border_radius=8, on_click=lambda e, x=i: self.show_d(x), content=ft.Column([ft.Image(src=im, fit="cover", height=180, expand=True), ft.Container(padding=5, content=ft.Text(t, size=11, no_wrap=True, color="white"))], spacing=0)))
                except: pass
            if items: self.page_num += 1
        except: pass
        self.loading = False; self.page.update()
    def show_d(self, i):
        t = i['title']['english'] or i['title']['romaji']
        d = self.clean_html(i.get('description', ""))
        im = i['coverImage']['extraLarge']
        self.page.views.append(ft.View("/d", [ft.AppBar(title=ft.Text("DATA"), bgcolor="#111"), ft.ListView([ft.Image(src=im, height=300, fit="cover"), ft.Container(padding=20, content=ft.Column([ft.Text(t, size=20, weight="bold"), ft.Divider(), ft.Text(d, color="#ccc")]))], expand=True)], bgcolor=BG))
        self.page.update()
