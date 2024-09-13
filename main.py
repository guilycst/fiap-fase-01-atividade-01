from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input, Header, Footer, ListView, ListItem
from textual.containers import Container, Vertical
from textual.reactive import reactive
import json
from service import calculate_area, calculate_input_needed
from persistence import save_data, load_paginated_data


class CropSelectionApp(App):
    selected_crop = reactive(None)
    selected_shape = reactive(None)
    selected_product = reactive(None)
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Static("[bold]Menu Principal", classes="menu-header"),
            Button("Inserir Novos Dados de Plantio", id="insert", variant="primary"),
            Button("Visualizar Dados Armazenados", id="view", variant="primary"),
            Button("Sair", id="exit", variant="error")
        )
    
    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "insert":
            await self.insert_data_flow()
        elif button_id == "view":
            await self.view_data()
        elif button_id == "exit":
            self.exit()

    async def insert_data_flow(self):
        # Seleção da Cultura
        await self.select_crop()

        # Seleção da Forma Geométrica
        await self.select_shape()

        # Inserção das Dimensões
        await self.input_dimensions()

        # Seleção do Insumo
        await self.select_product()

        # Calculo de insumos e salvamento
        await self.calculate_and_save_data()

    async def select_crop(self):
        self.clear()
        with open("crops.json", "r") as file:
            crops = json.load(file)

        yield Static("Selecione uma Cultura")
        crop_list = ListView(*[ListItem(crop["name"]) for crop in crops])
        self.mount(crop_list)

        crop_list.action_select_cursor = self.handle_crop_selection
        

    def handle_crop_selection(self):
        with open("crops.json", "r") as file:
            crops = json.load(file)
        event = self.Selected
        selected_name = event.item.label
        self.selected_crop = next(crop for crop in crops if crop["name"] == selected_name)
        self.clear()

    async def select_shape(self):
        if not self.selected_crop:
            return
        self.clear()
        yield Static("Selecione a Forma Geométrica")
        shapes = self.selected_crop["shapes"]
        shape_list = ListView(*[ListItem(shape) for shape in shapes])
        self.mount(shape_list)
        shape_list.on_click = self.handle_shape_selection

    def handle_shape_selection(self, event: ListItem):
        self.selected_shape = event.item.label
        self.clear()

    async def input_dimensions(self):
        if not self.selected_shape:
            return
        self.clear()
        yield Static("Insira as Dimensões")
        self.length_input = Input(placeholder="Comprimento (em metros)")
        self.mount(self.length_input)
        if self.selected_shape == "Retângulo":
            self.width_input = Input(placeholder="Largura (em metros)")
            self.mount(self.width_input)
        self.rows_input = Input(placeholder="Número de Ruas")
        self.mount(self.rows_input)

    async def select_product(self):
        if not self.selected_crop:
            return
        self.clear()
        yield Static("Selecione um Insumo")
        products = self.selected_crop["products"]
        product_list = ListView(*[ListItem(product["name"]) for product in products])
        self.mount(product_list)
        product_list.on_click = self.handle_product_selection

    def handle_product_selection(self, event: ListItem):
        products = self.selected_crop["products"]
        self.selected_product = next(product for product in products if product["name"] == event.item.label)
        self.clear()

    async def calculate_and_save_data(self):
        length = float(self.length_input.value)
        width = float(self.width_input.value) if self.selected_shape == "Retângulo" else None
        rows = int(self.rows_input.value)

        total_area, usable_area = calculate_area(self.selected_shape, {"length": length, "width": width, "rows": rows})
        input_needed = calculate_input_needed(usable_area, self.selected_product["ml_by_hectare"])

        save_data(self.selected_crop["name"], self.selected_shape, total_area, usable_area, self.selected_product["name"], input_needed)
        self.clear()
        yield Static(f"Dados de plantio salvos com sucesso!\nCultura: {self.selected_crop['name']}\nInsumo: {self.selected_product['name']}\nQuantidade: {input_needed} ml")

    async def view_data(self):
        self.clear()
        yield Static("[bold]Dados Armazenados")
        data = load_paginated_data(page_size=10)
        for record in data:
            yield Static(f"Cultura: {record[1]}, Forma: {record[2]}, Área Útil: {record[4]} ha, Insumo: {record[5]}, Quantidade: {record[6]} ml")


if __name__ == "__main__":
    CropSelectionApp().run()
