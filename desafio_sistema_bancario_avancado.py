import textwrap

def menu ():
    menu = """\n
    ========== Informe a operação desejada: ==========
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [u]\tCriar usuário
    [c]\tCriar conta corrente
    [l]\tListar contas
    [q]\tSair
    => """
    return input(menu)

#FUNÇÃO SAQUE: Receber os argumentos apenas por nome (Keyword only). Possiveis argumentos: saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES. Possiveis retornos: saldo e extrato.  
#FUNÇÃO DEPOSITO: Receber os argumentos apenas por posição (positional only). Possiveis argumentos: saldo, valor, extrato. Possiveis retornos: saldo e extrato.  
#FUNÇÃO EXTRATO: Receber os argumentos por nome e por posição (positional only e keyword only). Argumentos posicionais: saldo; Argumentos nomeados: extrato  
#FUNÇÃO CRIAR USUÁRIO: Armazenar os usuários em uma lista. Usuário(nome, DN, CPF e endereço (String logradouro, nro - bairro - cidade/sigla estado)). Armazenar CPF como string e somente números, que é único por usuário.
#FUNÇÃO CRIAR CONTA CORRENTE: Armazenar contas em uma lista; Conta (agência, número da conta, usuário); Número da conta é sequencial e começa com 1. Número da agência é fixo = "0001". Usuário pode ter mais de uma conta, mas uma conta é somente de um usuário. 
#FUNÇÃO LISTAR CONTAS

#Para vincular um usuário a uma conta, filtrar a lista de usuários buscando o número do CPF informado para cada usuário da lista.


def sacar(*, saldo, valor, limite, extrato, numero_saques, limite_saques):

    #Verificações obrigatórias para autorização do saque:
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Saldo insuficiente.")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor de saque excede o limite.")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques foi excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR${valor:.2f}\n"
        numero_saques += 1
        print(f"\n Operação realizada com sucesso! \n Saldo atual: R${saldo:.2f} \n")

    else: 
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):
            
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(f"\n=== Operação realizada com sucesso! \nSaldo atual: R$ {saldo:.2f} ===\n")
        
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    print("\n===================== EXTRATO ==================== ")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f} \n")
    print("\n================================================== ")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF(somente números): ")
    cliente = filtrar_cliente(cpf, usuarios)

    if cliente:
        print("\n@@@ Já existe usuário cadastrado com esse CPF. @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe sua data de nascimento (dd-mm-aaaa): ")
    #endereço
    logradouro = input("Logradouro: ")
    numero_logradouro = input("Número do logradouro: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    uf = input("UF: ")
    endereco = (f'{logradouro}, {numero_logradouro} - {bairro} - {cidade}/{uf}')
    
    usuarios.append({"cpf": cpf, "nome": nome, "data_nascimento": data_nascimento, "endereco" : endereco })

    print("=== Usuário criado com sucesso! ===")


def filtrar_cliente(cpf, usuarios):
    clientes_filtrados = [cliente for cliente in usuarios if cliente["cpf"] == cpf]
    return  clientes_filtrados[0] if clientes_filtrados else None
    

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF(somente números): ")
    cliente = filtrar_cliente(cpf, usuarios)

    if cliente: 
        print("\n Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "cliente":cliente}


    print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado. @@@")


def listar_contas(lista_contas):
    for conta in lista_contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C\C:\t\t{conta['numero_conta']}
            Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():

    #print(" Iniciando Código")
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    lista_contas = []    

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float (input("Informe o valor do deposito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato, numero_saques = sacar(
                saldo = saldo,
                valor = valor,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            numero_conta = len(lista_contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                lista_contas.append(conta)

        elif opcao == "l":
            listar_contas(lista_contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()