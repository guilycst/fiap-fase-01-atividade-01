# Função para calcular a área total e a área útil
def calculate_area(shape, dimensions):
    if shape == "Quadrado":
        total_area = dimensions["length"] ** 2
    elif shape == "Retângulo":
        total_area = dimensions["length"] * dimensions["width"]
    
    road_area = dimensions["rows"] * (dimensions["length"] + dimensions.get("width", dimensions["length"]))
    usable_area = total_area - road_area
    
    return total_area, usable_area

# Função para calcular a quantidade de insumo necessária
def calculate_input_needed(usable_area, ml_by_hectare):
    return usable_area * (ml_by_hectare * 0.0001)
