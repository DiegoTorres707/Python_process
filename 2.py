import pandas as pd

for i in range(1, 21):
    # Leer archivo de texto
    with open(f'{i}_100_Historico_NACK.txt') as f:
        datos = f.readlines()

    # Inicializar variables para generar resultados
    paquete_actual = None
    rx_ok_nack = False
    phydrop_nack = False
    nodos_colisionaron = 0
    no_nack = True
    num_error_data = 0
    num_txbegin_nack = 0
    rx_end_nack = False  # Nueva variable para buscar RXEND_NACK
    num_rxend_nack = 0  # Nueva variable para contar RXEND_NACK
    resultados = []

    # Procesar cada línea del archivo
    for linea in datos:
        # Obtener valores de la línea
        valores = linea.split()
        t = int(valores[1])
        nodo = valores[3]
        accion = valores[4]

        # Si cambiamos de paquete, guardar resultados del paquete anterior
        if paquete_actual is not None and t != paquete_actual:
            resultados.append({
                'Paquete': paquete_actual,
                'AP NACK OK': 'RX OK NACK' if rx_ok_nack else '',
                'Megacolision NACK': 'PHYDROP_NACK___' if phydrop_nack else '',
                'NO_NACK': 'X' if no_nack else '',
                'Numero_errorData': num_error_data,
                'TXBEginNACK': 'PHYTXBEGIN_NACK' if num_txbegin_nack > 0 else '',
                'Nume_TXBeginNACK': num_txbegin_nack,
                'num_nodos_colisionaron': nodos_colisionaron,
                'RX_END_NACK': 'RXEND_NACK' if rx_end_nack else '',  # Agregar nueva columna para RXEND_NACK
                'Num_RX_END_NACK': num_rxend_nack,  # Agregar nueva columna para contar RXEND_NACK
            })

            # Reiniciar variables para el nuevo paquete
            rx_ok_nack = False
            phydrop_nack = False
            nodos_colisionaron = 0
            no_nack = True
            num_error_data = 0
            num_txbegin_nack = 0
            rx_end_nack = False
            num_rxend_nack = 0

        # Actualizar variables según acción
        if accion == 'PHYTXBEGIN_DATA':
            paquete_actual = t
        elif accion == 'PHYRXOK_NACK___':
            rx_ok_nack = True
            no_nack = False
        elif accion == 'PHYDROP_NACK___':
            phydrop_nack = True
            nodos_colisionaron += 1
            no_nack = False
        elif accion == 'PHYRXERROR_DATA':
            num_error_data += 1
        elif accion == 'PHYTXBEGIN_NACK':
            num_txbegin_nack += 1
        elif accion == 'PHYRXEND_NACK__':  # Buscar RXEND_NACK y actualizar variables
            rx_end_nack = True
            num_rxend_nack += 1

    # Agregar resultados del último paquete procesado
    if paquete_actual is not None:
        resultados.append({
            'Paquete': paquete_actual,
            'AP NACK OK': 'RX OK NACK' if rx_ok_nack else '',
            'Megacolision NACK': 'PHYDROP_NACK___' if phydrop_nack else '',
            'NO_NACK': 'X' if no_nack else '',
            'Numero_errorData': num_error_data,
            'TXBEginNACK': 'PHYTXBEGIN_NACK' if num_txbegin_nack > 0 else '',
            'Nume_TXBeginNACK': num_txbegin_nack,
            'num_nodos_colisionaron': nodos_colisionaron,  # Agregamos la nueva columna
        })



        # Crear columnas para RX_END_NACK y num_RxEND_NACK
        rx_end_nack = 'RX_END_NACK' if num_rxend_nack > 0 else ''
        resultados[-1]['RX_END_NACK'] = rx_end_nack
        resultados[-1]['num_RxEND_NACK'] = num_rxend_nack

    # Crear DataFrame con resultados y guardar en archivo de Excel
    resultados_df = pd.DataFrame(resultados,
                                 columns=['Paquete', 'AP NACK OK', 'Megacolision NACK', 'NO_NACK', 'Numero_errorData',
                                          'TXBEginNACK', 'Nume_TXBeginNACK',
                                          'num_nodos_colisionaron', 'RX_END_NACK',
                                          'num_RxEND_NACK'])  # Agregar nuevas columnas al DataFrame
    resultados_df.to_excel(f'{i}_resultados.xlsx', index=False)

