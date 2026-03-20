def checar_colisao(obj1_x, obj1_y, obj1_largura, obj1_altura, 
                   obj2_x, obj2_y, obj2_largura, obj2_altura):
    
    # Verifica se há sobreposição no eixo X (Horizontal)
    # A direita do obj1 passa da esquerda do obj2? E a esquerda do obj1 passa da direita do obj2?
    colisao_x = (obj1_x < obj2_x + obj2_largura) and (obj1_x + obj1_largura > obj2_x)
    
    # Verifica se há sobreposição no eixo Y (Vertical)
    # O teto do obj1 passa do chão do obj2? E o chão do obj1 passa do teto do obj2?
    colisao_y = (obj1_y < obj2_y + obj2_altura) and (obj1_y + obj1_altura > obj2_y)
    
    # Se colidiu no X e no Y ao mesmo tempo, os objetos estão se tocando!
    return colisao_x and colisao_y