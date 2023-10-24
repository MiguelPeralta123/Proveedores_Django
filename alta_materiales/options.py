import os
import csv

DEFAULT_LIST = [
    ('', 'Seleccione una opción'),
]

EMPRESA_LIST = [
    ('', 'Seleccione una opción'),
    ('Sonorg - Tago - Wichita', 'Sonorg - Tago - Wichita'),
    ('Moonrise - Wellin', 'Moonrise - Wellin'),
    ('Sonorg - Tago - Wichita - Moonrise - Wellin', 'Sonorg - Tago - Wichita - Moonrise - Wellin'),
]

EMPRESA_MIGRACION_LIST = [
    ('', 'Seleccione una opción'),
    ('Sonorg', 'Sonorg'),
    ('Tago', 'Tago'),
    ('Wichita', 'Wichita'),
    ('Moonrise', 'Moonrise'),
    ('Wellin', 'Wellin'),
]

TIPO_ALTA_LIST = [
    ('', 'Seleccione una opción'),
    ('Almacén', 'Almacén'),
    ('Servicio', 'Servicio'),
]

SUBFAMILIA_LIST = [
    ('', 'Seleccione una opción'),
    ('0101 - Semilla', '0101 - Semilla'),
    ('0201 - Material cultivo', '0201 - Material cultivo'),
    ('0301 - Orgánicos', '0301 - Orgánicos'),
    ('0302 - Inorgánicos', '0302 - Inorgánicos'),
    ('0303 - Orgánico-minerales', '0303 - Orgánico-minerales'),
    ('0304 - Aminoácidos, algas marinas y extractos húmicos', '0304 - Aminoácidos, algas marinas y extractos húmicos'),
    ('0306 - Composta', '0306 - Composta'),
    ('0401 - Insecticidas', '0401 - Insecticidas'),
    ('0402 - Herbicidas', '0402 - Herbicidas'),
    ('0403 - Fungicidas', '0403 - Fungicidas'),
    ('0404 - Bactericidas', '0404 - Bactericidas'),
    ('0405 - Acaricidas', '0405 - Acaricidas'),
    ('0406 - Nematicidas', '0406 - Nematicidas'),
    ('0407 - Rodenticidas', '0407 - Rodenticidas'),
    ('0408 - Fitorreguladores', '0408 - Fitorreguladores'),
    ('0409 - Adherentes, sulfactantes y buferizante', '0409 - Adherentes, sulfactantes y buferizante'),
    ('0501 - Microorganismos', '0501 - Microorganismos'),
    ('0502 - Alguicidas', '0502 - Alguicidas'),
    ('0503 - Feromonas y atrayentes', '0503 - Feromonas y atrayentes'),
    ('0504 - Mejoradores de suelo', '0504 - Mejoradores de suelo'),
    ('0505 - Control biológico', '0505 - Control biológico'),
    ('0506 - Medio de cultivo', '0506 - Medio de cultivo'),
    ('0507 - Materia orgánica', '0507 - Materia orgánica'),
    ('0508 - Coadyuvantes', '0508 - Coadyuvantes'),
    ('0509 - Químico-Inorgánico', '0509 - Químico-Inorgánico'),
    ('0510 - Químico-Orgánico', '0510 - Químico-Orgánico'),
    ('9008 - Insumos MR', '9008 - Insumos MR'),
    ('0601 - Cera y sanitizantes', '0601 - Cera y sanitizantes'),
    ('0701 - Caja', '0701 - Caja'),
    ('0702 - Consumibles empaque', '0702 - Consumibles empaque'),
    ('0703 - Bolsa', '0703 - Bolsa'),
    ('0704 - Embalaje', '0704 - Embalaje'),
    ('0705 - Etiqueta', '0705 - Etiqueta'),
    ('0706 - Etiqueta -Fair Trade', '0706 - Etiqueta -Fair Trade'),
    ('0707 - Etiqueta -Good Life', '0707 - Etiqueta -Good Life'),
    ('0708 - Etiqueta -Rico Fair Trade', '0708 - Etiqueta -Rico Fair Trade'),
    ('0709 - Etiqueta - Rico Fair', '0709 - Etiqueta - Rico Fair'),
    ('0710 - Etiqueta - Térmicas', '0710 - Etiqueta - Térmicas'),
    ('0711 - Etiqueta - Whole Trade', '0711 - Etiqueta - Whole Trade'),
    ('0801 - Combustibles', '0801 - Combustibles'),
    ('0802 - Gas', '0802 - Gas'),
    ('0901 - Fierros y acero', '0901 - Fierros y acero'),
    ('0902 - Herramientas', '0902 - Herramientas'),
    ('0903 - Material eléctrico', '0903 - Material eléctrico'),
    ('0904 - Material ferretero y tornillería', '0904 - Material ferretero y tornillería'),
    ('0905 - Materiales de construcción', '0905 - Materiales de construcción'),
    ('0906 - Mangueras y conexiones', '0906 - Mangueras y conexiones'),
    ('1001 - Seguridad e higiene', '1001 - Seguridad e higiene'),
    ('1101 - Consumibles y equipo de cómputo', '1101 - Consumibles y equipo de cómputo'),
    ('1201 - Llantas', '1201 - Llantas'),
    ('1202 - Mantenimiento y equipo (Filtros y refacciones)', '1202 - Mantenimiento y equipo (Filtros y refacciones)'),
    ('1203 - Lubricantes', '1203 - Lubricantes'),
    ('1301 - Laboratorio', '1301 - Laboratorio'),
    ('1401 - Mobiliario y equipo menor', '1401 - Mobiliario y equipo menor'),
    ('1402 - Papelería y artículos de oficina', '1402 - Papelería y artículos de oficina'),
    ('1501 - Deportes', '1501 - Deportes'),
    ('1502 - Artículos decoración, dormitorios e instalaciones', '1502 - Artículos decoración, dormitorios e instalaciones'),
    ('1503 - Uniformes', '1503 - Uniformes'),
    ('1504 - Empaque alimentos', '1504 - Empaque alimentos'),
    ('1505 - Abarrotes', '1505 - Abarrotes'),
    ('1601 - Medicamentos y materiales médicos', '1601 - Medicamentos y materiales médicos'),
    ('1801 - Inocuidad y limpieza', '1801 - Inocuidad y limpieza'),
    ('5000 - Fletes exportación', '5000 - Fletes exportación'),
    ('5001 - Flete nacional', '5001 - Flete nacional'),
    ('5002 - Paquetería', '5002 - Paquetería'),
    ('5100 - In&Out', '5100 - In&Out'),
    ('5101 - Gastos de exportación', '5101 - Gastos de exportación'),
    ('1701 - Artículos publicitarios', '1701 - Artículos publicitarios'),
    ('5200 - Marketing y publicidad', '5200 - Marketing y publicidad'),
    ('5300 - Rentas y arrendamiento', '5300 - Rentas y arrendamiento'),
    ('5400 - Transporte de personal', '5400 - Transporte de personal'),
    ('5500 - Mantenimiento', '5500 - Mantenimiento'),
    ('5600 - Seguros y fianzas', '5600 - Seguros y fianzas'),
    ('5700 - Asesorías', '5700 - Asesorías'),
    ('5701 - Honorarios', '5701 - Honorarios'),
    ('5800 - Servicios generales del Campo', '5800 - Servicios generales del Campo'),
    ('5900 - Servicios públicos', '5900 - Servicios públicos'),
    ('6000 - Servicios al personal', '6000 - Servicios al personal'),
    ('6100 - Servicios de comedor', '6100 - Servicios de comedor'),
    ('6200 - Gastos Administrativos', '6200 - Gastos Administrativos'),
    ('6300 - Plántula', '6300 - Plántula'),
    ('9001 - Equipo de cómputo', '9001 - Equipo de cómputo'),
    ('9002 - Maquinaria y Equipo', '9002 - Maquinaria y Equipo'),
    ('9003 - Equipo de Transporte', '9003 - Equipo de Transporte'),
    ('9004 - Mobiliario y Equipo de Oficina', '9004 - Mobiliario y Equipo de Oficina'),
    ('9005 - Licencias de Software', '9005 - Licencias de Software'),
    ('9006 - Proyectos / Construcciones en proceso', '9006 - Proyectos / Construcciones en proceso')
]

PORCENTAJE_IVA_LIST = [
    ('', 'Seleccione una opción'),
    ('0', '0'),
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
        ('', 'Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        codigo = row[0]
        nombre = row[1]
        
        # Crea la cadena de texto con el formato deseado
        formato = f'{codigo} - {nombre}'
        
        # Agrega la tupla a la lista
        UNIDAD_MEDIDA_LIST.append((formato, formato))
# Ordenar la lista alfabéticamente en función de las etiquetas
UNIDAD_MEDIDA_LIST = sorted(UNIDAD_MEDIDA_LIST, key=lambda item: item[1])


medida_um_csv_path = os.path.join('csv_files', 'medida_um.csv')
with open(medida_um_csv_path, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skipping headers
    
    # Inicializa la lista que contendrá las tuplas
    MEDIDA_UM_LIST = [
        ('', 'Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        codigo = row[0]
        nombre = row[1]
        
        # Crea la cadena de texto con el formato deseado
        formato = f'{codigo} - {nombre}'
        
        # Agrega la tupla a la lista
        MEDIDA_UM_LIST.append((formato, formato))
# Ordenar la lista alfabéticamente en función de las etiquetas
MEDIDA_UM_LIST = sorted(MEDIDA_UM_LIST, key=lambda item: item[1])