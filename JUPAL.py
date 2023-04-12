class Node(object):
    def __init__(self, name):
        self.direita = None
        self.name = name
        self.esquerda = None
        self.altura = 1


def find_node(node, busca):
    while node and busca != node.name:
        if busca < node.name:
            node = node.esquerda
        else:
            node = node.direita
    return node


def find_min(node):
    while node.esquerda:
        node = node.esquerda
    return node


def find_max(node):
    while node.direita:
        node = node.direita
    return node


class Tree():
    def rotacionar_esquerda(self, node):
        temp1 = node.direita
        temp2 = temp1.esquerda

        temp1.esquerda = node
        node.direita = temp2

        node.altura = self.altura(node)
        temp1.altura = self.altura(temp1)

        return temp1

    def rotacionar_direita(self, node):
        temp1 = node.esquerda
        temp2 = temp1.direita

        temp1.direita = node
        node.esquerda = temp2

        node.altura = self.altura(node)
        temp1.altura = self.altura(temp1)

        return temp1

    def altura(self, node):
        altura_esquerda = 0
        if node.esquerda:
            altura_esquerda = node.esquerda.altura
        altura_direita = 0
        if node.direita:
            altura_direita = node.direita.altura
        altura_maior_perna = max(altura_direita, altura_esquerda)
        return altura_maior_perna + 1

    def add_node(self, node, name):
        if find_node(node, name) == None:
            if node == None:
                print(name, "INSERIDO")
                return Node(name)
            elif name < node.name:
                node.esquerda = self.add_node(node.esquerda, name)
            else:
                node.direita = self.add_node(node.direita, name)

            node.altura = self.altura(node)
            return self.AVL_check(node)
        else:
            print(name, "JA EXISTE")
            return node

    def AVL_weight(self, node):
        if node != None:
            altura_esquerda = 0
            if node.esquerda:
                altura_esquerda = node.esquerda.altura
            altura_direita = 0
            if node.direita:
                altura_direita = node.direita.altura
            return altura_esquerda - altura_direita
        return 0

    def remover_node(self, node, name):
        if not node:
            print(name, "NAO ENCONTRADO")
            return node
        elif name < node.name:
            node.esquerda = self.remover_node(node.esquerda, name)
        elif name > node.name:
            node.direita = self.remover_node(node.direita, name)
        else:
            print(name, "DELETADO")
            if not node.esquerda:
                return node.direita
            elif not node.direita:
                return node.esquerda
            temp = find_min(node.direita)
            node.name = temp.name
            node.direita = self.find_replacement(node.direita, temp.name)

        node.altura = self.altura(node)
        return self.AVL_check(node)

    def find_replacement(self, node, name):
        if name < node.name:
            node.esquerda = self.find_replacement(node.esquerda, name)
        elif name > node.name:
            node.direita = self.find_replacement(node.direita, name)
        else:
            if not node.esquerda:
                return node.direita
            elif not node.direita:
                return node.esquerda
            temp = find_min(node.direita)
            node.name = temp.name
            node.direita = self.find_replacement(node.direita, temp.name)

        node.altura = self.altura(node)
        return self.AVL_check(node)

    def AVL_check(self, node):
        bf = self.AVL_weight(node)
        if bf > 1:
            if self.AVL_weight(node.esquerda) >= 0:
                return self.rotacionar_direita(node)
            else:
                node.esquerda = self.rotacionar_esquerda(node.esquerda)
                return self.rotacionar_direita(node)
        if bf < -1:
            if self.AVL_weight(node.direita) <= 0:
                return self.rotacionar_esquerda(node)
            else:
                node.direita = self.rotacionar_direita(node.direita)
                return self.rotacionar_esquerda(node)
        return node


def printar_todo_node(node, maximo):
    if node != None:
        printar_todo_node(node.esquerda, maximo)
        if node.name != maximo:
            print(node.name, end=" ")
        else:
            print(node.name, end="\n")
        printar_todo_node(node.direita, maximo)


tree = Tree()
node_raiz = None

while True:
    instrucao = input().split()
    if instrucao[0].startswith('INSERIR'):
        node_raiz = tree.add_node(node_raiz, instrucao[1])
    elif instrucao[0].startswith('ALTURA'):
        altura = 0
        if node_raiz:
            altura = node_raiz.altura
        print("ALTURA:", altura)
    elif instrucao[0].startswith('DELETAR'):
        node_raiz = tree.remover_node(node_raiz, instrucao[1])
    elif instrucao[0].startswith('MAXIMO'):
        if node_raiz != None:
            print("MAIOR:", find_max(node_raiz).name)
        else:
            print("ARVORE VAZIA")
    elif instrucao[0].startswith('MINIMO'):
        if node_raiz != None:
            print("MENOR:", find_min(node_raiz).name)
        else:
            print("ARVORE VAZIA")
    else:
        if node_raiz != None:
            printar_todo_node(node_raiz, find_max(node_raiz).name)
        else:
            print("ARVORE VAZIA")
        break
