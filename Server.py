from threading import Event, Timer
from time import time, strftime, ctime, localtime
from flet import*

class Main:
    def __init__(self, page: Page, instances=[], t=[Text, Event(), 2*60, time()]):
        self.page = page

        page.window_left = 0
        page.window_width = 700
        
        page.theme_mode = ThemeMode.LIGHT
        page.bgcolor = colors.BLUE_50

        page.padding = 20

        if not page.web and page.platform not in (PagePlatform.ANDROID, PagePlatform.IOS):
            instances.insert(0, self)

            t[3] = time()

            page.add( 
                Container(    
                    Column(
                        [
                            Row(
                                [
                                    Text("EVALUATION", size=20, weight=FontWeight.BOLD)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            r := Row(
                                [
                                    Text("Etudiants connectés:"), n := Text(len(instances)-1)
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                visible=False
                            ),
                            TextField(120, input_filter=InputFilter('[0-9]'), suffix_text="secondes", width=150, on_submit=lambda e: (t[1].set(), t.__setitem__(2, int(e.control.value)), t.__setitem__(3, time()), e.control.__setattr__("visible", False), r.__setattr__("visible", True), page.update())),
                            Row(
                                [
                                    ElevatedButton("Afficher", on_click=lambda e: (e.control.__setattr__("text", "Afficher" if e.control.text == "Cacher" else "Cacher"), page.controls[2].__setattr__("visible", True if e.control.text == "Cacher" else False), page.update())),
                                ],
                                alignment=MainAxisAlignment.SPACE_AROUND
                            )
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    padding=Padding(20, 20, 20, 30),
                    border_radius=50,
                    bgcolor=colors.WHITE
                ),
                Divider(5)
            )

            t[0] = n

        else:
            page.add(
                Container(
                    Column(
                        [
                            Text("EVALUATION DE JAVA", weight=FontWeight.BOLD, size=20),
                            Text('En attente ...'),
                            ProgressRing()
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER
                    ),
                    alignment=alignment.center,
                    expand=True
                )
            )

            t[1].wait()
            
            page.clean()
            instances.append(self)

            def delay():
                time_delta = int(t[2] - (time() - t[3]))

                if time_delta > 0:
                    p.value = 1-((time() - t[3]) / t[2])
                    a.value = f"{round(p.value*100)}%"
                    b.value = f"{time_delta // 3600}h {(time_delta % 3600) // 60}m {(time_delta % 3600) % 60}s"

                    if p.value*100 > 90: p.color = colors.GREEN_600
                    elif p.value*100 > 80: p.color = colors.GREEN_400
                    elif p.value*100 > 70: p.color = colors.LIME
                    elif p.value*100 > 60: p.color = colors.LIME_400
                    elif p.value*100 > 50: p.color = colors.AMBER_200
                    elif p.value*100 > 40: p.color = colors.AMBER_500
                    elif p.value*100 > 30: p.color = colors.ORANGE
                    elif p.value*100 > 20: p.color = colors.ORANGE_800
                    else: p.color = colors.RED
                    a.color = colors.BLACK
                    page.update()

                    Timer(0.01, delay).start()
                else:
                    p.value = 0
                    a.value = f"0%"; a.color = colors.BLACK
                    b.value = f"0h 0m 0s"
                    page.controls[2].disabled = True
                    page.update()

            page.add(
                Row(
                    [
                        Stack(
                                [
                                    (p := ProgressRing(
                                        1-((time() - t[3]) / t[2]),
                                        5,
                                        width=50,
                                        height=50,
                                        color=colors.GREEN,
                                        bgcolor=colors.BLUE_100
                                    )),
                                    Container(a := Text(f"{round(100 - ((time() - t[3])*100 / t[2]))}%"), alignment=alignment.center, width=50, height=50),
                                ]
                            ),
                            (b := Text(f"{round(100 - ((time() - t[3])*100 / t[2]))} restant"))
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),

                Divider(10, opacity=0),

                Column(
                        [
                            Container(
                                Column(
                                    [
                                        Text("1. Cochez la bonne réponse.\n32767 est un entier de quel sous type ?"),
                                        Checkbox("Int"), Checkbox("Byte"), Checkbox("Short"), Checkbox("Long")
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=10,
                                border_radius=10
                            ),
                            Container(
                                Column(
                                    [
                                        Text("2. Lequel de ces types est un réel ?"),
                                        r := RadioGroup(Column(
                                            [
                                                Radio("int", value="i"),
                                                Radio("float", value="f"),
                                                Radio("bool", value="b"),
                                                Radio("str", value="s")
                                            ]
                                        ))
                                    ]
                                ),
                                bgcolor=colors.WHITE,
                                padding=10,
                                border_radius=10
                            ),
                            Row(
                                [
                                    ElevatedButton("Afficher", on_click=lambda e: page.connection)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            )
                        ],
                        scroll = ScrollMode.ADAPTIVE,
                        expand=True
                )
            )

            delay()

            t[0].value = len(instances) - 1
            instances[0].page.update()

            page.on_disconnect = lambda e: (instances.remove(self), t[0].__setattr__("value", len(instances) - 1), instances[0].page.update())
            page.on_connect = lambda e: (instances.append(self), t[0].__setattr__("value", len(instances) - 1), instances[0].page.update())
            
        page.update()
    
        
app(Main, port=81, host="localhost", view=AppView.FLET_APP_WEB)
