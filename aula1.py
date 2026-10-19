frota = []

def normalizar(texto):
    return texto.strip().lower()

def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Erro: o campo não pode ficar vazio.")

def ler_ano():
    while True:
        try:
            ano = int(input("Ano do caminhão: "))
            if ano > 0:
                return ano
            print("Erro: digite um ano válido.")
        except ValueError:
            print("Erro: digite apenas números para o ano.")

def normalizar_estado(estado):
    estados = {
        "sao paulo": "SP", "sp": "SP", "parana": "PR", "pr": "PR",
        "minas gerais": "MG", "mg": "MG", "rio de janeiro": "RJ", "rj": "RJ",
        "santa catarina": "SC", "sc": "SC", "rio grande do sul": "RS", "rs": "RS",
        "bahia": "BA", "ba": "BA", "goias": "GO", "go": "GO"
    }
    return estados.get(normalizar(estado), "")

def ler_estado():
    while True:
        estado = normalizar_estado(input("Digite o estado: "))
        if estado:
            return estado
        print("Erro: estado inválido. Digite uma sigla ou o nome completo do estado.")

def ler_placa():
    while True:
        placa = input("Digite a placa: ").strip().upper()
        if len(placa) >= 7:
            return placa
        print("Erro: digite uma placa válida com pelo menos 7 caracteres.")

def mostrar_caminhao(caminhao):
    for campo, rotulo in [
        ("placa", "Placa"), ("modelo", "Modelo"), ("motorista", "Motorista"),
        ("cidade", "Cidade"), ("estado", "Estado"), ("carga", "Carga"), ("ano", "Ano")
    ]:
        print(f"{rotulo}: {caminhao[campo]}")

def cadastrar_caminhao():
    print("\nCADASTRAR CAMINHÃO")
    placa = ler_placa()
    if any(c["placa"] == placa for c in frota):
        print("Essa placa já está cadastrada.")
        return
    caminhao = {
        "placa": placa,
        "modelo": ler_texto("Digite o modelo: "),
        "motorista": ler_texto("Digite o motorista: "),
        "cidade": ler_texto("Digite a cidade: "),
        "estado": ler_estado(),
        "carga": ler_texto("Qual o tipo de carga: "),
        "ano": ler_ano()
    }
    frota.append(caminhao)
    print("Caminhão cadastrado com sucesso!")

def listar_caminhoes():
    print("\nLISTA DE CAMINHÕES")
    if not frota:
        print("Nenhum caminhão cadastrado.")
        return
    for i, caminhao in enumerate(frota, 1):
        print(f"\nCaminhão {i}")
        mostrar_caminhao(caminhao)

def _pesquisar(campo, mensagem, normalizar_valor=False, estado=False):
    print("\nPESQUISAR", campo.upper())
    valor = ler_estado() if estado else ler_texto(mensagem)
    if normalizar_valor:
        valor = normalizar(valor)
    encontrados = [
        c for c in frota
        if (normalizar(c[campo]) if normalizar_valor else c[campo]) == valor
    ]
    if not encontrados:
        print("Nenhum caminhão encontrado.")
    for c in encontrados:
        print("\nCaminhão encontrado!")
        mostrar_caminhao(c)

def procurar_placa():
    placa = ler_placa()
    encontrados = [c for c in frota if c["placa"] == placa]
    if encontrados:
        mostrar_caminhao(encontrados[0])
    else:
        print("Nenhum caminhão encontrado.")

def procurar_motorista():
    _pesquisar("motorista", "Digite o nome do motorista: ", True)

def procurar_cidade():
    _pesquisar("cidade", "Digite o nome da cidade: ", True)

def procurar_estado():
    _pesquisar("estado", "Digite o estado: ", estado=True)

def procurar_carga():
    _pesquisar("carga", "Digite o tipo de carga: ", True)

def alterar_caminhao():
    print("\nALTERAR CAMINHÃO")
    placa = ler_placa()
    c = next((item for item in frota if item["placa"] == placa), None)
    if c is None:
        print("Nenhum caminhão encontrado.")
        return
    mostrar_caminhao(c)
    print("Deixe o campo vazio para não alterar.")
    for campo, rotulo in [("modelo", "Novo modelo: "), ("motorista", "Novo motorista: "),
                          ("cidade", "Nova cidade: "), ("estado", "Novo estado: "),
                          ("carga", "Nova carga: "), ("ano", "Novo ano: ")]:
        valor = input(rotulo).strip()
        if not valor:
            continue
        if campo == "estado":
            valor = normalizar_estado(valor)
            if not valor:
                print("Estado inválido; não foi alterado.")
                continue
        elif campo == "ano":
            try:
                valor = int(valor)
                if valor <= 0:
                    print("Ano inválido; não foi alterado.")
                    continue
            except ValueError:
                print("Digite apenas números para o ano.")
                continue
        c[campo] = valor
    print("Caminhão alterado com sucesso!")

def remover_caminhao():
    print("\nREMOVER CAMINHÃO")
    placa = ler_placa()
    c = next((item for item in frota if item["placa"] == placa), None)
    if c is None:
        print("Nenhum caminhão encontrado.")
        return
    mostrar_caminhao(c)
    while True:
        resposta = input("Deseja realmente remover? (S/N): ").strip().upper()
        if resposta == "S":
            frota.remove(c)
            print("Caminhão removido com sucesso!")
            return
        if resposta == "N":
            print("Remoção cancelada.")
            return
        print("Opção inválida. Digite apenas S ou N.")

def estatisticas():
    print("\nESTATÍSTICAS DA FROTA")
    if not frota:
        print("Nenhum caminhão cadastrado.")
        return
    print("Total de caminhões:", len(frota))
    for estado in ("SP", "PR", "MG", "RJ"):
        print(f"Caminhões de {estado}:", sum(c["estado"] == estado for c in frota))
    print("Caminhões de outros estados:", sum(c["estado"] not in ("SP", "PR", "MG", "RJ") for c in frota))
