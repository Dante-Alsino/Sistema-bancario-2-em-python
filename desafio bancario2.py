import textwrap


def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def depositar(saldo_atual, valor, extrato_atual, /):
    if valor > 0:
        saldo_atual += valor
        extrato_atual += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo_atual, extrato_atual


def sacar(*, saldo_atual, valor, extrato_atual, limite_saque, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo_atual
    excedeu_limite = valor > limite_saque
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo_atual -= valor
        extrato_atual += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo_atual, extrato_atual


def exibir_extrato(saldo_atual, /, *, extrato_atual):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato_atual else extrato_atual)
    print(f"\nSaldo:\t\tR$ {saldo_atual:.2f}")
    print("==========================================")


def criar_usuario(usuarios_lista):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios_lista)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios_lista.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios_lista):
    usuarios_filtrados = [usuario for usuario in usuarios_lista if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios_lista):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios_lista)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")


def listar_contas(contas_lista):
    for conta in contas_lista:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA_PADRAO = "0001"

    saldo_atual = 0
    limite_saque = 500
    extrato_atual = ""
    numero_saques = 0
    usuarios_lista = []
    contas_lista = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo_atual, extrato_atual = depositar(saldo_atual, valor, extrato_atual)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo_atual, extrato_atual = sacar(
                saldo_atual=saldo_atual,
                valor=valor,
                extrato_atual=extrato_atual,
                limite_saque=limite_saque,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo_atual, extrato_atual=extrato_atual)

        elif opcao == "nu":
            criar_usuario(usuarios_lista)

        elif opcao == "nc":
            numero_conta = len(contas_lista) + 1
            conta = criar_conta(AGENCIA_PADRAO, numero_conta, usuarios_lista)

            if conta:
                contas_lista.append(conta)

        elif opcao == "lc":
            listar_contas(contas_lista)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
