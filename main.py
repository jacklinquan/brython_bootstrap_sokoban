from browser import document, html, window, timer, alert, markdown, console, bind  # type: ignore
from interpreter import Interpreter  # type: ignore
import math
import struct
import base64

from sokobanpy import SokobanVector, Sokoban  # type: ignore


def text_follow_value(a, b):
    a.text = b.value


class WebApp:
    def __init__(self) -> None:
        self.build_ui()

    def build_ui(self):
        # Title
        document.title = "Sokoban"

        # Favicon
        document["favicon"].href = (
            "data:image/png;base64,"
            "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAABhGlDQ1BJQ0MgcHJv"
            "ZmlsZQAAKJF9kT1Iw0AcxV8/tCIVUYuIOGSoTnZREcdSxSJYKG2FVh1MLv2CJg1J"
            "iouj4Fpw8GOx6uDirKuDqyAIfoC4C06KLlLi/5JCixgPjvvx7t7j7h3gbVSYYvij"
            "gKKaeioeE7K5VSHwim4Mwo9hDIjM0BLpxQxcx9c9PHy9i/As93N/jj45bzDAIxBH"
            "maabxBvEs5umxnmfOMRKokx8Tjyp0wWJH7kuOfzGuWizl2eG9ExqnjhELBQ7WOpg"
            "VtIV4hnisKyolO/NOixz3uKsVGqsdU/+wmBeXUlzneYY4lhCAkkIkFBDGRWYiNCq"
            "kmIgRfsxF/+o7U+SSyJXGYwcC6hCgWj7wf/gd7dGYXrKSQrGgK4Xy/oYBwK7QLNu"
            "Wd/HltU8AXzPwJXa9lcbwNwn6fW2Fj4C+reBi+u2Ju0BlzvAyJMm6qIt+Wh6CwXg"
            "/Yy+KQcM3QK9a05vrX2cPgAZ6mr5Bjg4BCaKlL3u8u6ezt7+PdPq7wdn0nKig4/q"
            "FgAAAAlwSFlzAAAuIwAALiMBeKU/dgAAAAd0SU1FB+kGEgQzJEeuo2MAAAAZdEVY"
            "dENvbW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAATElEQVRIx2NgGAUDDRiR"
            "Of///6eOoYwIY5lo7YOhbwELMeGIHDfI4sTE32gcjFowlPMBLkBMnhiNA+rHAa5y"
            "aTQfjNbJw8SCUTDwAADYCxI11hkOtAAAAABJRU5ErkJggg=="
        )

        # Page container
        self.page_list = []
        self.html_page_container = html.DIV(Class="container")

        # Home Page
        html_page_home = self.build_page_home()
        self.page_list.append(html_page_home)
        self.html_page_container <= html_page_home

        # About Page
        html_page_about = self.build_page_about()
        self.page_list.append(html_page_about)

        # Tools Page
        html_page_tools = self.build_page_tools()
        self.page_list.append(html_page_tools)

        # Offcanvas
        page_label_list = [
            "Home",
            "About",
            "Tools",
        ]
        page_link_list = []
        for (
            i,
            page_label,
        ) in enumerate(page_label_list):
            link = html.A(
                page_label,
                Class="list-group-item list-group-item-action",
                data_bs_dismiss="offcanvas",
                href="#",
            )
            link.bind(
                "click",
                (lambda ev, page_num=i: self.offcanvas_link_action(ev, page_num)),
            )
            page_link_list.append(link)

        document <= html.DIV(
            [
                html.DIV(
                    [
                        html.H3(
                            "Menu",
                            Class="offcanvas-title",
                        ),
                        html.BUTTON(
                            type="button",
                            Class="btn-close",
                            data_bs_dismiss="offcanvas",
                            aria_label="Close",
                        ),
                    ],
                    Class="offcanvas-header",
                ),
                html.DIV(
                    [
                        # html.DIV(
                        #     "Some text as placeholder. "
                        #     "In real life you can have the elements you have chosen. "
                        #     "Like, text, images, lists, etc."
                        # ),
                        html.DIV(
                            sum(
                                page_link_list,
                                start=html.HR(),
                            ),
                            Class="list-group list-group-flush",
                        ),
                    ],
                    Class="offcanvas-body",
                ),
            ],
            Class="offcanvas offcanvas-start",
            id="offcanvas_menu",
            aria_labelledby="offcanvas_menu_label",
        )

        # Navbar
        document <= html.NAV(
            html.DIV(
                html.A(
                    [
                        html.IMG(
                            src="assets/img/lq_32x32.png",
                            # src="assets/img/logo_32x32.png",
                        ),
                        html.SPAN("Sokoban", Class="navbar-text text-white p-2"),
                    ],
                    Class="navbar-brand",
                    data_bs_toggle="offcanvas",
                    href="#offcanvas_menu",
                ),
                Class="container",
            ),
            Class="navbar navbar-expand-sm bg-primary opacity-90 shadow",
        )

        # Attach page container
        document <= self.html_page_container

    def build_page_home(self):
        ################################
        # The start of the main functional App UI.

        # Game state
        self.game = None
        self.game_solved = False
        self.game_moving_player = False
        self.home_key_enabled = True
        self.tile_size = 24
        self.default_canvas_width = self.tile_size * 8
        self.default_canvas_height = self.tile_size * 8

        # Dropdown for collection selection
        self.collections_path = "assets/collections/"
        self.collection_select = html.SELECT(Class="form-select")

        COLLECTION_LIST_URL = "assets/collections/collection_list.txt"
        self.init_collection_list(open(COLLECTION_LIST_URL).read())

        # Dropdown for level selection
        self.level_select = html.SELECT(Class="form-select mt-1")
        self.level_select <= html.OPTION(
            "Select Level", value="", disabled=True, selected=True
        )

        # Canvas for game display
        self.canvas = html.CANVAS(
            id="sokoban-canvas",
            Class="d-block mx-auto border mt-3",
            width=str(self.default_canvas_width),
            height=str(self.default_canvas_height),
        )

        # Bind events
        self.collection_select.bind("change", self.init_level_list)
        self.level_select.bind("change", self.load_level)
        document.bind("keydown", self.on_key)
        self.canvas.bind("click", self.on_mouse_click)

        # Button group
        # full-screen flex container, centered
        btn_group_container = html.DIV(
            Class="d-flex justify-content-center align-items-center mt-3"
        )

        # horizontal wrapper: [ arrows-T ] [   UNDO   ]
        wrapper = html.DIV(Class="d-flex align-items-center")

        # build the T-shaped arrow group with flex utilities + gap
        arrows = html.DIV(Class="d-flex flex-column align-items-center gap-2")

        # Buttons
        btn_up = html.BUTTON("^(W)", Class="btn btn-primary")
        btn_left = html.BUTTON("<(A)", Class="btn btn-primary")
        btn_right = html.BUTTON(">(D)", Class="btn btn-primary")
        btn_down = html.BUTTON("v(S)", Class="btn btn-primary")
        btn_undo = html.BUTTON("Undo(U)", Class="btn btn-secondary ms-4")

        btn_up.bind(
            "click", (lambda ev, direction=Sokoban.UP: self.on_direction(ev, direction))
        )
        btn_left.bind(
            "click",
            (lambda ev, direction=Sokoban.LEFT: self.on_direction(ev, direction)),
        )
        btn_right.bind(
            "click",
            (lambda ev, direction=Sokoban.RIGHT: self.on_direction(ev, direction)),
        )
        btn_down.bind(
            "click",
            (lambda ev, direction=Sokoban.DOWN: self.on_direction(ev, direction)),
        )
        btn_undo.bind("click", self.on_undo)

        # UP
        arrows <= btn_up
        # middle row: LEFT and RIGHT, spaced
        middle = html.DIV(Class="d-flex gap-4")
        middle <= btn_left
        middle <= btn_right
        arrows <= middle
        # DOWN
        arrows <= btn_down
        # put arrow-group into the wrapper
        wrapper <= arrows
        # UNDO to the right, with margin
        wrapper <= btn_undo
        # assemble
        btn_group_container <= wrapper

        # Assemble home page
        html_page_home = html.DIV(
            [
                # html.H1("Sokoban", Class="text-center mb-3"),
                self.collection_select,
                self.level_select,
                self.canvas,
                btn_group_container,
            ],
            Class="m-3 text-center",
        )

        # The end of the main functional App UI
        ################################

        return html_page_home

    def init_collection_list(self, text):
        self.collection_select <= html.OPTION(
            "Select Collection", value="", disabled=True, selected=True
        )
        for item in text.split("\n"):
            file_name = item.strip()
            file_path = self.collections_path + file_name
            file_name_stem = list(file_name.split("."))[0]
            self.collection_select <= html.OPTION(f"{file_name_stem}", value=file_path)

    def init_level_select(self, text):
        self.collection_text = text

        self.level_select.clear()
        self.level_select <= html.OPTION(
            "Select Level", value="", disabled=True, selected=True
        )

        parser = window.DOMParser.new()
        xml_doc = parser.parseFromString(text, "text/xml")
        for item in xml_doc.getElementsByTagName("Level"):
            item_id = item.getAttribute("Id")
            self.level_select <= html.OPTION(f"{item_id}", value=item_id)

    def init_level_list(self, ev):
        url = ev.target.value
        self.init_level_select(open(url).read())
        self.init_game(None)

    def draw_game(self):
        if self.game is None:
            self.canvas.setAttribute("width", str(self.default_canvas_width))
            self.canvas.setAttribute("height", str(self.default_canvas_height))
            ctx = self.canvas.getContext("2d")
            ctx.fillStyle = "White"
            ctx.fillRect(0, 0, self.canvas.width, self.canvas.height)
            return

        rows = self.game.nrow
        cols = self.game.ncol
        # Set internal resolution
        self.canvas.setAttribute("width", str(cols * self.tile_size))
        self.canvas.setAttribute("height", str(rows * self.tile_size))

        ctx = self.canvas.getContext("2d")

        # Space
        ctx.fillStyle = "Azure"
        ctx.fillRect(0, 0, self.canvas.width, self.canvas.height)

        # Walls
        for wall in self.game.walls:
            x = wall.c * self.tile_size
            y = wall.r * self.tile_size
            ctx.fillStyle = "SteelBlue"
            ctx.fillRect(x, y, self.tile_size, self.tile_size)

        # Goals
        for goal in self.game.goals:
            x = goal.c * self.tile_size
            y = goal.r * self.tile_size
            ctx.fillStyle = "Silver"
            ctx.fillRect(x, y, self.tile_size, self.tile_size)
            ctx.fillStyle = "Gray"
            ctx.fillRect(x + 1, y + 1, self.tile_size - 2, self.tile_size - 2)

        # Boxes
        for box in self.game.boxes:
            x = box.c * self.tile_size
            y = box.r * self.tile_size
            # ctx.fillStyle = "Gold"
            # ctx.fillRect(
            #     x + self.tile_size // 8,
            #     y + self.tile_size // 8,
            #     self.tile_size // 8 * 6,
            #     self.tile_size // 8 * 6,
            # )
            ctx.strokeStyle = "Gold"
            ctx.lineWidth = self.tile_size // 8 * 2
            ctx.strokeRect(
                x + self.tile_size // 8 * 2,
                y + self.tile_size // 8 * 2,
                self.tile_size // 8 * 4,
                self.tile_size // 8 * 4,
            )

        # Player
        x = self.game.player.c * self.tile_size + self.tile_size // 2
        y = self.game.player.r * self.tile_size + self.tile_size // 2
        ctx.fillStyle = "Tomato"
        ctx.beginPath()
        ctx.arc(x, y, self.tile_size // 8 * 3, 0, 2 * math.pi)
        ctx.fill()

        # Text
        ctx.font = "16px Arial"
        ctx.fillStyle = "Black"
        ctx.textAlign = "start"
        ctx.textBaseline = "top"
        ctx.fillText(f"m:{self.game.nmove} p:{self.game.npush}", 2, 2)

    def init_game(self, level_text):
        if not level_text:
            self.game = None
        else:
            self.game = Sokoban(level_text, undo_limit=None)

        self.game_solved = False
        self.game_moving_player = False
        self.draw_game()

    def load_level(self, ev):
        level_id = ev.target.value
        parser = window.DOMParser.new()
        xml_doc = parser.parseFromString(self.collection_text, "text/xml")
        for level in xml_doc.getElementsByTagName("Level"):
            if level.getAttribute("Id") == level_id:
                level_text = "\n".join(
                    [item.textContent for item in level.getElementsByTagName("L")]
                )
                self.init_game(level_text)
                break

    def can_take_player_action(self):
        if (
            self.home_key_enabled
            and self.game
            and (not self.game_solved)
            and (not self.game_moving_player)
        ):
            return True

        return False

    def show_solved_alert(self):
        alert(
            "\n".join(
                [
                    "This level is solved!",
                    f"Move(s): {self.game.nmove}",
                    f"Push(es): {self.game.npush}",
                ]
            )
        )

    def on_key(self, ev):
        if not self.can_take_player_action():
            return

        key_code = ev.code
        direction = None
        if key_code == "KeyW":
            direction = Sokoban.UP
        elif key_code == "KeyS":
            direction = Sokoban.DOWN
        elif key_code == "KeyA":
            direction = Sokoban.LEFT
        elif key_code == "KeyD":
            direction = Sokoban.RIGHT
        elif key_code == "KeyU":
            if self.game.undo():
                self.draw_game()

        if direction and self.game.move(direction):
            self.draw_game()
            if self.game.is_solved():
                self.game_solved = True
                timer.set_timeout(self.show_solved_alert, 200)

    def get_pos_from_mouse_click(self, ev):
        rect = self.canvas.getBoundingClientRect()
        r = int((ev.clientY - rect.top) // self.tile_size)
        c = int((ev.clientX - rect.left) // self.tile_size)
        return SokobanVector(r, c)

    # def on_mouse_click(self, ev):
    #     if not self.can_take_player_action():
    #         return

    #     rect = self.canvas.getBoundingClientRect()
    #     # Global coordinates of the mouse click
    #     mouse_x = ev.clientX - rect.left
    #     mouse_y = ev.clientY - rect.top
    #     # Global coordinates of the center of the player
    #     player_center_x = self.game.player.c * self.tile_size + self.tile_size // 2
    #     # Coordinates of the mouse click relative to center of the player
    #     player_center_y = self.game.player.r * self.tile_size + self.tile_size // 2
    #     x = mouse_x - player_center_x
    #     y = mouse_y - player_center_y

    #     direction = None
    #     if y <= -x and y <= x and y < -self.tile_size // 2:
    #         direction = Sokoban.UP
    #     elif y < -x and y > x and x < -self.tile_size // 2:
    #         direction = Sokoban.LEFT
    #     elif y >= -x and y >= x and y > self.tile_size // 2:
    #         direction = Sokoban.DOWN
    #     elif y > -x and y < x and x > self.tile_size // 2:
    #         direction = Sokoban.RIGHT

    #     if direction and self.game.move(direction):
    #         self.draw_game()
    #         if self.game.is_solved():
    #             self.game_solved = True
    #             timer.set_timeout((lambda: alert("This level is solved!")), 200)

    def move_along_path(self, path):
        def step():
            if self.game is None:
                return

            if path:
                self.game_moving_player = True
                next_pos = path.pop(0)
                self.game.move(next_pos - self.game.player)
                self.draw_game()
                timer.set_timeout(step, 100)
            else:
                self.game_moving_player = False

        step()

    def on_mouse_click(self, ev):
        if not self.can_take_player_action():
            return

        target_pos = self.get_pos_from_mouse_click(ev)
        direction = target_pos - self.game.player
        if (direction) in Sokoban.DIRECTION_SET:
            if self.game.move(direction):
                self.draw_game()
                if self.game.is_solved():
                    self.game_solved = True
                    timer.set_timeout(self.show_solved_alert, 200)
        else:
            path = self.game.find_path(target_pos)
            if path:
                self.move_along_path(path)

    def on_direction(self, ev, direction):
        if not self.can_take_player_action():
            return

        self.game.move(direction)
        self.draw_game()
        if self.game.is_solved():
            self.game_solved = True
            timer.set_timeout(self.show_solved_alert, 200)

    def on_undo(self, ev):
        if not self.can_take_player_action():
            return

        self.game.undo()
        self.draw_game()

    def build_page_about(self):
        ABOUT_PAGE_MD_URL = "assets/md/about_page.md"

        md_html, scripts = markdown.mark(open(ABOUT_PAGE_MD_URL).read())

        html_page_about = html.DIV(
            # Class="d-flex m-3 justify-content-center",
            Class="m-3",
        )
        html_page_about.html = md_html

        return html_page_about

    def build_page_tools(self):
        self.interpreter_button = html.BUTTON(
            "Brython Interpreter",
            type="button",
            Class="btn btn-outline-primary",
        )
        self.interpreter_button.bind("click", self.start_interpreter)
        html_page_tools = html.DIV(
            self.interpreter_button,
            Class="d-flex m-3 justify-content-center",
        )

        return html_page_tools

    def offcanvas_link_action(self, event, page_num=None):
        self.html_page_container.clear()
        self.html_page_container <= self.page_list[page_num]
        if page_num == 0:
            self.home_key_enabled = True
        else:
            self.home_key_enabled = False

    def start_interpreter(self, event):
        self.interpreter = Interpreter(globals=globals(), rows=50, cols=100)


if __name__ == "__main__":
    webapp = WebApp()
