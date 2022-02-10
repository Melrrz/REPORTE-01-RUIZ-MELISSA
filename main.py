from math import prod
from unicodedata import name
from lifestore_file import lifestore_products, lifestore_sales, lifestore_searches

'''lifestore_searches = [id_search, id product]
lifestore_sales = [id_sale, id_product, score (from 1 to 5), date, refund (1 for true or 0 to false)]
lifestore_products = [id_product, name, price, category, stock]'''

IDX_SEARCHES_ID_SEARCH = 0
IDX_SEARCHES_ID_PRODUCT = 1
IDX_SALES_ID_SALE = 0
IDX_SALES_ID_PRODUCTO = 1
IDX_SALES_SCORE = 2
IDX_SALES_DATE = 3
IDX_SALES_REFUND = 4
IDX_PRODUCTS_ID = 0
IDX_PRODUCTS_NAME = 1
IDX_PRODUCTS_PRICE = 2
IDX_PRODUCTS_CATEGORY = 3
IDX_PRODUCTS_STOCK = 4

def login(user, contras):
    ''' 
    Retorna el nombre del usuario si el usuario y la contraseña coinciden con las credenciles
    En caso contrario retorna None
    '''
    credentials = [['mel', 'tico3'], ['dan', 'perro1'], ['carm', 'tutia'], ['luli', 'moy2']]
    for credencial in credentials:
        if user == credencial[0] and contras == credencial[1]:
            return user
    return None

def get_productos_agrupar_por_categoria():
    '''
    Agrupa los produc_id por categorías, retorna un diccionario 
    {'procesadores': [1, 2, 3...], 'otra categoría': [más product_id que pertenecen a esta]}
    '''
    categorias = {}
    for producto in lifestore_products:
        categoria_prod = producto[IDX_PRODUCTS_CATEGORY]
        if categoria_prod not in categorias.keys():
            categorias[categoria_prod] = []
        categorias[categoria_prod].append(producto[IDX_PRODUCTS_ID])
    return categorias   

def get_menos_ventas_por_categorias(categorias, lifestore_sales):
    '''
    Relaciona las categorias de los productos con su id, ventas, busquedas y las ordena
    A partir de las categorias agrega: 
    - las ventas  realizadas de esa categoría
    - las búsquedas a los productos de esa categoría
    - las productos con menores ventas de esa categoría
    - los productos con menores busquedas de esa categoría
    {'procesadores': 
        {
            prod_id: [1, 2, 3],
            ventas:[[1, 1, 5, '24/07/2020', 0]],
            ordenados_ventas:[(id_product, 32), (id_product, 47)], ordena ascendente
            busquedas:[[id_search,id_prod ]],
            ordenados_busquedas: [(id_prod, 54)] ordena ascendente
        }
    }
    '''
    prod_vendidos_por_categorias = {}
    for category in categorias:
        prod_vendidos_por_categorias[category] = {'prod_id':[], 'ventas':[], 'ordenados_ventas':[], 'busquedas':[], 'ordenados_busquedas':[]}
        contador_ventas = {}
        contador_busquedas = {}
        for prod_id in categorias[category]:
            contador_ventas[prod_id] = 0
            prod_vendidos_por_categorias[category]['prod_id'].append(prod_id)
            contador_busquedas[prod_id] = 0
            for sale in lifestore_sales:
                if prod_id == sale[IDX_SALES_ID_PRODUCTO]:
                    contador_ventas[prod_id] += 1
                    prod_vendidos_por_categorias[category]['ventas'].append(sale)
                    break
            for search in lifestore_searches:
                if prod_id == search[IDX_SEARCHES_ID_PRODUCT]:
                    contador_busquedas[prod_id] += 1
                    prod_vendidos_por_categorias[category]['busquedas'].append(search)
                    break
        ordenados_ventas = sorted(contador_ventas.items(), key = lambda x:x[1], reverse = False)
        prod_vendidos_por_categorias[category]['ordenados_ventas'] = ordenados_ventas
        ordenados_menores_busquedas = sorted(contador_busquedas.items(), key = lambda x:x[1], reverse = False)
        prod_vendidos_por_categorias[category]['ordenados_busquedas'] = ordenados_menores_busquedas
    return prod_vendidos_por_categorias

       
def get_ordenar_productos(lifestore_sales, limit = 5, top = True,):
    '''
    Retorna una lista de tuplas con la cantidad ventas que tuvo cada id_product y los ordena descendente
    '''
    productos = {}
    for sale in lifestore_sales:
        prod_id = sale[IDX_SALES_ID_PRODUCTO]
        if prod_id not in productos.keys():
            productos[prod_id] = 0
        productos[prod_id] +=1 
    productos_ordenados = sorted(productos.items(), key = lambda x:x[1], reverse = top)   
    return productos_ordenados[:limit]

def get_ordenar_por_resenas(lifestore_products, limit = 5, top = True):
    #To Do -> Averiguar que pedo con tomar en cuenta productos con devolución
    resenas = {}
    for sale in lifestore_sales:
        prod_id = sale[IDX_SALES_ID_PRODUCTO]
        if prod_id not in resenas.keys():
            resenas[prod_id] = {'score_acumulado':0,'cuenta':0}
        resenas[prod_id]['score_acumulado'] = resenas[prod_id]['score_acumulado'] + sale[IDX_SALES_SCORE]
        resenas[prod_id]['cuenta'] = resenas[prod_id]['cuenta'] + 1 
    for prod_id in resenas:
        prom = resenas[prod_id]['score_acumulado'] / resenas[prod_id]['cuenta'] 
        resenas[prod_id]['prom'] = prom
    promedios_ordenados = sorted(resenas.items(), key = lambda x:x[1]['prom'], reverse = top)
    return promedios_ordenados[:limit]   

def get_totales(lifestore_products, lifestore_sales):
    totales = {}
    for product in lifestore_products:
        for sale in lifestore_sales:
            id_prod = product[IDX_PRODUCTS_ID]
            if id_prod is not lifestore_sales:
                totales[id_prod] = 0




                

def get_product_name():
    '''
    Itearar en mi listado de productos para buscar el prod_id e imprimir el nombre del producto
    '''
    nombre_productos = {}
    for product in lifestore_products:
        nombre_productos[product[IDX_PRODUCTS_ID]] = product[IDX_PRODUCTS_NAME]
    return nombre_productos

    

        
     
   

def print_reports():
    '''
    Imprime el reporte con las:
    Lista de requerimientos de Emtech - Escribirla despues
    ToDo: Acomodar reportes de manera clara y visible
    '''
    nombres = get_product_name()

    mayores_ventas = get_ordenar_productos(lifestore_sales)
    print("Los productos con mayores ventas son: ", mayores_ventas)
    
    mayores_busquedas = get_ordenar_productos(lifestore_searches, 10, True)
    print("Los productos con mayores búsquedas son: ", mayores_busquedas)

    categorias = get_productos_agrupar_por_categoria()
    
    mejores_resenas = get_ordenar_por_resenas(lifestore_sales, limit = 5, top = True)
    print("Los productos con mejores reseñas son: ", mejores_resenas)

    menores_ventas = get_menos_ventas_por_categorias(categorias, lifestore_sales)
    for category in menores_ventas:
        menores_ventas[category]['ordenados_ventas']
        print(category)
        for i in range(5):
            if i < len(menores_ventas[category]['ordenados_ventas']):
                product = menores_ventas[category]['ordenados_ventas'][i]
                nombre = nombres[product[0]]
                print(f"El producto '{nombre[:15]}' se vendió: {product[1]} veces")

            

#[1, 1, 5, '24/07/2020', 0],
if __name__ == "__main__":
    mensaje_bienvenida = 'Bienvenidx al sistema\nAccede con tus credenciales'
    print(mensaje_bienvenida)
    oportunidad = 0
    while oportunidad < 3:
        user = input('Usuario: ')
        contrase = input('Contraseña: ')
        userloged = login(user, contrase)
        if userloged is not None:
            print('Login Exitoso')
            print_reports()    
            break
        else:
            print('No existe ningún usuario con esas Credenciales')
            oportunidad = oportunidad + 1        
    
    
    
    
    
    
    
    

         
    




