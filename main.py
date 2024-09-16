import numbers
import json
import re
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Rule, Button, Label, Static, Input, Header, Footer, ListView, ListItem, ContentSwitcher, RadioSet, RadioButton
from textual.widget import Widget
from textual.containers import  Vertical, VerticalScroll, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.events import ScreenSuspend, Blur
from textual import events
from persistence import delete_data, get_data, save_data, load_data, Model
from rich.text import Text

meta = None
with open("metadata.json", "r") as file:
    meta = json.load(file)

flow_state = {
    "crop": {},
    "shape": ""
}

model = Model(None, "", "", 0.0, 0.0, 0.0, "", 0.0)

def reset_state():
    global flow_state
    flow_state = {
        "crop": {},
        "shape": ""
    }
    global model
    model = Model(None, "", "", 0.0, 0.0, 0.0, "", 0.0)

class ShapeList(ListView):
    
    def compose(self) -> ComposeResult:
        for shape in meta["shapes"]:
            yield ListItem(Label(shape["name"]), name=shape["name"])
    
class CropList(ListView):
    
    def compose(self) -> ComposeResult:
        for crop in meta["crops"]:
            yield ListItem(Label(crop["name"]), name=crop["name"])

class AreaDisplay(Widget):
    total_area: reactive[float] = reactive(0)
    management_area: reactive[float] = reactive(0)
    usable_area: reactive[float] = reactive(0)
    unit: str = ""

    def __init__(self,shape, **kwargs):
        self.unit = shape["unit"]
        super().__init__(**kwargs)
        
    def render(self) -> str:
        
        return f"""
Area Total: {self.total_area} {self.unit}
Area de manejo: {self.management_area} {self.unit}
Area util: {self.usable_area} {self.unit}
        """

class InputForm(Screen):
    
    crop: dict | None = None
    selected_input: dict | None = None
    all_inputs: dict | None = {}
    def __init__(self, crop):
        self.crop = crop
        super().__init__(id=f"input-form-{hash(crop['name'])}")
        
    def compose(self) -> ComposeResult:
        
        with RadioSet(id="focus_me"):
            for i in range(len(self.crop["inputs"])):
                input = self.crop["inputs"][i]
                type = input["type"]
                input_amount = model.usable_area * (input["ml_by_hectare"]* 0.0001)
                input_amount = input_amount/1000
                name = f"{input["name"]} - {type} - {input_amount} L"
                self.all_inputs[i] = [input["name"], input_amount]
                yield RadioButton(name, name=input["name"])
                
            yield Rule()
            yield Horizontal(
                Button("✓ Salvar", name="ok", variant="success", disabled=True),
                Label(" "),
                Button("✕ Cancelar", name="cancel", variant="error"),
                classes="dock-btm-mh")
    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        model.input = self.all_inputs[event.index][0]
        model.input_amount = self.all_inputs[event.index][1]
        for bt in self.query(Button):
            if bt.name == "ok":
                bt.disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_name = event.button.name
        if btn_name == "ok":
            global model
            new = save_data(model)
            self.app.notify(f"Registro {new.id} salvo com sucesso")
            reset_state()
            while len(self.app.screen_stack) > 1:
                self.app.pop_screen()
        elif btn_name == "cancel":
            self.app.pop_screen()  
        
class ShapeForm(Widget):
    shape: dict | None = None
    
    def __init__(self, shape):
        self.shape = shape
        super().__init__(id=f"shape-form-{hash(shape['name'])}")
        
    def gen_form(self):
        dim = self.shape["dimensions"]
        yield Label(f"Forneça as dimensões da area de plantio")
        yield Rule()
        for d in dim:
            yield Label(f"{d["name"]} ({d["unit"]})")
            yield Input(placeholder=f"{d["name"]} ({d["unit"]})", name=d["symbol"], type="number")
        
        yield Label("")
        yield Label(f"Forneça as dimensões da area de manejo")
        yield Rule()
        yield Label(f"Ruas/Linhas (m)")
        yield Input(placeholder="Ruas/Linhas (m)", name="_rows")
        yield Label(f"Largura (m)")
        yield Input(placeholder="Largura (m)", name="rows_width")
        yield Label(f"Comprimento (m)")
        yield Input(placeholder="Comprimento (m)", name="rows_length")
        yield Rule()

        
    def compose(self) -> ComposeResult:
        els: list[Widget] = []
        for el in self.gen_form():
            els.append(el)
            
        yield VerticalScroll(*els, classes="test")
        yield AreaDisplay(self.shape, classes="area-display")
        yield Horizontal(
            Button("✓ Ok", name="ok", variant="primary" , disabled=True),
            Label(" "),
            Button("✕ Cancelar", name="cancel", variant="error"),
            classes="dock-btm-mh"
            )
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_name = event.button.name
        if btn_name == "ok":
            model.shape = self.shape["name"]
            area_display = self.query_one(AreaDisplay)
            model.total_area = area_display.total_area
            model.management_area = area_display.management_area
            model.usable_area = area_display.usable_area
            self.app.push_screen(InputForm(flow_state["crop"]))
        elif btn_name == "cancel":
            self.app.pop_screen()
    
    def on_input_changed(self, event: Input.Changed) -> None:
        script = self.shape["eval"]
        management_area_script = "rows_length * rows_width * _rows"
        for el in self.query(Input):
            value = el.value
            if not value or re.match(r'-(\d+)?', value):
                value = '0'
            script = re.sub(r'\b' + el.name + r'\b', value, script)
            management_area_script = re.sub(r'\b' + el.name + r'\b', value, management_area_script)
            
        display = self.query_one(AreaDisplay)
        try:
            total_result = eval(script)
            display.total_area = total_result
            model.total_area = display.total_area
            
            management_result = eval(management_area_script) 
            display.management_area = management_result
            model.management_area = display.management_area
            
            display.usable_area = total_result - management_result
            model.usable_area = display.usable_area
            for bt in self.query(Button):
                if bt.name == "ok":
                    bt.disabled = model.total_area <= 0 or model.usable_area < 0
        except Exception as e:
            print(e)
        

class InsertFlow(Screen):
    def compose(self) -> ComposeResult:
        reset_state()
        with ContentSwitcher(initial="crop-list") as switcher:  
            yield VerticalScroll(
                *[Static("Selecione uma Cultura"),
                CropList()],
                id="crop-list")
           
            
            with VerticalScroll(id="shape-list"):
                yield Static("Forma da area de plantio")
                yield ShapeList()
                    
            for shape in meta["shapes"]:
                yield ShapeForm(shape)
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if not flow_state["crop"]:
            selected_crop = next(crop for crop in meta["crops"] if crop["name"] == event.item.name)
            flow_state["crop"] = selected_crop
            model.crop = selected_crop["name"]
            self.query_one(ContentSwitcher).current = "shape-list"
        elif not flow_state["shape"]:
            shape = next(shape for shape in meta["shapes"] if shape["name"] == event.item.name)
            flow_state["shape"] = shape
            model.shape = shape["name"]
            self.query_one(ContentSwitcher).current = f"shape-form-{hash(shape["name"])}"
    
        
class ViewFlow(Screen):
    
    BINDINGS = [
        ("escape", "app.pop_screen", "Voltar/Sair"),
        ("e", "", "Editar"),
        ("enter", "", "Editar"),
        ("d", "", "Deletar"),
        ("delete", "", "Deletar"),
        ("backspace", "", "Deletar")
        ]
    HELP = "Pressione 'e' ou 'enter' para editar, 'd' ou 'delete' para deletar"
    
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()
        
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_columns("ID", "Cultura", "Forma", "Area Total (m²)", "Area de Manejo (m²)", "Area Util (m²)", "Insumo", "Quantidade (L/m²)")
        for d in load_data():
            
            row = [d.id, d.crop, d.shape, d.total_area, d.management_area, d.usable_area, d.input, d.input_amount]

            for i in range(len(row)):
                col = row[i]
                
                if isinstance(col, numbers.Integral):
                    continue
                if isinstance(col, numbers.Real):
                    row[i] = Text(f"{col:.2f}", justify="right")
            
            table.add_row(*row)
            
    def on_key(self, event: events.Key)-> None:
        match event.key:
            case "e" | "enter":
                table = self.query_one(DataTable)
                table_cursor_row = table.cursor_row
                table_cursor_col = table.cursor_column
                row = table.get_row_at(table.cursor_row)

                if not row:
                    return
                update_screen = UpdateScreen(row)
                def hook():
                    self.on_mount()
                    table = self.query_one(DataTable)
                    table.move_cursor(row=table_cursor_row, column=table_cursor_col)
                    
                update_screen.set_hook(hook)
                self.app.push_screen(update_screen)
            case "d" | "delete" | "backspace":
                table = self.query_one(DataTable)
                table_cursor_row = table.cursor_row
                row = table.get_row_at(table.cursor_row)
                if not row:
                    return
                delete_id = row[0]
                delete_data(id=delete_id)  
                self.notify(f"Registro {delete_id} deletado com sucesso")   
                self.on_mount()   

class UpdateScreen(Screen):
    id = None
    updating_model: Model = None
    hook: callable = None
    
    def __init__(self, row):
        self.id = row[0]
        self.updating_model = get_data(self.id)
        super().__init__(id=f"update-screen-{row[0]}")
    
    def compose(self) -> ComposeResult:
        yield Label("Atualizar Dados")
        yield Rule()
        yield Label("Area Total")
        yield Input(placeholder="Area Total", name="total_area",type="number", value=f"{self.updating_model.total_area}")
        yield Label("Area de Manejo")
        yield Input(placeholder="Area de Manejo", name="management_area",type="number", value=f"{self.updating_model.management_area}")
        yield Rule()
        yield Horizontal(
            Button("✓ Ok", name="ok", variant="primary"),
            Label(" "),
            Button("✕ Cancelar", name="cancel", variant="error"),
            classes="dock-btm-mh")
        
    def on_input_changed(self, event: Input.Changed) -> None:
        value = event.value
        if not value or re.match(r'-(\d+)?', value):
            value = '0'
        
        match event.input.name:
            case "total_area":
                self.updating_model.total_area = float(value)
            case "management_area":
                self.updating_model.management_area = float(value)
            case _:
                pass
        
    def set_hook(self, hook):
        self.hook = hook
        
    def on_screen_suspend(self, event: ScreenSuspend) -> None:
        self.hook()
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_name = event.button.name
        match btn_name:
            case "ok":
                usable_area = self.updating_model.usable_area
                new_usable_area = self.updating_model.total_area - self.updating_model.management_area
                input_amount = self.updating_model.input_amount
                new_input_amount = 0
                if input_amount == 0:
                    meta_crop = next(crop for crop in meta["crops"] if crop["name"] == self.updating_model.crop)
                    input = next(input for input in meta_crop["inputs"] if input["name"] == self.updating_model.input)
                    new_input_amount = new_usable_area * (input["ml_by_hectare"]* 0.0001)
                else:
                    new_input_amount = new_usable_area * (input_amount / usable_area)
                self.updating_model.usable_area = new_usable_area
                self.updating_model.input_amount = new_input_amount
                save_data(self.updating_model)
                self.app.pop_screen()
            case "cancel":
                self.app.pop_screen()
              
        
class MainMenu(Screen):
    
    def compose(self) -> ComposeResult:

        yield Vertical(
            Static("[bold]Menu Principal", classes="menu-header"),
            ListView(* [
                ListItem(Label("+ Inserir Novos Dados de Plantio"), id="insert"),
                ListItem(Label("⌖ Consultar"), id="view"),
            ]),
        )
        yield Button("↵ Sair", id="exit", variant="error", classes="dock-btm")
        
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "insert":
            self.app.push_screen(InsertFlow())
        elif event.item.id == "view":
            self.app.push_screen(ViewFlow())
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "insert":
            self.app.push_screen(InsertFlow())
        elif button_id == "view":
            self.mount(Static("view"))
        elif button_id == "exit":
            self.app.exit()
    
class CropSelectionApp(App):
    CSS_PATH = "style.css"
    BINDINGS = [("escape", "app.pop_screen", "Voltar/Sair")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield MainMenu()
        yield Footer()



if __name__ == "__main__":
    CropSelectionApp().run()
