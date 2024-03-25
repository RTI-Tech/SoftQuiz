from threading import Timer
from time import sleep
from flet import*

class Main:
    def __init__(self, page: Page):
        self.page = page

        page.adaptive = True
        page.window_always_on_top = True

        page.theme = Theme(
            color_scheme_seed=colors.BLUE,
        )

        page.theme_mode = ThemeMode.LIGHT
        #page.platform = PagePlatform.IOS

        page.window_left = 960
        page.window_width = 400
        page.window_height = 700
        page.padding = 0

        # Fonction pour procéder les Evénements du clavier
        page.on_keyboard_event = self.KeyBoard_Event_Handler

        
        # Conteneur Principal
        self.Main_container = Container(
            gradient=RadialGradient(colors=[colors.BLUE_100, colors.BLUE_200], radius=0.7, center=Alignment(0, -.1)),
            alignment=alignment.center,
            animate=1000,
            expand=True
        )

        #  --------------  Launch Page Animation  -------------------#

        self.anim_image = Image(
            src="SoftQuiz_logo.png",
            error_content=Icon(icons.ERROR, colors.RED, 60),
            scale=0,
            offset=Offset(0, -0.2),
            animate_scale=1000,
            on_animation_end=lambda e: self.animation(self.anim_text)
        )

        self.anim_text = Text(
            "Gérez vos évalutions en toute éfficacité",
            font_family="Times",
            theme_style=TextThemeStyle.TITLE_MEDIUM,
            offset=Offset(0, -2),
            opacity=0,
            animate_opacity=1000,
            animate_offset=1000,
            on_animation_end=lambda e: (self.animation(self.anim_progress), sleep(5), self.animation(self.Choose_Page))
        )

        self.anim_progress = ProgressRing(
            value=None,
            stroke_width=2,
            opacity=0,
            animate_opacity=500
        )

        self.Animation_Page = Column(
            [self.anim_image, self.anim_text, self.anim_progress],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

        # Le permutateur des pages
        self.Switcher = AnimatedSwitcher(
            self.Animation_Page,
            transition=AnimatedSwitcherTransition.FADE,
            switch_in_curve=AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN,
            duration=2000
        )

        # Ajout du permutateur
        self.Main_container.content = self.Switcher

        
        # Retarde l'animation de 500 millisecondes
        Timer(.5, self.animation, (self.anim_image,)).start()

        # Ajout du conteneur principal
        page.add(self.Main_container)


        # ----------------    Choose Page   ---------------------

        self.Choose_Page = Column(
            [
                Image(
                    src="SoftQuiz_logo.png",
                    error_content=Icon(icons.QUESTION_MARK_ROUNDED, colors.RED, 60),
                    scale=0.8,
                ),
                
                Container(
                    Column(
                        [
                            Text(
                                "Continuez en tant que",
                                font_family="Times New Romans",
                                theme_style=TextThemeStyle.TITLE_MEDIUM
                            ),

                            Divider(
                                height=1,
                                color=colors.TRANSPARENT
                            ),

                            FilledTonalButton(
                                "   Etudiant",
                                icons.SCHOOL_ROUNDED,
                                width=240,
                                height=55,
                                on_click=lambda e: self.animation(self.Login_Page, "Etudiant")
                            ),
                            
                            FilledTonalButton(
                                " Professeur",
                                icons.SUPERVISOR_ACCOUNT,
                                width=240,
                                height=55,
                                on_click=lambda e: self.animation(self.Login_Page, "Professeur")
                            ),
                            
                            FilledTonalButton(
                                "  Parent",
                                icons.ELDERLY_ROUNDED,
                                width=240,
                                height=55,
                                on_click=lambda e: self.animation(self.Login_Page, "Parent")
                            ),
                        ],

                        spacing=20,
                        alignment=MainAxisAlignment.START,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        scroll=ScrollMode.ADAPTIVE        
                    ),

                    padding=padding.only(top=50),
                    bgcolor=colors.BLUE_50,
                    border=border.all(1, colors.BLACK54),
                    border_radius=border_radius.vertical(30),
                    alignment=alignment.top_center,
                    shadow=BoxShadow(5, 10, colors.BLACK26),
                    expand=True
                )
            ],
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )

        # --------------   Login Page   -------------------

        self.Login_Page = Column(
            [
                Container(
                    Image(
                        src="SoftQuiz_logo.png",
                        error_content=Icon(icons.QUESTION_MARK_ROUNDED, colors.RED, 60),
                        scale=0.8,
                        offset=Offset(0, -0.1)
                    ),
                    bgcolor=colors.LIGHT_BLUE_50,
                    #gradient=RadialGradient(colors=[colors.WHITE, colors.LIGHT_BLUE_50], radius=0.7, center=Alignment(0, 0)),
                    width=500,
                    height=150,
                    border_radius=border_radius.vertical(bottom=60),
                    border=border.only(top=BorderSide(1, colors.BLACK26)) if page.platform in [PagePlatform.WINDOWS, PagePlatform.ANDROID, PagePlatform.LINUX] else None,
                    alignment=alignment.center,
                    shadow=BoxShadow(8, 20, colors.BLACK38)
                ),

                Container(
                        Icon(
                        icons.ACCOUNT_CIRCLE_ROUNDED,
                        colors.BLUE_GREY_700,
                        80,
                    ),
                    offset=Offset(0, -3),
                    shape=BoxShape.CIRCLE,
                    #border=border.all(1, colors.GREY),
                    #bgcolor="white",
                    height=20,
                ),
                    
                TextField(
                    label="Matricule",
                    border_radius=10,
                    keyboard_type=KeyboardType.NUMBER,
                    input_filter=InputFilter(r"[\d]+"),
                    border_color=colors.BLUE_700,
                    prefix_icon=icons.ACCOUNT_BOX_ROUNDED,
                    dense=True,
                    width=self.page.width - 50 if self.page.width <= 500 else 500
                ),

                TextField(
                    label="Mot de passe",
                    border_radius=10,
                    border_color=colors.BLUE_700,
                    prefix_icon=icons.KEY_ROUNDED,
                    password=True,
                    can_reveal_password=True,
                    dense=True,
                    width=self.page.width - 50 if self.page.width <= 500 else 500
                ),

                Divider(
                    height=0,
                    color=colors.TRANSPARENT
                ),

                FilledButton(
                    "Connection",
                    style=ButtonStyle(
                        color={
                            MaterialState.DEFAULT: colors.BLACK,
                            MaterialState.HOVERED: colors.BLACK54
                        },
                        bgcolor={
                            MaterialState.DEFAULT: colors.LIGHT_GREEN_500,
                            MaterialState.HOVERED: colors.LIGHT_GREEN_700
                        }
                    ),
                    width=self.page.width - 50 if self.page.width <= 500 else 500,
                    height=50,
                ),

                Divider(
                    height=3,
                    color=colors.TRANSPARENT
                ),

                Row(
                    [
                        ElevatedButton("  Google  ", icons.THREE_P_ROUNDED),
                        ElevatedButton("  Facebook  ", icons.FACEBOOK)
                    ],
                    alignment=MainAxisAlignment.SPACE_AROUND,
                    width=self.page.width - 50 if self.page.width <= 500 else 500,
                ),

                TextButton(
                    "Mot de passe oublié"
                ),
                
                OutlinedButton(
                    "Créer un compte",
                    icons.ADD
                )
            ],
            spacing=15,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            scroll=ScrollMode.ADAPTIVE       
        )
        
        page.update()

    def KeyBoard_Event_Handler(self, event: KeyboardEvent):
        print(f"Key: {event.key}")
        if event.key == "R":
            self.page.clean()
            self.__init__(self.page)

    def animation(self, widget: Control, *args):
        match widget:
            case self.anim_image:
                widget.opacity = 1
                widget.scale = 0.9
                self.Main_container.gradient = RadialGradient(colors=[colors.BLUE_50, colors.BLUE_300], radius=0.7, center=Alignment(0, -0.1))

            case self.anim_text:
                widget.opacity = 1
                widget.offset = Offset(0, -1)

            case self.anim_progress:
                sleep(1)
                self.anim_progress.opacity = 1

            case self.Choose_Page:
                self.Main_container.animate = None
                self.Main_container.gradient =  RadialGradient(colors=[colors.BLUE_50, colors.BLUE_300], radius=0.7, center=Alignment(0, -0.7))
                
                self.Main_container.padding = padding.only(top=30)
                self.Main_container.alignment = alignment.top_center

                self.Switcher.content = self.Choose_Page

            case self.Login_Page:
                self.page.appbar = AppBar(
                    leading=IconButton(icons.WEST_ROUNDED),
                    automatically_imply_leading=True,
                    title=Text("Connection"),
                    center_title=True,
                    actions=[
                        IconButton(icons.BRIGHTNESS_6_OUTLINED),
                        IconButton(icons.MORE_VERT_SHARP)
                    ],
                    elevation=1,
                    #toolbar_height=40,
                    bgcolor=colors.LIGHT_BLUE_50
                )

                self.Main_container.animate = None
                self.Main_container.gradient = None
                self.Main_container.bgcolor=colors.BLUE_50,
                
                self.Main_container.padding = 0
                self.Main_container.alignment = alignment.top_center

                self.Switcher.content = self.Login_Page           

        self.page.update()
        

app(Main)
