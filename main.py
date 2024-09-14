from logging import log
from textual.app import App, ComposeResult
from textual.events import Event
from textual.widgets import Rule, Button, Label, Static, Input, Header, Footer, ListView, ListItem, ContentSwitcher, RadioSet, RadioButton
from textual.widget import Widget
from textual.containers import  Vertical, VerticalScroll, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.events import ScreenSuspend
import json
from service import calculate_area, calculate_input_needed
from persistence import save_data, load_paginated_data, Model
import re


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
                Button("✕ Cancel", name="cancel", variant="error"))
    
    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        model.input = self.all_inputs[event.index][0]
        model.input_amount = self.all_inputs[event.index][1]
        for bt in self.query(Button):
            if bt.name == "ok":
                bt.disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_name = event.button.name
        if btn_name == "ok":
            self.app.pop_screen()
            global model
            save_data(model)
            reset_state()
            self.app.pop_screen() 
        elif btn_name == "cancel":
            self.app.pop_screen()  
        
class ShapeForm(VerticalScroll):
    shape: dict | None = None
    
    def __init__(self, shape):
        self.shape = shape
        super().__init__(id=f"shape-form-{hash(shape['name'])}")
        
    def compose(self) -> ComposeResult:
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
        yield AreaDisplay(self.shape)
        yield Rule()
        yield Horizontal(
            Button("✓ Ok", name="ok", variant="primary" , disabled=True),
            Label(" "),
            Button("✕ Cancel", name="cancel", variant="error"))
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_name = event.button.name
        if btn_name == "ok":
            model.shape = self.shape["name"]
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
    
    def on_screen_suspend(self, event: ScreenSuspend) -> None:
        reset_state()


class MainMenu(Screen):
    
    def compose(self) -> ComposeResult:

        yield Vertical(
            Static("[bold]Menu Principal", classes="menu-header"),
            ListView(* [
                ListItem(Label("+ Inserir Novos Dados de Plantio"), id="insert"),
                ListItem(Label("⌖ Consultar"), id="view"),
            ]),
            Button("↵ Sair", id="exit", variant="error")
        )
        
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "insert":
            self.app.push_screen(InsertFlow())
        elif event.item.name == "view":
              self.mount(Static("view"))
        
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
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield MainMenu()
        yield Footer()



if __name__ == "__main__":
    CropSelectionApp().run()
