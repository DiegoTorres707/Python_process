import pandas as pd

for i in range(1, 2):
    # Leer archivo de texto
    with open(f'Seed_{i}_Nnodos_1000_prob_0_1_HtMcs7_Historico_NACK.txt') as f:
        datos = f.readlines()

    # Inicializar variables para generar resultados
    paquete_actual = None
    rx_ok_ack = False
    phydrop_ack = False
    nodos_colisionaron = 0
    no_ack = True
    num_ok_data = 0
    num_txbegin_ack = 0
    num_rxend_ack=0
    num_rxerror_ack=0
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
                'AP ACK OK': 'RX OK ACK' if rx_ok_ack else '',
                'Megacolision ACK': 'PHYDROP_ACK____' if phydrop_ack else '',
                'NO_ACK': 'X' if no_ack else '',
                'Numero_Ok_Data': num_ok_data,
                'TXBEginACK': 'PHYTXBEGIN_ACK_' if num_txbegin_ack > 0 else '',
                'Nume_TXBeginACK': num_txbegin_ack,
                'num_nodos_colisionaron': nodos_colisionaron, # Agregamos la nueva columna
                'RxEnd_ACK': 'PHYRXEND_ACK___' if num_rxend_ack >0 else '',
                'Nume_RXEndACK': num_rxend_ack,
                'RxError_ACK': num_rxerror_ack if num_rxerror_ack >0 else '0'
            })

            # Reiniciar variables para el nuevo paquete
            rx_ok_ack = False
            phydrop_ack = False
            nodos_colisionaron = 0
            no_ack = True
            num_ok_data = 0
            num_txbegin_ack = 0
            num_rxend_ack=0
            num_rxerror_ack=0

        # Actualizar variables según acción
        if accion == 'PHYTXBEGIN_DATA':
            paquete_actual = t
        elif accion == 'PHYRXOK_ACK____':
            rx_ok_ack = True
            no_ack = False
        elif accion == 'PHYDROP_ACK____':
            phydrop_ack = True
            nodos_colisionaron += 1
            no_ack = False
        elif accion == 'PHYRXOK_DATA___':
            num_ok_data += 1
        elif accion == 'PHYTXBEGIN_ACK_':
            num_txbegin_ack += 1
        elif accion == 'PHYRXEND_ACK___':
            num_rxend_ack +=1
        elif accion == 'PHYRXERROR_ACK_':
            num_rxerror_ack +=1

    # Agregar resultados del último paquete procesado
    if paquete_actual is not None:
        resultados.append({
            'Paquete': paquete_actual,
            'AP ACK OK': 'RX OK ACK' if rx_ok_ack else '',
            'Megacolision ACK': 'PHYDROP_ACK____' if phydrop_ack else '',
            'NO_ACK': 'X' if no_ack else '',
            'Numero_Ok_Data': num_ok_data,
            'TXBEginACK': 'PHYTXBEGIN_ACK' if num_txbegin_ack > 0 else '',
            'Nume_TXBeginACK': num_txbegin_ack,
            'num_nodos_colisionaron': nodos_colisionaron, # Agregamos la nueva columna
            'RxEnd_ACK': 'PHYRXEND_ACK___' if num_rxend_ack > 0 else '',
            'Nume_RXEndACK': num_rxend_ack,
            'RxError_ACK': num_rxerror_ack if num_rxerror_ack > 0 else '0'
        })

    # Crear DataFrame con resultados y guardar en archivo de Excel
    resultados_df = pd.DataFrame(resultados,
                                 columns=['Paquete', 'AP ACK OK', 'Megacolision ACK', 'NO_ACK', 'Numero_Ok_Data',
                                          'TXBEginACK', 'Nume_TXBeginACK',
                                          'num_nodos_colisionaron', 'RxEnd_ACK','Nume_RXEndACK','RxError_ACK'])  # Agregar nueva columna al DataFrame
    resultados_df.to_excel(f'{i}_resultados_Nnodos_1000_ACK.xlsx', index=False)