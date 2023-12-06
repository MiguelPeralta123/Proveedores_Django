import os
import csv

DEFAULT_LIST = [
    ('', ' Seleccione una opción'),
]

EMPRESA_LIST = [
    ('', ' Seleccione una opción'),
    ('Sonorg - Tago - Wichita', 'Sonorg - Tago - Wichita'),
    ('Moonrise - Wellin', 'Moonrise - Wellin'),
    ('Sonorg - Tago - Wichita - Moonrise - Wellin', 'Sonorg - Tago - Wichita - Moonrise - Wellin'),
]

EMPRESA_MIGRACION_ORIGEN_LIST = [
    ('', ' Seleccione una opción'),
    ('Datamine Sonorg', 'Datamine Sonorg'),
    ('Datamine Tago', 'Datamine Tago'),
    ('Datamine Wichita', 'Datamine Wichita'),
    ('Datamine Moonrise', 'Datamine Moonrise'),
    ('Datamine Wellin', 'Datamine Wellin'),
]

EMPRESA_MIGRACION_DESTINO_LIST = [
    ('', ' Seleccione una opción'),
    ('Sonorg', 'Sonorg'),
    ('Tago', 'Tago'),
    ('Wichita', 'Wichita'),
    ('Moonrise', 'Moonrise'),
    ('Wellin', 'Wellin'),
]

TIPO_ALTA_LIST = [
    ('', ' Seleccione una opción'),
    ('Almacén', 'Almacén'),
    ('Servicio', 'Servicio'),
]

subfamilia_csv_path = os.path.join('csv_files', 'catalogo_subfamilias.csv')
with open(subfamilia_csv_path, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skipping headers
    
    # Inicializa la lista que contendrá las tuplas
    SUBFAMILIA_LIST = [
        ('', ' Seleccione una opción')
    ]
    SUBFAMILIA_PRODUCTO_LIST = [
        ('', ' Seleccione una opción')
    ]
    SUBFAMILIA_SERVICIO_LIST = [
        ('', ' Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Agrega la tupla a la lista
        nombre = row[0]
        SUBFAMILIA_LIST.append((nombre, nombre))
        if int(row[1]) < 50:
            SUBFAMILIA_PRODUCTO_LIST.append((nombre, nombre))
        else:
            SUBFAMILIA_SERVICIO_LIST.append((nombre, nombre))

# Ordenar la lista alfabéticamente en función de las etiquetas
SUBFAMILIA_LIST = sorted(SUBFAMILIA_LIST, key=lambda item: item[1])
SUBFAMILIA_PRODUCTO_LIST = sorted(SUBFAMILIA_PRODUCTO_LIST, key=lambda item: item[1])
SUBFAMILIA_SERVICIO_LIST = sorted(SUBFAMILIA_SERVICIO_LIST, key=lambda item: item[1])

medida_um_csv_path = os.path.join('csv_files', 'catalogo_medida_um.csv')
with open(medida_um_csv_path, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skipping headers
    
    # Inicializa la lista que contendrá las tuplas
    MEDIDA_UM_LIST = [
        ('', ' Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        nombre = row[1]
        # Agrega la tupla a la lista
        MEDIDA_UM_LIST.append((nombre, nombre))
        
# Ordenar la lista alfabéticamente en función de las etiquetas
MEDIDA_UM_LIST = sorted(MEDIDA_UM_LIST, key=lambda item: item[1])

PORCENTAJE_IVA_LIST = [
    ('', ' Seleccione una opción'),
    ('No aplica', 'No aplica'),
    ('8%', '8%'),
    ('16%', '16%'),
]

catalogo_unidad_medida_csv_path = os.path.join('csv_files', 'catalogo_unidad_medida.csv')
with open(catalogo_unidad_medida_csv_path, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skipping headers
    
    # Inicializa la lista que contendrá las tuplas
    UNIDAD_MEDIDA_LIST = [
        ('', ' Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        nombre = row[1]
        # Agrega la tupla a la lista
        UNIDAD_MEDIDA_LIST.append((nombre, nombre))

# Ordenar la lista alfabéticamente en función de las etiquetas
UNIDAD_MEDIDA_LIST = sorted(UNIDAD_MEDIDA_LIST, key=lambda item: item[1])