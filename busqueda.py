import pandas as pd

for i in range(1, 2):
    # Leer archivo de texto
    with open(f'Seed_{i}_Nnodos_1000_prob_0_1_HtMcs7_Historico_NACK.txt') as f:
        datos = f.readlines()

    # Inicializar variables para generar resultados
    paquete_actual = None
    rx_ok_nack = False
    phydrop_nack = False
    nodos_colisionaron = 0
    no_nack = True
    num_error_data = 0
    num_txbegin_nack = 0
    num_rxend_nack=0
    num_rxerror_nack=0
    resultados = []

    # Procesar cada línea del archivo
    for linea in datos:
        # Obtener valores de la línea
        valores = linea.split()
        t = int(valores[1])
        nodo = valores[3]
        accion = valores[6]

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
                'num_nodos_colisionaron': nodos_colisionaron, # Agregamos la nueva columna
                'RxEnd_NACK': 'PHYRXEND_NACK__' if num_rxend_nack >0 else '',
                'Nume_RXEndNACK': num_rxend_nack,
                'RxError_NACK': num_rxerror_nack if num_rxerror_nack >0 else '0'
            })

            # Reiniciar variables para el nuevo paquete
            rx_ok_nack = False
            phydrop_nack = False
            nodos_colisionaron = 0
            no_nack = True
            num_error_data = 0
            num_txbegin_nack = 0
            num_rxend_nack=0
            num_rxerror_nack=0

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
        elif accion == 'PHYRXEND_NACK__':
            num_rxend_nack +=1
        elif accion == 'PHYRXERROR_NACK':
            num_rxerror_nack +=1

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
            'num_nodos_colisionaron': nodos_colisionaron, # Agregamos la nueva columna
            'RxEnd_NACK': 'PHYRXEND_NACK__' if num_rxend_nack > 0 else '',
            'Nume_RXEndNACK': num_rxend_nack,
            'RxError_NACK': num_rxerror_nack if num_rxerror_nack > 0 else '0'
        })

    # Crear DataFrame con resultados y guardar en archivo de Excel
    resultados_df = pd.DataFrame(resultados,
                                 columns=['Paquete', 'AP NACK OK', 'Megacolision NACK', 'NO_NACK', 'Numero_errorData',
                                          'TXBEginNACK', 'Nume_TXBeginNACK',
                                          'num_nodos_colisionaron', 'RxEnd_NACK','Nume_RXEndNACK','RxError_NACK'])  # Agregar nueva columna al DataFrame
    resultados_df.to_excel(f'{i}_resultados_Nnodos_1000_NACK.xlsx', index=False)

