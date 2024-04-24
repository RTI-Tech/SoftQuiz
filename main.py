from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM, getaddrinfo, socket
from threading import Event, Thread
from traceback import print_exc, print_last
from random import randint, sample
from time import sleep
from flet import*

class Main:
    def __init__(self, page: Page):
        self.page = page

        page.adaptive = True
        page.window_always_on_top = True

        """ Cette fonction permet à l'utilisateur de
            retourner à la précédente vue ou page
        """
        page.on_view_pop = self.on_view_pop

        # Detecter le changement de page
        page.on_route_change = self.on_route_change

        # Le thème de l'application
        page.theme = Theme(
            color_scheme_seed=colors.BLUE_400
        )

        page.theme_mode = ThemeMode.LIGHT
        #page.platform = PagePlatform.IOS
        
        # L'animations de transition entre les pages pour chaque plateforme
        page.theme.page_transitions = PageTransitionsTheme(
            android=PageTransitionTheme.CUPERTINO,
            ios=PageTransitionTheme.CUPERTINO,
            macos=PageTransitionTheme.CUPERTINO,
            linux=PageTransitionTheme.CUPERTINO,
            windows=PageTransitionTheme.CUPERTINO
        )

        # Pour les ordinateurs uniquement
        page.window_left = 960
        page.window_width = 400
        page.window_height = 700
        page.padding = 0

        # Pour les clics au clavier
        page.on_keyboard_event = self.on_keyboard_event

        # Pour contrôler la vibration
        self.haptic = HapticFeedback()
        page.overlay.append(self.haptic)

        # Aller à la page correspondante
        page.go(page.route)

    def on_view_pop(self, event: ViewPopEvent):
        self.page.views.pop()
        self.page.route = self.page.views[-1].route
        self.page.update()

    def on_route_change(self, event: RouteChangeEvent):
        if self.page.views and self.page.views[-1].route == event.route: return
        {
            "": self.Page_Animation,
            "Selection": self.Page_Selection,
            "Accueil": self.Page_Accueil,
            "Connection": self.Page_Connection,
            "Evaluation_locale": self.Page_Evaluation_Locale

        }.get(event.route.removeprefix("/")) ()

    def Page_Animation(self):
        self.page.controls.clear()

        self.anim_image = Image(
            src="SoftQuiz_logo.png",
            error_content=Icon(icons.ERROR, colors.RED, 60),
            opacity=0,
            scale=0,
            offset=Offset(0, -0.2),
            animate_scale=500,
        )

        self.anim_text = Text(
            "Pour une une gestion optimale de vos évalutions",
            #font_family="Times",
            #theme_style=TextThemeStyle.TITLE_MEDIUM,
            text_align=TextAlign.CENTER,
            opacity=0,
            offset=Offset(0, -1),
            animate_opacity=1000
        )

        self.anim_progress = ProgressRing(
            value=None,
            opacity=0,
            stroke_width=2,
            animate_opacity=500
        )

        # Conteneur principal
        self.Main_container = Container(
            Column(
                [
                    self.anim_image,
                    self.anim_text,
                    self.anim_progress
                ],
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER
            ),

            gradient=RadialGradient(
                colors=[colors.BLUE_100,
                        colors.BLUE_200],
                radius=0.7,
                center=Alignment(0, -0.1)
            ),
            alignment=alignment.center,
            animate=1000,
            expand=True
        )

        # Ajout du conteneur principal
        self.page.add(self.Main_container)
        self.page.update()

        # -----------      Animation     ------------------
        sleep(0.5)
        self.anim_image.opacity = 1
        self.anim_image.scale = 0.9

        self.Main_container.gradient = RadialGradient(
                                                    colors=[
                                                        colors.BLUE_50,
                                                        colors.BLUE_300
                                                    ],
                                                    radius=0.7,
                                                    center=Alignment(0, -0.1)
                                                )
        self.page.update()

        sleep(1)
        self.anim_text.opacity = 1
        self.page.update()

        sleep(2)
        self.anim_progress.opacity = 1
        self.page.update()

        sleep(2)
        self.page.go("Selection")

    def Page_Selection(self):
        if self.page.client_storage.contains_key("identifiants"): return self.page.go("Accueil")
        
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
                                " Université",
                                icons.SCHOOL_ROUNDED,
                                width=240,
                                height=55,
                                on_click=lambda e: (self.page.client_storage.set("user", "University"), self.page.go("Connection"))
                            ),

                            FilledTonalButton(
                                "   Etudiant",
                                icons.MAN_ROUNDED,
                                width=240,
                                height=55,
                                on_click=lambda e: (self.page.client_storage.set("user", "Etudiant"), self.page.go("Connection"))
                            ),
                            
                            FilledTonalButton(
                                " Professeur",
                                icons.SUPERVISOR_ACCOUNT,
                                width=240,
                                height=55,
                                on_click=lambda e: (self.page.client_storage.set("user", "Professeur"), self.page.go("Connection"))
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

        # Conteneur principal
        self.Main_container = Container(
            self.Choose_Page,
            gradient=RadialGradient(
                colors=[colors.BLUE_50,
                        colors.BLUE_300],
                radius=0.7,
                center=Alignment(0, -0.7)
            ),
            alignment=alignment.top_center,
            padding=padding.only(top=50),
            expand=True
        )

        self.page.views.append(
            View(
                "Selection",
                [
                    self.Main_container
                ],
                padding=0
            )
        )

        self.page.update()

    def Page_Connection(self):
        if self.page.client_storage.contains_key("identifiants"): return self.page.go("Accueil")

        self.Login_Page = Column(
            [
                Stack(
                    [
                        Container(
                            Image(
                                src="SoftQuiz_logo.png",
                                error_content=Icon(icons.QUESTION_MARK_ROUNDED, colors.RED, 60),
                                scale=0.8
                            ),
                            bgcolor=colors.LIGHT_BLUE_50,
                            gradient=RadialGradient(colors=[colors.BLUE_50, colors.BLUE_200], radius=0.8, center=Alignment(0, -0.1)),
                            width=500,
                            height=160,
                            border_radius=border_radius.vertical(bottom=60),
                            border=border.all(1, colors.BLACK45),
                            alignment=alignment.top_center,
                            shadow=BoxShadow(8, 20, colors.BLACK38)
                        ),
                
                        Container(
                                Icon(
                                icons.ACCOUNT_CIRCLE_ROUNDED,
                                colors.BLUE_GREY_700,
                                80,
                            ),
                            bgcolor=colors.WHITE,
                            bottom=10,
                            left=0,
                            right=0,
                            shape=BoxShape.CIRCLE,
                            border=border.all(1, colors.BLACK38),
                        )
                    ],
                    height=210
                ),
                
                Column(
                    [
                        Divider(opacity=0, height=0),

                        matricule := TextField(
                            label="Matricule",
                            border_radius=10,
                            keyboard_type=KeyboardType.NUMBER,
                            input_filter=InputFilter(r"[\d]+"),
                            border_color=colors.BLACK38,
                            focused_border_color=colors.BLUE_400,
                            bgcolor=colors.WHITE,
                            prefix_icon=icons.ACCOUNT_BOX_ROUNDED,
                            dense=True,
                            width=self.page.width - 50 if self.page.width <= 500 else 500
                        ),

                        mot_de_passe := TextField(
                            label="Mot de passe",
                            border_radius=10,
                            border_color=colors.BLACK38,
                            focused_border_color=colors.BLUE_400,
                            bgcolor=colors.WHITE,
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
                            content=Text("Enregistrer", theme_style=TextTheme.display_large),
                            on_click=lambda e: (self.page.client_storage.set("identifiants", {"matricule": matricule.value, "mot_de_passe": mot_de_passe.value}), self.page.go("Accueil")),
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
                        )
                    ],
                    spacing=15,
                    expand=True,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    scroll=ScrollMode.ADAPTIVE
                )
            ],
            alignment=MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            expand=True
        )

        appbar = AppBar(
            title=Text("Connection"),
            #center_title=True,
            actions=[
                IconButton(icons.BRIGHTNESS_6_OUTLINED),
                #IconButton(icons.MORE_VERT_SHARP)
            ],
            elevation=0,
            #color="red",
            #toolbar_height=40,
            bgcolor=colors.BLUE_200
        )
                
        self.page.views.append(
            View(
                "Connection",
                [
                    self.Login_Page
                ],
                appbar=appbar,
                padding=0,
                bgcolor=colors.BLUE_50
            )
        )
        
        self.page.update()

    def Page_Accueil(self):

        self.Home_Page = Tabs(
            tabs=[
                Tab(
                    tab_content=Row(
                        [    
                            Icon(icons.HOME_ROUNDED),
                            Text("Accueil")
                        ]
                    ),
                    content=Container(    
                        Column(
                            [   
                                ResponsiveRow(
                                    [
                                        Container(
                                            ExpansionTile(
                                                [
                                                    Container(
                                                        Row(
                                                            [
                                                                IconButton(icons.BAR_CHART_ROUNDED, colors.BLACK),
                                                                IconButton(icons.ASSIGNMENT_OUTLINED, colors.BLACK),
                                                                IconButton(icons.ACCOUNT_CIRCLE_ROUNDED, colors.BLACK),
                                                            ],
                                                            alignment=MainAxisAlignment.END,
                                                            vertical_alignment=CrossAxisAlignment.END,
                                                            spacing=0
                                                        ),
                                                        height=150,
                                                        border_radius=border_radius.vertical(0, 40),
                                                        padding=5,
                                                        bgcolor=colors.WHITE,
                                                        border=border.only(top=BorderSide(1, colors.GREY))
                                                    ),
                                                ],

                                                leading=IconButton(icons.MORE_VERT_ROUNDED),
                                                tile_padding=padding.only(right=20),
                                                title=Row(
                                                    [
                                                        Text(cours),
                                                        Badge(
                                                            text=(i := randint(0, 5)),
                                                            bgcolor='pink500',
                                                            label_visible=bool(i)
                                                        )
                                                    ],
                                                    alignment=MainAxisAlignment.SPACE_BETWEEN
                                                ),
                                                subtitle=Text("L2 LMD"),
                                                shape=RoundedRectangleBorder(),
                                                icon_color=colors.BLACK,
                                                initially_expanded=True,
                                                #maintain_state=True
                                            ),
                                        bgcolor=color,
                                        border=border.all(1, colors.GREY_500),
                                        border_radius=40,
                                        col={"sm":6, "lg":4, "xxl":3}
                                        ) for cours, color in zip(("Physique", "Algèbre", "Algorithme", "Java", "Trigonométrie"), sample([color for color in list(colors.__dict__.values())[9:] if color.endswith("100")], k=5))
                                    ],
                                    columns=12
                                )
                            ],
                            scroll=ScrollMode.ADAPTIVE
                        ),
                        bgcolor=colors.WHITE,
                        padding=padding.symmetric(15, 10)
                    )
                ),
                
                Tab(
                    tab_content=Row(
                        [    
                            Icon(icons.COLLECTIONS_BOOKMARK_ROUNDED),
                            Text("Cours")
                        ]
                    ),
                    content=Container(bgcolor=colors.WHITE)
                ),
                
                Tab(
                    tab_content=Row(
                        [    
                            Icon(icons.SUPERVISOR_ACCOUNT_ROUNDED),
                            Text("Compte")
                        ]
                    ),
                    content=Container(
                        Column(
                            [
                                Container(
                                    Column(
                                        [
                                            Container(
                                                Icon(
                                                    icons.ACCOUNT_CIRCLE_ROUNDED,
                                                    colors.BLUE_GREY_700,
                                                    80,
                                                ),
                                                bgcolor=colors.WHITE,
                                                shape=BoxShape.CIRCLE,
                                                border=border.all(1, colors.BLACK38),
                                            ),
                                            Text(self.page.client_storage.get('identifiants')['matricule'], color=colors.WHITE),
                                            Text(self.page.client_storage.get('user'), color=colors.WHITE),
                                            Container(
                                                Row(
                                                    [
                                                        Column(
                                                            [
                                                                Text(10, color=colors.WHITE, text_align=TextAlign.CENTER),
                                                                Text("Cours", color=colors.WHITE)
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                            spacing=0
                                                        ),
                                                        Column(
                                                            [
                                                                Text(5, color=colors.WHITE, text_align=TextAlign.CENTER),
                                                                Text("Devoirs", color=colors.WHITE)
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                            spacing=0
                                                        ),
                                                        Column(
                                                            [
                                                                Text(20, color=colors.WHITE, text_align=TextAlign.CENTER),
                                                                Text("Achevés", color=colors.WHITE)
                                                            ],
                                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                                            spacing=0
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.SPACE_AROUND
                                                ),
                                                bgcolor=colors.BLUE_600,
                                                padding=padding.symmetric(0, 10)
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                    bgcolor=colors.BLUE_400,
                                    border_radius=border_radius.vertical(bottom=30),
                                    width=self.page.width,
                                    padding=padding.only(top=30)
                                ),
                                Container(
                                    Column(
                                        [
                                            ListTile(padding.only(left=10), leading=Icon(icons.MANAGE_ACCOUNTS_ROUNDED), title=Text("Paramètres"), trailing=Icon(icons.ARROW_FORWARD_IOS)),
                                            ListTile(padding.only(left=10), leading=Icon(icons.HISTORY_ROUNDED), title=Text("Hitorique"), trailing=Icon(icons.ARROW_FORWARD_IOS)),
                                            ListTile(padding.only(left=10), leading=Icon(icons.SETTINGS_APPLICATIONS_ROUNDED), title=Text("Parametres"), trailing=Icon(icons.ARROW_FORWARD_IOS)),
                                            ListTile(padding.only(left=10), leading=Icon(icons.LOGOUT_ROUNDED), title=Text("Déconnection"), trailing=Icon(icons.ARROW_FORWARD_IOS))
                                        ]
                                    ),
                                    padding=padding.symmetric(10, 20)
                                )
                            ]
                        ),
                        bgcolor=colors.BLUE_50
                    )
                ),
            ],
            tab_alignment=TabAlignment.CENTER,
            indicator_color=colors.TRANSPARENT,
            label_color=colors.BLACK,
            unselected_label_color=colors.WHITE70,
            divider_color=colors.BLUE_400,
            expand=True
        )

        self.page.views.clear()

        self.page.views.append(
            View(
                "Accueil",
                [
                    Container(
                        self.Home_Page,
                        bgcolor=colors.BLUE_400,
                        expand=True
                    )
                ],
                
                appbar= AppBar(
                    leading=IconButton(icons.MENU_ROUNDED, on_click=lambda e: self.page.show_drawer(self.page.views[-1].drawer)),
                    title=Text("SoftQuiz"),
                    center_title=True,
                    actions=[
                        IconButton(icons.SEARCH_ROUNDED),
                        IconButton(
                            icons.BRIGHTNESS_6_OUTLINED,
                            selected_icon=icons.BRIGHTNESS_6,
                            selected=self.page.theme_mode == ThemeMode.DARK,
                            on_click=lambda e: (
                                (self.page.__setattr__("theme_mode", ThemeMode.LIGHT), e.control.__setattr__("selected", False)) if self.page.theme_mode == ThemeMode.DARK
                                else (self.page.__setattr__("theme_mode", ThemeMode.DARK), e.control.__setattr__("selected", True)),
                                self.page.update()
                            )
                        ),
                        #IconButton(icons.MORE_VERT_SHARP)
                    ],
                    elevation=0,
                    #color="red",
                    #toolbar_height=40,
                    bgcolor=colors.BLUE_400
                ),
                
                bottom_appbar=BottomAppBar(
                    bgcolor=colors.BLUE_300,
                    shape=NotchShape.CIRCULAR,
                    notch_margin=15,
                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                    content=Container(
                        Row(
                            [
                                Column([selected := IconButton(icons.HOME_ROUNDED, icon_color=colors.BLACK, bgcolor=colors.WHITE, on_click=lambda e: (self.selected.__setattr__("bgcolor", colors.TRANSPARENT), e.control.__setattr__("bgcolor", colors.WHITE), self.__setattr__("selected", e.control), self.Home_Page.__setattr__("selected_index", 0), self.page.update())), Text("Accueil")], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=0, expand=2),
                                Column([IconButton(icon=icons.SCHOOL, icon_color=colors.BLACK, on_click=lambda e: (self.selected.__setattr__("bgcolor", colors.TRANSPARENT), e.control.__setattr__("bgcolor", colors.WHITE), self.__setattr__("selected", e.control), self.Home_Page.__setattr__("selected_index", 1), self.page.update())), Text("Cours")], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=0, expand=2),
                                Column([Icon(icons.MORE_VERT_ROUNDED)], alignment=MainAxisAlignment.END, horizontal_alignment=CrossAxisAlignment.CENTER, expand=2, opacity=1),
                                Column([IconButton(icon=icons.ACCOUNT_BOX_ROUNDED, icon_color=colors.BLACK, on_click=lambda e: (self.selected.__setattr__("bgcolor", colors.TRANSPARENT), e.control.__setattr__("bgcolor", colors.WHITE), self.__setattr__("selected", e.control), self.Home_Page.__setattr__("selected_index", 2), self.page.update())), Text("Compte")], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=0, expand=2),
                                Column([IconButton(icon=icons.SETTINGS_ROUNDED, icon_color=colors.BLACK, on_click=lambda e: (self.selected.__setattr__("bgcolor", colors.TRANSPARENT), e.control.__setattr__("bgcolor", colors.WHITE), self.__setattr__("selected", e.control), self.page.update())), Text("Options")], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=0, expand=2),
                            ],
                            alignment=MainAxisAlignment.SPACE_AROUND,
                            spacing = 10
                        ),
                        padding=padding.symmetric(10)
                    ),
                    height=100,
                    visible=False
                ),

                drawer = NavigationDrawer(
                    [
                        Container(
                            IconButton(
                                icons.CLOSE_ROUNDED,
                                on_click=lambda e: self.page.close_drawer()
                            ),
                            alignment=Alignment(-0.9, 0),
                            on_click=lambda e: self.page.close_drawer(),
                            ink=True
                        ),
                        
                        Image(
                            "SoftQuiz_logo.png",
                            fit=ImageFit.FIT_HEIGHT,
                            offset=Offset(-0.01, -0.2),
                            height=80
                        ),
                        
                        NavigationDrawerDestination(
                            "Accueil",
                            icons.HOME_ROUNDED
                        ),
                        
                        NavigationDrawerDestination(
                            "Cours",
                            icons.COLLECTIONS_BOOKMARK_ROUNDED
                        ),
                        
                        NavigationDrawerDestination(
                            "Compte",
                            icons.ACCOUNT_CIRCLE_ROUNDED
                        ),

                        Divider(thickness=1),

                        NavigationDrawerDestination(
                            "Parametres",
                            icons.SETTINGS_ROUNDED
                        ),

                        NavigationDrawerDestination(
                            "A prpos",
                            icons.INFO_OUTLINE_ROUNDED
                        ),

                        Divider(thickness=1),

                        Container(height=self.page.height - 630),

                        NavigationDrawerDestination(
                            "Déconnexion",
                            icons.LOGOUT_ROUNDED
                        ),

                        NavigationDrawerDestination(
                            "Quitter",
                            icons.POWER_SETTINGS_NEW_ROUNDED
                        ),

                        NavigationDrawerDestination(
                            "Réduire",
                            icons.ARROW_BACK_IOS_NEW_ROUNDED
                        ),

                        TextButton("v1.0.0"),
                    ],
                    on_change=lambda e: (self.page.show_dialog(self.page.dialog) if e.data == "5" else
                                         self.page.close_drawer() if e.data == "7" else None)
                ),

                floating_action_button=FloatingActionButton(
                    content=PopupMenuButton(
                        Icon(
                            icons.POST_ADD_ROUNDED,
                            colors.BLACK,
                            26
                        ),
                        items=[
                            PopupMenuItem(
                                "Evaluation locale",
                                icons.BROADCAST_ON_HOME_ROUNDED, #ADD_TO_QUEUE_OUTLINED,
                                on_click=lambda e: self.page.go("Evaluation_locale")
                            ),
                            PopupMenuItem(
                                "Nouveau cours",
                                icons.MY_LIBRARY_ADD_OUTLINED
                            ),
                            PopupMenuItem(
                                "Nouveau Document",
                                icons.POST_ADD_OUTLINED
                            ),
                            PopupMenuItem(
                                "Nouvelle classe",
                                icons.DOMAIN_ADD_OUTLINED
                            ),
                            PopupMenuItem(
                                "Nouvelle evaluation",
                                icons.ASSIGNMENT_ADD
                            ),
                            PopupMenuItem(
                                "Nouvelle personne",
                                icons.PERSON_ADD_ALT_1_OUTLINED
                            )
                        ]
                    ),
                    bgcolor=colors.BLUE_400
                ),
                
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
                padding=0,
            )
        )

        self.selected = selected
        
        self.page.dialog = AlertDialog(
            False,
            Text("Déconnection"),
            Text("Souhaitez-vous vraiment vous déconnecter ?"),
            [
                Row(
                    [
                        FilledButton("Non", on_click=lambda e: self.page.close_dialog()),
                        OutlinedButton("Oui", on_click=lambda e: (self.page.close_dialog(), self.page.views.pop(), self.page.client_storage.remove("identifiants"), self.page.go("Selection")))
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY
                    )
            ]
        )

        setattr(self.page.theme.page_transitions, self.page.platform.value, PageTransitionTheme.ZOOM)
        self.page.update()

    def Page_Evaluation_Locale(self):
        block = Event()

        def recherche():
            if block.is_set(): block.clear()
            
            Adresses = [addr[-1][0] for addr in getaddrinfo('', 80, AF_INET)]
            print(Adresses)
            
            s = socket(type=SOCK_DGRAM)

            try:  s.connect(("8.8.8.8", 53))
            except Exception as e: print(e); self.text.visible = True; self.page.update()
            else: self.text.visible = False; self.page.update()

            for addresse in Adresses:
                tete, _, _ = addresse.rpartition(".")

                for i in range(1, 255):
                    addr = f"{tete}.{i}"
                    try:
                        my_socket = socket(AF_INET, SOCK_STREAM)
                        my_socket.settimeout(0.01)
                        
                        my_socket.connect((addr, 81))

                    except TimeoutError: my_socket.close(); print(addr)
                    except: print(addr); print_exc(); my_socket.close()
                    else:
                        self.page.overlay.append(App := FletApp(
                                                    f"http://{addr}:81",
                                                    1000,
                                                    on_error=lambda e: (print(f"Erreur lors de la connection à {e.control.url}"), block.set() if not block.isSet() else Thread(target=recherche).start(), self.page.overlay.clear(), self.page.update())
                                                    )
                        )

                        print("Trouvé :", addr)
                        self.page.update()
                        if block.wait(60): block.clear()
                        else: block.set(); return print("Connection supposée réussie")
                        print("Retour")

            self.text.visible = True; self.page.update()
            if self.page.views[-1].route == "Evaluation_locale": print("recommencer"); recherche()

        self.page.views.append(
            View(
                "Evaluation_locale",
                [
                    Container(
                        Column(
                            [
                                Text(
                                    "Recherche d'une évaluation",
                                    theme_style=TextThemeStyle.TITLE_MEDIUM
                                ),

                                Stack(
                                    [
                                        IconButton(
                                            icons.WIFI_FIND_ROUNDED,
                                            width=40,
                                            height=40
                                        ),
                                        ProgressRing(
                                            stroke_width=2,
                                            width=40,
                                            height=40
                                        )
                                    ]
                                ),

                                text := Text(
                                    "Rassurez-vous que vous êtes connecté au réseau WI-FI !",
                                    color=colors.RED,
                                    text_align=TextAlign.CENTER,
                                    width=self.page.width - 80,
                                    visible=False
                                ),

                                Evaluation := FletApp(
                                    on_error=lambda e: print(e.data),
                                    expand=True,
                                    visible=False
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        alignment=alignment.center,
                        bgcolor=colors.WHITE,
                        expand=True
                    )
                ],
                
                appbar= AppBar(
                    leading=IconButton(
                        icons.ARROW_BACK_ROUNDED,
                        on_click=lambda e: self.page.show_dialog(self.page.dialog)
                    ),
                    title=Text("Evalution"),
                    center_title=True,
                    actions=[
                        IconButton(icons.HELP_OUTLINE)
                    ],
                    elevation=0,
                    bgcolor=colors.BLUE_400
                ),

                floating_action_button=FloatingActionButton(
                    content=PopupMenuButton(
                        Icon(
                            icons.CALCULATE_OUTLINED , #HOME_ROUNDED, #CONSTRUCTION_OUTLINED
                            colors.WHITE,
                            size=30
                        ),
                        items=[
                            PopupMenuItem(
                                "Calculatrice",
                                icons.CALCULATE_OUTLINED,
                            ),
                            PopupMenuItem(
                                "Document",
                                icons.MY_LIBRARY_BOOKS_OUTLINED
                            ),
                            PopupMenuItem(
                                "Message",
                                icons.MESSAGE_OUTLINED
                            ),
                            PopupMenuItem(
                                "Aide",
                                icons.HELP_OUTLINE
                            )
                        ]
                    ),
                    bgcolor=colors.BLUE_400
                ),
                
                floating_action_button_location=FloatingActionButtonLocation.END_FLOAT,
                padding=0,
            )
        )
        
        self.page.dialog = AlertDialog(
            False,
            Text("Fermeture"),
            Text("Souhaitez-vous vraiment vous quitter ?"),
            [
                Row(
                    [
                        FilledButton(
                            "Non",
                            on_click=lambda e: self.page.close_dialog()
                        ),
                        OutlinedButton(
                            "Oui",
                            on_click=lambda e: (self.page.close_dialog(), (self.page.overlay.clear(), self.page.update()) if self.page.overlay else self.on_view_pop(None))
                        )
                    ],
                    alignment=MainAxisAlignment.SPACE_EVENLY
                    )
            ]
        )

        self.text = text
        Thread(target=recherche()).start()

        self.page.update()

    def on_keyboard_event(self, event: KeyboardEvent):
        print(f"Key: {event.key}")
        if event.key == "R":
            self.page.clean()
            self.__init__(self.page)


app(Main, port=80, host="192.168.173.1", view=AppView.FLET_APP_WEB)
