from flet import Page, FletApp, ThemeMode, app, colors

def main(page: Page):

    page.padding = page.window_left = 0
    page.window_width = 700
        
    page.theme_mode = ThemeMode.LIGHT
    page.bgcolor = colors.BLUE_50

    page.add(
        FletApp(
            "http://192.168.173.1:81",
            expand=True
        )
    )
        
app(main)
