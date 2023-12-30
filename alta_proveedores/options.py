import os
import csv

EMPRESA_LIST = [
    ('', ' Seleccione una opción'),
    ('Sonorg - Tago - Wichita', 'Sonorg - Tago - Wichita'),
    ('Moonrise - Wellin', 'Moonrise - Wellin'),
    ('Sonorg - Tago - Wichita - Moonrise - Wellin', 'Sonorg - Tago - Wichita - Moonrise - Wellin'),
]

EMPRESA_MIGRACION_ORIGEN_LIST = [
    ('', ' Seleccione una opción'),
    ('Sonorg', 'Sonorg'),
    ('Moonrise', 'Moonrise'),
    ('Wellin', 'Wellin'),
]

EMPRESA_MIGRACION_DESTINO_LIST = [
    ('', ' Seleccione una opción'),
    ('Sonorg', 'Sonorg'),
    ('Moonrise', 'Moonrise'),
    ('Wellin', 'Wellin'),
]

TIPO_ALTA_LIST = [
    ('', ' Seleccione una opción'),
    ('Proveedor', 'Proveedor'),
    ('Cliente', 'Cliente'),
]

CONTRIBUYENTE_LIST = [
    ('', ' Seleccione una opción'),
    ('Persona física', 'Persona física'),
    ('Persona moral', 'Persona moral'),
]

csv_path_regimen_capital = os.path.join('csv_files', 'catalogo_regimen_capital.csv')
with open(csv_path_regimen_capital, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    
    # Inicializa la lista que contendrá las tuplas
    REGIMEN_CAPITAL_LIST = [
        ('', ' Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        clave = row[2]
        nombre = row[1]
        
        # Crea la cadena de texto con el formato deseado
        format = f'{clave} - {nombre}'
        
        # Agrega la tupla a la lista
        REGIMEN_CAPITAL_LIST.append((format, format))
# Ordenar la lista alfabéticamente en función de las etiquetas
REGIMEN_CAPITAL_LIST = sorted(REGIMEN_CAPITAL_LIST, key=lambda item: item[1])

REGIMEN_FISCAL_LIST = [
    ('', ' Seleccione una opción'),
    ('601 - General de Ley Personas Morales', '601 - General de Ley Personas Morales'),
    ('603 - Personas Morales con Fines no Lucrativos', '603 - Personas Morales con Fines no Lucrativos'),
    ('605 - Sueldos y Salarios e Ingresos Asimilados a Salarios', '605 - Sueldos y Salarios e Ingresos Asimilados a Salarios'),
    ('606 - Arrendamiento', '606 - Arrendamiento'),
    ('607 - Régimen de Enajenación o Adquisición de Bienes', '607 - Régimen de Enajenación o Adquisición de Bienes'),
    ('608 - Demás ingresos', '608 - Demás ingresos'),
    ('609 - Consolidación', '609 - Consolidación'),
    ('610 - Residentes Extranjero sin Establecimiento Permanente en Méx', '610 - Residentes Extranjero sin Establecimiento Permanente en Méx'),
    ('611 - Ingresos por Dividendos (socios y accionistas)', '611 - Ingresos por Dividendos (socios y accionistas)'),
    ('612 - Personas Físicas con Actividades Empresariales y Profesionales', '612 - Personas Físicas con Actividades Empresariales y Profesionales'),
    ('614 - Ingresos por intereses', '614 - Ingresos por intereses'),
    ('615 - Régimen de los ingresos por obtención de premios', '615 - Régimen de los ingresos por obtención de premios'),
    ('616 - Sin obligaciones fiscales', '616 - Sin obligaciones fiscales'),
    ('620 - Sociedades Cooperativas Producción optan por diferir ingresos', '620 - Sociedades Cooperativas Producción optan por diferir ingresos'),
    ('621 - Incorporación Fiscal', '621 - Incorporación Fiscal'),
    ('622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras', '622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
    ('623 - Opcional para Grupos de Sociedades', '623 - Opcional para Grupos de Sociedades'),
    ('624 - Coordinados', '624 - Coordinados'),
    ('626 - Régimen Simplificado de Confianza', '626 - Régimen Simplificado de Confianza'),
    ('628 - Hidrocarburos', '628 - Hidrocarburos'),
    ('629 - Regímenes Fiscales Preferentes y Empresas Multinacionales', '629 - Regímenes Fiscales Preferentes y Empresas Multinacionales'),
    ('630 - Enajenación de acciones en bolsa de valores', '630 - Enajenación de acciones en bolsa de valores'),
]

USO_CFDI_LIST = [
    ('', ' Seleccione una opción'),
    ('G01 - Adquisición de Mercancías', 'G01 - Adquisición de Mercancías'),
    ('G02 - Devoluciones', 'G02 - Devoluciones'),
    ('G03 - Gastos en general', 'G03 - Gastos en general'),
    ('I01 - Construcciones', 'I01 - Construcciones'),
    ('I02 - Mobiliario y equipo de oficina por inversiones', 'I02 - Mobiliario y equipo de oficina por inversiones'),
    ('I03 - Equipo de transporte', 'I03 - Equipo de transporte'),
    ('I04 - Equipo de computo y accesorios', 'I04 - Equipo de computo y accesorios'),
    ('I05 - Dados', 'I05 - Dados'),
    ('I06 - Comunicaciones telefónicas', 'I06 - Comunicaciones telefónicas'),
    ('I07 - Comunicaciones satelitales', 'I07 - Comunicaciones satelitales'),
    ('I08 - Otra maquinaria y equipo', 'I08 - Otra maquinaria y equipo'),
    ('D01 - Honorarios médicos', 'D01 - Honorarios médicos'),
    ('D02 - Gastos médicos por incapacidad o discapacidad', 'D02 - Gastos médicos por incapacidad o discapacidad'),
    ('D03 - Gastos funerales', 'D03 - Gastos funerales'),
    ('D04 - Donativos', 'D04 - Donativos'),
    ('D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)', 'D05 - Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
    ('D06 - Aportaciones voluntarias al SAR', 'D06 - Aportaciones voluntarias al SAR'),
    ('D07 - Primas por seguros de gastos médicos', 'D07 - Primas por seguros de gastos médicos'),
    ('D08 - Gastos de transportación escolar obligatoria', 'D08 - Gastos de transportación escolar obligatoria'),
    ('D09 - Depósitos en cuentas para el ahorro', 'D09 - Depósitos en cuentas para el ahorro'),
    ('D10 - Pagos por servicios educativos (colegiaturas)', 'D10 - Pagos por servicios educativos (colegiaturas)'),
    ('P01 - Por definir', 'P01 - Por definir'),
    ('CP01 - Pagos', 'CP01 - Pagos'),
    ('CN01 - Nomina', 'CN01 - Nomina'),
    ('S01 - Sin efectos fiscales', 'S01 - Sin efectos fiscales'),
]

csv_path_rubro = os.path.join('csv_files', 'catalogo_rubros.csv')
with open(csv_path_rubro, 'r') as csv_file:
    # Lee el archivo CSV
    csv_reader = csv.reader(csv_file)
    next(csv_reader) # Skipping headers
    
    # Inicializa la lista que contendrá las tuplas
    RUBRO_LIST = [
        ('', ' Seleccione una opción')
    ]
    
    # Itera sobre cada fila del archivo CSV
    for row in csv_reader:
        # Extrae la información necesaria de las columnas
        codigo = row[0]
        nombre = row[1]
        
        # Crea la cadena de texto con el formato deseado
        format = f'{codigo} - {nombre}'
        
        # Agrega la tupla a la lista
        RUBRO_LIST.append((format, format))
# Ordenar la lista alfabéticamente en función de las etiquetas
RUBRO_LIST = sorted(RUBRO_LIST, key=lambda item: item[1])

#RUBRO_LIST = [
#    ('', ' Seleccione una opción'),
#    ('Aduanas', 'Aduanas'),
#    ('Agronomía', 'Agronomía'),
#    ('Aseguradoras', 'Aseguradoras'),
#    ('Aviación', 'Aviación'),
#    ('Aviación', 'Aviación'),
#    ('Bebidas y tabaco', 'Bebidas y tabaco'),
#    ('Comercio electrónico', 'Comercio electrónico'),
#    ('Comercio general', 'Comercio general'),
#    ('Construcción', 'Construcción'),
#    ('Consultoría de sistemas', 'Consultoría de sistemas'),
#    ('Educación', 'Educación'),
#    ('Electrónica', 'Electrónica'),
#    ('Fletes', 'Fletes'),
#    ('Gobierno', 'Gobierno'),
#    ('Industria alimenticia', 'Industria alimenticia'),
#    ('Industria plástica-polietileno', 'Industria plástica-polietileno'),
#    ('Manufactura', 'Manufactura'),
#    ('Minería', 'Minería'),
#    ('Otro', 'Otro'),
#    ('Prensa', 'Prensa'),
#    ('Publicidad', 'Publicidad'),
#    ('Rentas', 'Rentas'),
#    ('Servicios administrativos', 'Servicios administrativos'),
#    ('Servicios de internet', 'Servicios de internet'),
#    ('Servicios financieros', 'Servicios financieros'),
#    ('Servicios públicos', 'Servicios públicos'),
#    ('Tecnología de la información', 'Tecnología de la información'),
#    ('Telecomunicaciones', 'Telecomunicaciones'),
#    ('Textil', 'Textil'),
#    ('Transporte y distribución', 'Transporte y distribución'),
#    ('Turismo', 'Turismo'),
#]
# Ordenar la lista alfabéticamente en función de las etiquetas
#RUBRO_LIST = sorted(RUBRO_LIST, key=lambda item: item[1])

TIPO_OPERACION_LIST = [
    ('', ' Seleccione una opción'),
    ('Bienes', 'Bienes'),
    ('Servicios', 'Servicios'),
]

TIPO_TERCERO_LIST = [
    ('', ' Seleccione una opción'),
    ('Extranjero', 'Extranjero'),
    ('Extranjero Relacionado', 'Extranjero Relacionado'),
    ('Global', 'Global'),
    ('Nacional', 'Nacional'),
    ('Nacional Relacionado', 'Nacional Relacionado'),
]

AGENTE_ADUANAL_LIST = [
    ('', ' Seleccione una opción'),
    ('Si', 'Si'),
    ('No', 'No'),
]

RETENCION_IVA_LIST = [
    ('', ' Seleccione una opción'),
    ('No aplica', 'No aplica'),
    ('3%', '3%'),
    ('4%', '4%'),
    ('6%', '6%'),
    ('8%', '8%'),
    ('2/3', '2/3'),
    ('16%', '16%'),
]

RETENCION_ISR_LIST = [
    ('', ' Seleccione una opción'),
    ('No aplica', 'No aplica'),
    ('1.25%', '1.25%'),
    ('10%', '10%'),
]

IVA_FRONTERA_LIST = [
    ('', ' Seleccione una opción'),
    ('No aplica', 'No aplica'),
    ('8%', '8%'),
    ('16%', '16%'),
]

BANCO_LIST = [
    ('', ' Seleccione una opción'),
    ('ABC Capital S.A.', 'ABC Capital S.A.'),
    ('Acciones y Valores Banamex S.A. de C.V.', 'Acciones y Valores Banamex S.A. de C.V.'),
    ('Actinver Casa de Bolsa S.A. de C.V.', 'Actinver Casa de Bolsa S.A. de C.V.'),
    ('Akala S.A. de C.V.', 'Akala S.A. de C.V.'),
    ('American Express Bank (México) S.A.', 'American Express Bank (México) S.A.'),
    ('B y B Casa de Cambio S.A. de C.V.', 'B y B Casa de Cambio S.A. de C.V.'),
    ('Banca Afirme S.A.', 'Banca Afirme S.A.'),
    ('Banca Mifel S.A.', 'Banca Mifel S.A.'),
    ('Banco Actinver S.A.', 'Banco Actinver S.A.'),
    ('Banco Ahorro Famsa S.A.', 'Banco Ahorro Famsa S.A.'),
    ('Banco Autofin México S.A.', 'Banco Autofin México S.A.'),
    ('Banco Azteca S.A.', 'Banco Azteca S.A.'),
    ('Banco Base S.A.', 'Banco Base S.A.'),
    ('Banco Compartamos S.A.', 'Banco Compartamos S.A.'),
    ('Banco Credit Suisse (México) S.A.', 'Banco Credit Suisse (México) S.A.'),
    ('Banco del Ahorro Nacional y Servicios Financieros S.N.C. (Bansefi)', 'Banco del Ahorro Nacional y Servicios Financieros S.N.C. (Bansefi)'),
    ('Banco del Bajío S.A.', 'Banco del Bajío S.A.'),
    ('Banco Inbursa S.A.', 'Banco Inbursa S.A.'),
    ('Banco Interacciones S.A.', 'Banco Interacciones S.A.'),
    ('Banco Invex S.A.', 'Banco Invex S.A.'),
    ('Banco J.P. Morgan S.A.', 'Banco J.P. Morgan S.A.'),
    ('Banco Mercantil del Norte S.A. (Banorte)', 'Banco Mercantil del Norte S.A. (Banorte)'),
    ('Banco Monex S.A.', 'Banco Monex S.A.'),
    ('Banco Multiva S.A.', 'Banco Multiva S.A.'),
    ('Banco Nacional de Comercio Exterior S.N.C. (Bancomext)', 'Banco Nacional de Comercio Exterior S.N.C. (Bancomext)'),
    ('Banco Nacional de México S.A. (Citibanamex)', 'Banco Nacional de México S.A. (Citibanamex)'),
    ('Banco Nacional de Obras y Servicios Públicos S.N.C. (Banobras)', 'Banco Nacional de Obras y Servicios Públicos S.N.C. (Banobras)'),
    ('Banco Nacional del Ejército Fuerza Aérea y Armada S.N.C. (Banjercito)', 'Banco Nacional del Ejército Fuerza Aérea y Armada S.N.C. (Banjercito)'),
    ('Banco Regional de Monterrey S.A. (Banregio)', 'Banco Regional de Monterrey S.A. (Banregio)'),
    ('Banco Santander (México) S.A.', 'Banco Santander (México) S.A.'),
    ('Banco Ve Por Mas S.A.', 'Banco Ve Por Mas S.A.'),
    ('Banco Wal-Mart de México Adelante S.A.', 'Banco Wal-Mart de México Adelante S.A.'),
    ('BanCoppel S.A.', 'BanCoppel S.A.'),
    ('Bank of America México S.A.', 'Bank of America México S.A.'),
    ('Bank of Tokyo-Mitsubishi UFJ (México)', 'Bank of Tokyo-Mitsubishi UFJ (México)'),
    ('Bansi S.A.', 'Bansi S.A.'),
    ('Barclays Bank México S.A.', 'Barclays Bank México S.A.'),
    ('BBVA Bancomer S.A.', 'BBVA Bancomer S.A.'),
    ('Bulltick Casa de Bolsa S.A. de C.V.', 'Bulltick Casa de Bolsa S.A. de C.V.'),
    ('Casa de Bolsa Finamex S.A. de C.V.', 'Casa de Bolsa Finamex S.A. de C.V.'),
    ('Casa de Cambio Tiber S.A. de C.V.', 'Casa de Cambio Tiber S.A. de C.V.'),
    ('CI Casa de Bolsa S.A. de C.V.', 'CI Casa de Bolsa S.A. de C.V.'),
    ('CIBanco S.A.', 'CIBanco S.A.'),
    ('Cls Bank International	', 'Cls Bank International	'),
    ('Consubanco S.A.', 'Consubanco S.A.'),
    ('Deutsche Bank México S.A.', 'Deutsche Bank México S.A.'),
    ('Deutsche Securities S.A. de C.V.', 'Deutsche Securities S.A. de C.V.'),
    ('Estructuradores del Mercado de Valores Casa de Bolsa S.A. de C.V.', 'Estructuradores del Mercado de Valores Casa de Bolsa S.A. de C.V.'),
    ('Evercore Casa de Bolsa S.A. de C.V.', 'Evercore Casa de Bolsa S.A. de C.V.'),
    ('Fifth Third Bank', 'Fifth Third Bank'),
    ('Fincomún Servicios Financieros Comunitarios S.A. de C.V.', 'Fincomún Servicios Financieros Comunitarios S.A. de C.V.'),
    ('GBM Grupo Bursátil Mexicano S.A.', 'GBM Grupo Bursátil Mexicano S.A.'),
    ('HDI Seguros S.A. de C.V.', 'HDI Seguros S.A. de C.V.'),
    ('Hipotecaria Su Casita S.A. de C.V.', 'Hipotecaria Su Casita S.A. de C.V.'),
    ('HSBC México S.A.', 'HSBC México S.A.'),
    ('ING Bank (México) S.A.', 'ING Bank (México) S.A.'),
    ('Inter Banco S.A.', 'Inter Banco S.A.'),
    ('INTERCAM Banco	', 'INTERCAM Banco	'),
    ('Intercam Casa de Bolsa S.A.', 'Intercam Casa de Bolsa S.A.'),
    ('IXE Banco S.A.', 'IXE Banco S.A.'),
    ('J.P. Morgan Casa de Bolsa S.A. de C.V.', 'J.P. Morgan Casa de Bolsa S.A. de C.V.'),
    ('J.P. Morgan Chase Bank NA', 'J.P. Morgan Chase Bank NA'),
    ('J.P. SOFIEXPRESS S.A. de C.V. S.F.P.', 'J.P. SOFIEXPRESS S.A. de C.V. S.F.P.'),
    ('Kuspit Casa de Bolsa S.A. de C.V.', 'Kuspit Casa de Bolsa S.A. de C.V.'),
    ('Libertad Servicios Financieros S.A. de C.V.', 'Libertad Servicios Financieros S.A. de C.V.'),
    ('MAPFRE Tepeyac S.A.', 'MAPFRE Tepeyac S.A.'),
    ('Masari Casa de Bolsa S.A.', 'Masari Casa de Bolsa S.A.'),
    ('Merrill Lynch México S.A. de C.V.', 'Merrill Lynch México S.A. de C.V.'),
    ('Monex Casa de Bolsa S.A. de C.V.', 'Monex Casa de Bolsa S.A. de C.V.'),
    ('N/A', 'N/A'),
    ('Nacional Financiera S.A. (Nafinsa)', 'Nacional Financiera S.A. (Nafinsa)'),
    ('Operaciones Empresariales del Noreste S.A. de C.V.', 'Operaciones Empresariales del Noreste S.A. de C.V.'),
    ('OPERADORA ACTINVER S.A. DE C.V.', 'OPERADORA ACTINVER S.A. DE C.V.'),
    ('Operadora de Recursos Reforma S.A. de C.V.', 'Operadora de Recursos Reforma S.A. de C.V.'),
    ('Order Express Casa de Cambio S.A. de C.V.', 'Order Express Casa de Cambio S.A. de C.V.'),
    ('Profuturo G.N.P. S.A. de C.V.', 'Profuturo G.N.P. S.A. de C.V.'),
    ('Scotiabank Inverlat S.A.', 'Scotiabank Inverlat S.A.'),
    ('SD. Indeval S.A. de C.V.', 'SD. Indeval S.A. de C.V.'),
    ('Seguros Monterrey New York Life S.A de C.V.', 'Seguros Monterrey New York Life S.A de C.V.'),
    ('Sistema de Transferencias y Pagos STP S.A. de C.V.', 'Sistema de Transferencias y Pagos STP S.A. de C.V.'),
    ('Skandia Operadora de Fondos S.A. de C.V.', 'Skandia Operadora de Fondos S.A. de C.V.'),
    ('Skandia Vida S.A. de C.V.', 'Skandia Vida S.A. de C.V.'),
    ('Sociedad Hipotecaria Federal S.N.C.', 'Sociedad Hipotecaria Federal S.N.C.'),
    ('Solución Asea S.A. de C.V.', 'Solución Asea S.A. de C.V.'),
    ('Sterling Casa de Cambio S.A. de C.V.', 'Sterling Casa de Cambio S.A. de C.V.'),
    ('Telecomunicaciones de México', 'Telecomunicaciones de México'),
    ('The Royal Bank of Scotland México S.A.', 'The Royal Bank of Scotland México S.A.'),
    ('UBS Bank México S.A.', 'UBS Bank México S.A.'),
    ('UNAGRA S.A. de C.V. S.F.P.', 'UNAGRA S.A. de C.V. S.F.P.'),
    ('Unica Casa de Cambio S.A. de C.V.', 'Unica Casa de Cambio S.A. de C.V.'),
    ('Valores Mexicanos Casa de Bolsa S.A. de', 'Valores Mexicanos Casa de Bolsa S.A. de'),
    ('Value S.A. de C.V.', 'Value S.A. de C.V.'),
    ('Vector Casa de Bolsa S.A. de C.V.', 'Vector Casa de Bolsa S.A. de C.V.'),
    ('Volkswagen Bank S.A.', 'Volkswagen Bank S.A.'),
    ('WELLS FARGO BANK', 'WELLS FARGO BANK'),
    ('Zurich Companía de Seguros S.A. de C.V.', 'Zurich Companía de Seguros S.A. de C.V.'),
    ('Zurich Vida Companía de Seguros S.A. de C.V.', 'Zurich Vida Companía de Seguros S.A. de C.V.'),
]
# Ordenar la lista alfabéticamente en función de las etiquetas
BANCO_LIST = sorted(BANCO_LIST, key=lambda item: item[1])

MONEDA_LIST = [
    ('', ' Seleccione una opción'),
    ('MXP', 'MXP'),
    ('USD', 'USD'),
]