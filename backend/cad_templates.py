# Templates CAD simples pour formes de base
# Ces templates fonctionnent à 100% avec build123d

TEMPLATES = {
    "cube": """from build123d import *

# Cube de {size}mm
with BuildPart() as p:
    Box({size}, {size}, {size})

result_part = p.part
export_stl(result_part, r'{output_path}')
""",
    
    "box": """from build123d import *

# Boîte de {width}x{depth}x{height}mm
with BuildPart() as p:
    Box({width}, {depth}, {height})

result_part = p.part
export_stl(result_part, r'{output_path}')
""",
    
    "cylinder": """from build123d import *

# Cylindre rayon {radius}mm, hauteur {height}mm
with BuildPart() as p:
    Cylinder(radius={radius}, height={height})

result_part = p.part
export_stl(result_part, r'{output_path}')
""",
    
    "sphere": """from build123d import *

# Sphère rayon {radius}mm
with BuildPart() as p:
    Sphere(radius={radius})

result_part = p.part
export_stl(result_part, r'{output_path}')
""",
    
    "cone": """from build123d import *

# Cône rayon {radius}mm, hauteur {height}mm
with BuildPart() as p:
    Cone(bottom_radius={radius}, top_radius=0, height={height})

result_part = p.part
export_stl(result_part, r'{output_path}')
"""
}

def parse_simple_shape(prompt):
    """Parse les demandes simples et retourne le template + params"""
    prompt_lower = prompt.lower()
    
    # Extraire les dimensions
    import re
    numbers = re.findall(r'\d+(?:\.\d+)?', prompt)
    
    # Cube
    if 'cube' in prompt_lower:
        size = float(numbers[0]) if numbers else 10
        return 'cube', {'size': size}
    
    # Boîte/Box
    if 'boite' in prompt_lower or 'box' in prompt_lower or 'rectangle' in prompt_lower:
        if len(numbers) >= 3:
            return 'box', {'width': float(numbers[0]), 'depth': float(numbers[1]), 'height': float(numbers[2])}
        elif len(numbers) == 1:
            size = float(numbers[0])
            return 'box', {'width': size, 'depth': size, 'height': size}
    
    # Cylindre
    if 'cylindre' in prompt_lower or 'cylinder' in prompt_lower:
        if len(numbers) >= 2:
            return 'cylinder', {'radius': float(numbers[0]), 'height': float(numbers[1])}
        elif len(numbers) == 1:
            size = float(numbers[0])
            return 'cylinder', {'radius': size/2, 'height': size}
    
    # Sphère
    if 'sphere' in prompt_lower or 'sphère' in prompt_lower or 'boule' in prompt_lower:
        radius = float(numbers[0])/2 if numbers else 5
        return 'sphere', {'radius': radius}
    
    # Cône
    if 'cone' in prompt_lower or 'cône' in prompt_lower:
        if len(numbers) >= 2:
            return 'cone', {'radius': float(numbers[0]), 'height': float(numbers[1])}
        elif len(numbers) == 1:
            size = float(numbers[0])
            return 'cone', {'radius': size/2, 'height': size}
    
    return None, None
