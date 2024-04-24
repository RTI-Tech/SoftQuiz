from socket import AF_INET, SOCK_DGRAM, getaddrinfo, socket
from threading import Event, Timer
from time import time as now, localtime, strftime, strptime
from datetime import time
from flet import*

class Main:
    def __init__(self, page: Page, instances=[], t=[Text, Event(), 60, now(), Text, Text, "INFORMATIQUE"]):
        self.page = page

        page.padding = page.spacing = 0
        
        page.theme_mode = ThemeMode.LIGHT
        page.bgcolor = colors.INDIGO_50

        if not instances and not page.web and page.client_ip in (addr, addr_p) and page.platform not in (PagePlatform.ANDROID, PagePlatform.IOS):
            instances.insert(0, self)

            page.window_left = 0
            page.window_min_width = 900

            t[3] = now()

            page.add( 
                Row(
                    [
                        Container(    
                            Column(
                                [
                                    Row(
                                        [
                                            Text("EVALUATION ", [tit := TextSpan()], theme_style=TextThemeStyle.DISPLAY_SMALL)
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    ),

                                    Divider(20, opacity=0),
                                
                                    col :=  Column(
                                        [
                                            tim := TimePicker(
                                                time.fromisoformat("00:01:00"),
                                                time_picker_entry_mode=TimePickerEntryMode.INPUT,
                                                on_change=lambda e: (ti.__setattr__("value", e.control.value), ti.update())
                                            ),

                                            file := FilePicker(),
                                            
                                            Row(
                                                [   
                                                    TextButton(
                                                        "Cours",
                                                        icons.BOOK_OUTLINED,
                                                        width=120
                                                    ),

                                                    titv := TextField(
                                                        "INFORMATIQUE",
                                                        width=150,
                                                        height=50,
                                                        filled=True,
                                                        border=InputBorder.NONE,
                                                        on_change=lambda e: t.__setitem__(4, e.data)
                                                    )
                                                ],
                                                tight=True,
                                                spacing=0
                                            ),
                                            
                                            Row(
                                                [
                                                    TextButton(
                                                        "Temps",
                                                        icons.TIMER_OUTLINED,
                                                        on_click=lambda e: tim.pick_time(),
                                                        width=120
                                                    ),

                                                    ti := TextField(
                                                        "00:01:00",
                                                        width=150,
                                                        height=50,
                                                        filled=True,
                                                        border=InputBorder.NONE,
                                                        input_filter=InputFilter(""),
                                                        on_focus=lambda e: tim.pick_time()
                                                    )
                                                ],
                                                tight=True,
                                                spacing=0
                                            ),
                                            
                                            Divider(0, opacity=0),

                                            FilledTonalButton(
                                                "Fichier",
                                                icon=icons.FILE_DOWNLOAD_OUTLINED,
                                                style=ButtonStyle(bgcolor=colors.with_opacity(0.6, colors.BLUE_200)),
                                                on_click=lambda e: file.pick_files()
                                            ),

                                            Divider(opacity=0),
                                            
                                            FilledButton(
                                                "Continuer",
                                                #icon=icons.RUN_CIRCLE_OUTLINED,
                                                on_click=lambda e: (t.__setitem__(2, tim.value.hour*3600 + tim.value.minute*60 + tim.value.second),
                                                    b.__setattr__("text", strftime("%Hh %Mm %Ss", strptime(tim.value.isoformat(), "%H:%M:%S"))),
                                                    col.__setattr__("visible", False), t.__setitem__(-1, titv.value), tit.__setattr__("text", ": "+titv.value),
                                                    r.__setattr__("visible", True),
                                                    af.__setattr__("visible", True),
                                                    page.update()
                                                )
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                    
                                    r := Row(
                                        [   
                                            Column(   
                                                [
                                                    Text(
                                                        "SURVEILLANTS",
                                                        theme_style=TextThemeStyle.TITLE_LARGE
                                                    ),

                                                    Column(
                                                        [
                                                            Text(
                                                                "Nombre : ",
                                                                [
                                                                    sur := TextSpan(
                                                                        "0",
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),

                                                            Text(
                                                                "IP : ",
                                                                [
                                                                    TextSpan(
                                                                        page.client_ip,
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),
                                                        ],
                                                        height=100,
                                                        alignment=MainAxisAlignment.SPACE_AROUND,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                                    ),
                                                    
                                                    Container(
                                                        Image(
                                                            "code_QR.png",
                                                            fit=ImageFit.CONTAIN,
                                                            height=100
                                                        ),
                                                        bgcolor=colors.GREY_100,
                                                        padding=10,
                                                        border_radius=10,
                                                        border=border.all(1, colors.GREY)
                                                    )
                                                ],
                                                expand=1,
                                                height=300,
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),

                                            Column(   
                                                [
                                                    Text(
                                                        "TEMPS",
                                                        theme_style=TextThemeStyle.TITLE_LARGE
                                                    ),

                                                    Column(
                                                        [
                                                            Text(
                                                                "Début : ",
                                                                [
                                                                    deb := TextSpan(
                                                                        "",
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),
                                                            
                                                            Text(
                                                                "Fin : ",
                                                                [
                                                                    fin := TextSpan(
                                                                        "",
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),

                                                            Text(
                                                                "Restant : ",
                                                                [
                                                                    (b := TextSpan(
                                                                            style=TextStyle(weight=FontWeight.BOLD),
                                                                    ))
                                                                ],
                                                                size=16
                                                            ),
                                                        ],
                                                        height=100,
                                                        alignment=MainAxisAlignment.SPACE_AROUND,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                                    ),

                                                    Stack(
                                                        [
                                                            Container(
                                                                p := ProgressRing(
                                                                    1,
                                                                    10,
                                                                    width=100,
                                                                    height=100,
                                                                    color=colors.GREEN,
                                                                    bgcolor=colors.WHITE
                                                                ),
                                                                shape=BoxShape.CIRCLE,
                                                                border=border.all(1, colors.BLACK54),
                                                                padding=5
                                                            ),

                                                            Container(
                                                                a := Text(
                                                                    "100%",
                                                                    size=18,
                                                                    weight=FontWeight.BOLD
                                                                ),
                                                                alignment=alignment.center,
                                                                top=11,
                                                                bottom=11,
                                                                left=11,
                                                                right=11,
                                                                shape=BoxShape.CIRCLE,
                                                                border=border.all(1, colors.BLACK54)
                                                            ),
                                                        ]
                                                    )

                                                ],
                                                expand=1,
                                                height=300,
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),

                                            Column(   
                                                [
                                                    Text(
                                                        "ETUDIANTS",
                                                        theme_style=TextThemeStyle.TITLE_LARGE
                                                    ),
                                                    
                                                    Column(
                                                        [
                                                            Text(
                                                                "Total : ",
                                                                [
                                                                    tot := TextSpan(
                                                                        "0",
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),

                                                            Text(
                                                                "Restants : ",
                                                                [
                                                                    n := TextSpan(
                                                                        len(instances)-1,
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),
                                                            
                                                            Text(
                                                                "Terminés : ",
                                                                [
                                                                    ter := TextSpan(
                                                                        "0",
                                                                        style=TextStyle(weight=FontWeight.BOLD)
                                                                    )
                                                                ],
                                                                size=16
                                                            ),
                                                        ],
                                                        height=100,
                                                        alignment=MainAxisAlignment.SPACE_AROUND,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                                    ),

                                                    Container(
                                                        Image(
                                                            "code_QR.png",
                                                            fit=ImageFit.CONTAIN,
                                                            height=100
                                                        ),
                                                        bgcolor=colors.GREY_100,
                                                        padding=10,
                                                        border_radius=10,
                                                        border=border.all(1, colors.GREY)
                                                    )
                                                ],
                                                expand=1,
                                                height=300,
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                horizontal_alignment=CrossAxisAlignment.CENTER
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=CrossAxisAlignment.START,
                                        visible=False
                                    ),

                                    Divider(40, opacity=0),

                                    af := Row(
                                        [                                    
                                            ret := ElevatedButton(
                                                " Retour ",
                                                on_click=lambda e: (af.__setattr__("visible", False), r.__setattr__("visible", False), col.__setattr__("visible", True), page.update())
                                            ),

                                            FilledTonalButton(
                                                " Visualiser ",
                                                style=ButtonStyle(bgcolor=colors.with_opacity(0.6, colors.BLUE_200)),
                                                on_click=lambda e: (
                                                    e.control.__setattr__("text", "Visualiser" if e.control.text == "Cacher" else "Cacher"),
                                                    page.controls[0].controls[1].__setattr__("visible", True if e.control.text == "Cacher" else False),
                                                    page.__setattr__("maximised", e.control.text == "Cacher"),
                                                    page.update()
                                                )
                                            ),

                                            f := FilledButton(
                                                " Démarrer ",
                                                on_click=lambda e: (
                                                    (deb.__setattr__("text", strftime("%Hh %Mm %Ss", localtime())),
                                                    fin.__setattr__("text", strftime("%Hh %Mm %Ss", localtime(now()+t[2]))),
                                                    ret.__setattr__("visible", False), t.__setitem__(3, now()), f.__setattr__("text", " Arrêter "),
                                                    t[1].set(), page.update())  if f.text == " Démarrer " else page.show_dialog(AlertDialog(
                                                        False,
                                                        Text("Fermeture"),
                                                        Text("Etes-vous sûr de vouloir arrêter l'évaluation ? Toutes les données seront perdues !", width=200),
                                                        actions=[
                                                            Row(
                                                                [   FilledButton("Non", on_click=lambda e: page.close_dialog()),
                                                                    ElevatedButton("Oui", on_click=lambda e: (deb.__setattr__("text", 0), fin.__setattr__("text", 0), b.__setattr__("text", 0),ret.__setattr__("visible", True),
                                                                                                            t[1].clear(), t.__setitem__(3, 0), f.__setattr__("text", " Démarrer "), p.__setattr__("value", 1),
                                                                                                            a.__setattr__("value", "100%"), af.__setattr__("visible", True), page.close_dialog(), page.update())
                                                                    )
                                                                ], alignment=MainAxisAlignment.SPACE_AROUND
                                                            )
                                                        ]
                                                    ))
                                                )
                                            )
                                        ],
                                        visible=False,
                                        alignment=MainAxisAlignment.SPACE_AROUND
                                    )
                                ],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                spacing=5,
                                tight=True
                            ),
                            border=border.all(1, colors.BLACK54),
                            border_radius=20,
                            margin=20,
                            bgcolor=colors.WHITE38,
                            alignment=alignment.center,
                            width=800
                        ),
                    ],
                    alignment = MainAxisAlignment.CENTER,
                    expand=True
                )
            )

            t[0] = n
            t[4] = tot
            t[5] = ter

        if True:
            page.add(
                Container(
                    Column(
                        [
                            Text(f"EVALUATION : {t[-1]}", weight=FontWeight.BOLD, size=20),
                            Text('En attente du lancement ...'),
                            ProgressRing()
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    alignment=alignment.center,
                    expand=True,
                    visible=False if page.controls else True
                )
            )

            None if instances and self == instances[0] else t[1].wait()
            
            page.controls.pop()
            None if self == instances[0] else instances.append(self)
            page.fini = False

            def delay():
                t[1].wait()
                time_delta = int(t[2] - (now() - t[3]))

                if time_delta > 0 and not page.fini:
                    p.value = 1-((now() - t[3]) / t[2])

                    if self == instances[0]: a.value = f"{round(p.value*100)}%"

                    b.text = b.value = f"{time_delta // 3600}h {(time_delta % 3600) // 60}m {(time_delta % 3600) % 60}s"

                    if p.value*100 > 90: p.color = colors.GREEN_400
                    elif p.value*100 > 80: p.color = colors.LIME_600
                    elif p.value*100 > 70: p.color = colors.LIME
                    elif p.value*100 > 60: p.color = colors.LIME_400
                    elif p.value*100 > 50: p.color = colors.AMBER_200
                    elif p.value*100 > 40: p.color = colors.AMBER_500
                    elif p.value*100 > 30: p.color = colors.ORANGE
                    elif p.value*100 > 20: p.color = colors.ORANGE_800
                    else: p.color = colors.RED
                    
                    page.update()

                    Timer(0.01, delay).start()
                
                else:
                    p.value = 0
                    b.text = b.value = "Terminé"
                    
                    if self == instances[0]:
                        a.value = "0%"
                        page.update()
                        return
                    
                    b.style = TextStyle(color=colors.PINK_100, weight=FontWeight.BOLD)

                    page.controls[1].disabled = True

                    check.content.controls[1].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.GREEN} if check.content.controls[1].content.controls[0].value else None
                    check.content.controls[2].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.RED} if check.content.controls[2].content.controls[0].value else None
                    check.content.controls[3].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.GREEN} if check.content.controls[3].content.controls[0].value else None
                    check.content.controls[4].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.GREEN} if check.content.controls[4].content.controls[0].value else None
                    
                    check.content.controls[1].content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if check.content.controls[1].content.controls[0].value else Icon(icons.CLOSE_ROUNDED, colors.RED))
                    check.content.controls[2].content.controls.append(Icon(icons.CLOSE_ROUNDED, colors.RED) if check.content.controls[2].content.controls[0].value else Icon(icons.CHECK_ROUNDED, colors.GREEN))
                    check.content.controls[3].content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if check.content.controls[3].content.controls[0].value else Icon(icons.CLOSE_ROUNDED, colors.RED))
                    check.content.controls[4].content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if check.content.controls[4].content.controls[0].value else Icon(icons.CLOSE_ROUNDED, colors.RED))

                    check.content.controls[1].bgcolor = colors.GREEN_50 if check.content.controls[1].content.controls[0].value else colors.RED_50
                    check.content.controls[2].bgcolor = colors.RED_50 if check.content.controls[2].content.controls[0].value else None
                    check.content.controls[3].bgcolor = colors.GREEN_50 if check.content.controls[3].content.controls[0].value else colors.RED_50
                    check.content.controls[4].bgcolor = colors.GREEN_50 if check.content.controls[4].content.controls[0].value else colors.RED_50

                    value = radio.content.controls[1].value

                    radio.content.controls[1].content.controls[0].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.RED} if value == "i" else None
                    radio.content.controls[1].content.controls[1].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.GREEN} if value == "f" else None
                    radio.content.controls[1].content.controls[2].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.RED} if value == "b" else None
                    radio.content.controls[1].content.controls[3].content.controls[0].fill_color = {MaterialState.DISABLED:  colors.RED} if value == "s" else None
                    

                    radio.content.controls[1].content.controls[0].content.controls.append(Icon(icons.CLOSE_ROUNDED, colors.RED) if value == "i" else  Icon(icons.CHECK_ROUNDED, colors.GREEN, visible=False))
                    radio.content.controls[1].content.controls[1].content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if value == "f" else  Icon(icons.CLOSE_ROUNDED, colors.RED, visible=False))
                    radio.content.controls[1].content.controls[2].content.controls.append(Icon(icons.CLOSE_ROUNDED, colors.RED) if value == "b" else  Icon(icons.CHECK_ROUNDED, colors.GREEN, visible=False))
                    radio.content.controls[1].content.controls[3].content.controls.append(Icon(icons.CLOSE_ROUNDED, colors.RED) if value == "s" else  Icon(icons.CHECK_ROUNDED, colors.GREEN, visible=False))

                    radio.content.controls[1].content.controls[0].bgcolor = colors.RED_50 if value == "i" else  None
                    radio.content.controls[1].content.controls[1].bgcolor = colors.GREEN_50 if value == "f" else  None
                    radio.content.controls[1].content.controls[2].bgcolor = colors.RED_50 if value == "b" else  None
                    radio.content.controls[1].content.controls[3].bgcolor = colors.RED_50 if value == "s" else  None

                    if not value:
                        radio.bgcolor = colors.RED_50
                        radio.border = border.all(1, colors.GREY_400)

                    code.bgcolor = colors.GREEN_50 if code.content.controls[0].value.strip() == "10" else colors.RED_50
                    code.content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if code.content.controls[0].value.strip() == "10" else Icon(icons.CLOSE_ROUNDED, colors.RED))
                    code.padding = Padding(10, 10, 20, 10)
                    code.content.controls[0].width = page.width-120 if page.width <= 700 else 620

                    mot.bgcolor = colors.GREEN_50 if mot.content.controls[0].value.strip() == "import" else colors.RED_50
                    mot.content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if mot.content.controls[0].value.strip() == "import" else Icon(icons.CLOSE_ROUNDED, colors.RED))
                    mot.padding = Padding(10, 10, 20, 10)
                    mot.content.controls[0].width = page.width-120 if page.width <= 700 else 620
                    
                    resul.bgcolor = colors.GREEN_50 if resul.content.controls[0].value.strip() == "2**16" else colors.RED_50
                    resul.content.controls.append(Icon(icons.CHECK_ROUNDED, colors.GREEN) if code.content.controls[0].value.strip() == "2**16" else Icon(icons.CLOSE_ROUNDED, colors.RED))
                    resul.padding = Padding(10, 10, 20, 10)
                    resul.content.controls[0].width = page.width-120 if page.width <= 700 else 620

                    instances.remove(self)
                    t[0].text = len(instances) - 1
                    t[5].text = int(t[5].text) + 1
                    instances[0].page.update()
                                  
                    page.update()

            page.add(
                Row(
                    [
                        Container(    
                            Row(
                                [        
                                    Column(
                                        [
                                            (b := Text(
                                                f"{round(100 - ((now() - t[3])*100 / t[2]))}",
                                                weight=FontWeight.BOLD,
                                                color=colors.WHITE,
                                                size=16,
                                            )),
                                            
                                            (p := ProgressBar(
                                                1-((now() - t[3]) / t[2]),
                                                4,
                                                color=colors.GREEN,
                                                bgcolor=colors.WHITE70
                                            ))
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        width=100,
                                        spacing=5
                                    ),

                                    Stack(
                                        [
                                            (pr := ProgressRing(
                                                0,
                                                6,
                                                width=40,
                                                height=40,
                                                color=colors.RED,
                                                bgcolor=colors.WHITE70
                                            )),

                                            Container(
                                                Text(
                                                    "0%",
                                                    size=12
                                                ),
                                                alignment=alignment.center,
                                                width=40,
                                                height=40,
                                            ),
                                        ]
                                    ),

                                    FilledTonalButton(
                                        content=Icon(icons.SEND_ROUNDED, colors.BLUE_900),
                                        on_click=lambda e: page.__setattr__("fini", True)
                                    )
                                ],
                                alignment=MainAxisAlignment.SPACE_AROUND
                            ),
                            width=page.width if page.width < 700 else 700,
                            bgcolor=colors.BLUE_400,
                            padding=padding.symmetric(10)
                        ),
                    ] if self != instances[0] else None,
                    alignment=MainAxisAlignment.CENTER
                ),

                Container(
                    Column(
                        [
                            check := Container(
                                Column(
                                    [
                                        Text("1. Cochez la bonne réponse.\n32767 est un entier de quel sous type ?"),
                                        Container(
                                            Row(
                                                [
                                                    Checkbox("Int")
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.only(right=10)
                                        ),
                                        Container(
                                            Row(
                                                [
                                                    Checkbox("Byte")
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.only(right=10)
                                        ),
                                        Container(
                                            Row(
                                                [
                                                    Checkbox("Short")
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.only(right=10)
                                        ),
                                        Container(
                                            Row(
                                                [
                                                    Checkbox("Long")
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.only(right=10)
                                        ),
                                    ],
                                ),
                                bgcolor=colors.WHITE,
                                padding=20,
                                border_radius=10
                            ),
 
                            radio := Container(
                                Column(
                                    [
                                        Text("2. Lequel de ces types est un réel ?"),
                                        RadioGroup(
                                            Column(
                                                [
                                                    Container(
                                                        Row(
                                                            [
                                                                Radio("int", value="i")
                                                            ],
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN
                                                        ),
                                                        padding=padding.only(right=10)
                                                    ),
                                                    Container(
                                                        Row(
                                                            [
                                                                Radio("float", value="f")
                                                            ],
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN
                                                        ),
                                                        padding=padding.only(right=10)
                                                    ),
                                                    Container(
                                                        Row(
                                                            [
                                                                    Radio("bool", value="b")
                                                            ],
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN
                                                        ),
                                                        padding=padding.only(right=10)
                                                    ),
                                                    Container(
                                                        Row(
                                                            [
                                                                Radio("str", value="s")
                                                            ],
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN
                                                        ),
                                                        padding=padding.only(right=10)
                                                    ),
                                                ]
                                            )
                                        )
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=20,
                                border_radius=10
                            ),
                            
                            Container(
                                Column(
                                    [
                                        Text("3. Après exécution de ce code, qu'est-ce qui sera affiché à l'écran ?"),
                                        Markdown(
                                            "```python \n"
                                            "a = 10 \n"
                                            "b = 100 \n\n"
                                            "for i in range(10): \n"
                                            "   b += a \n\n"
                                            "print(a) \n"
                                            "```",
                                            extension_set=MarkdownExtensionSet.GITHUB_WEB,
                                            code_theme="vs2015",
                                            code_style=TextStyle(14, color=colors.WHITE70, font_family="consolas")
                                        ),
                                        code := Container(
                                            Row(
                                                [
                                                    TextField(
                                                        label="Votre réponse",
                                                        label_style=TextStyle(color=colors.GREY),
                                                        border=InputBorder.UNDERLINE,
                                                        border_color=colors.GREY,
                                                        border_width=1,
                                                        on_focus=lambda e: (e.control.__setattr__("label", ""), e.control.update()),
                                                        on_blur=lambda e: (e.control.__setattr__("label", "" if e.control.value else "Votre réponse"), e.control.update()),
                                                        height=40,
                                                        width=page.width-80 if page.width <= 600 else 620
                                                    )
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.symmetric(10)
                                        )
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=Padding(20, 20, 20, 10),
                                border_radius=10
                            ),
                            
                            Container(
                                Column(
                                    [
                                        Text("4. Quel est le mot clé utilsé en python pour faire l'importation ?"),
                                        mot := Container(
                                            Row(
                                                [
                                                    TextField(
                                                        label="Votre réponse",
                                                        label_style=TextStyle(color=colors.GREY),
                                                        border=InputBorder.UNDERLINE,
                                                        border_color=colors.GREY,
                                                        on_focus=lambda e: (e.control.__setattr__("label", ""), e.control.update()),
                                                        on_blur=lambda e: (e.control.__setattr__("label", "" if e.control.value else "Votre réponse"), e.control.update()),
                                                        height=40,
                                                        width=page.width-80 if page.width <= 600 else 620
                                                    )
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.symmetric(10)
                                        )
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=Padding(20, 20, 20, 10),
                                border_radius=10
                            ),
                            
                            Container(
                                Column(
                                    [   
                                        Text("Ecrire 2^16 en python"),
                                        resul := Container(
                                            Row(
                                                [
                                                    TextField(
                                                        label="Votre réponse",
                                                        label_style=TextStyle(color=colors.GREY),
                                                        border=InputBorder.UNDERLINE,
                                                        border_color=colors.GREY,
                                                        on_focus=lambda e: (e.control.__setattr__("label", ""), e.control.update()),
                                                        on_blur=lambda e: (e.control.__setattr__("label", "" if e.control.value else "Votre réponse"), e.control.update()),
                                                        height=40,
                                                        width=page.width-80 if page.width <= 600 else 620
                                                    )
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN
                                            ),
                                            padding=padding.symmetric(10)
                                        )
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=Padding(20, 20, 20, 10),
                                border_radius=10
                            )
                        ],
                        scroll = ScrollMode.ADAPTIVE,
                        width=700,
                        expand=True
                    ),
                    alignment=alignment.center,
                    padding=padding.only(top=10, bottom=20, left=20, right=20),
                    expand=True,
                    disabled=True if self == instances[0] else False,
                    visible=False if self == instances[0] else True
                )
            )

            delay()

            if self == instances[0]: page.controls[0].controls.append(page.controls.pop())
            else: t[4].text = int(t[4].text) + 1
                
            t[0].text = len(instances) - 1
            instances[0].page.update()

            page.on_disconnect = lambda e: (instances.remove(self), t[0].__setattr__("text", len(instances) - 1), t[5].__setattr__("text", int(t[5].text) + 1), instances[0].page.update())
            page.on_connect = lambda e: (instances.append(self), t[0].__setattr__("text", len(instances) - 1), instances[0].page.update())
            
        page.update()

if __name__ == "__main__":
    Adresses = [addr[-1][0] for addr in getaddrinfo('', 80, AF_INET) if addr[-1][0].startswith("192")]
    Adresses.sort(reverse=True)

    print(Adresses)

    addr = addr_p = ""
                
    s = socket(type=SOCK_DGRAM)

    try:  s.connect(("8.8.8.8", 81))
    except: print("\x1b[31mVous n'êtes pas connectés à un réseau extérieur\x1b[0m")
    else: addr_p = s.getsockname()[0]

    if not addr_p.startswith("192"):
        for addr in Adresses:
            try:
                s = socket()
                s.bind((addr, 81))
            except: ...
            else: s.close(); break

        if not addr: addr = "127.0.0.1"

        if addr != "127.0.0.1" or (addr == "127.0.0.1" and not addr_p):
            print("\x1b[32mUtilisation du réseau local :\x1b[0m", addr)
            print("\x1b[33mIl ne se peut qu'il ne soit visible que par votre ordinateur.\x1b[0m")
        
        else:
            print("\x1b[32mUtilisation du réseau publique :\x1b[0m", s.getsockname())
            print("\x1b[33mWarrning : Ce réseau peut toute fois être indisponible pour les autres, préferé un point d'accès (routeur).\x1b[0m")

    app(Main, port=81, host=addr, view=AppView.FLET_APP_WEB)
