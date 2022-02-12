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
                devolucion = sale[IDX_SALES_REFUND]
                if devolucion == 0 and prod_id == sale[IDX_SALES_ID_PRODUCTO]:
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

def get_ordenar_por_resenas(limit = 5, top = True):
    '''
    Retorna un diccionario con el score acumulado, cuenta y promedio los 5 productos con las mejores o peores reseñas
    '''
    resenas = {}
    for sale in lifestore_sales:
        prod_id = sale[IDX_SALES_ID_PRODUCTO]
        if sale[IDX_SALES_REFUND] == 1:
            score = 1
        else:
            score = sale[IDX_SALES_SCORE]
        if prod_id not in resenas.keys():
            resenas[prod_id] = {'score_acumulado':0,'cuenta':0}
        resenas[prod_id]['score_acumulado'] = resenas[prod_id]['score_acumulado'] + score
        resenas[prod_id]['cuenta'] = resenas[prod_id]['cuenta'] + 1 
    for prod_id in resenas:
        prom = resenas[prod_id]['score_acumulado'] / resenas[prod_id]['cuenta'] 
        resenas[prod_id]['prom'] = prom
    promedios_ordenados = sorted(resenas.items(), key = lambda x:x[1]['prom'], reverse = top)
    return promedios_ordenados[:limit]   
        


def get_totales(lifestore_sales, name_and_price_product):
    '''
    Retorna un diccionario con las ventas e ingresos totales por año y por mes
    '''
    totales = {}
    for sale in lifestore_sales:
        anio = sale[IDX_SALES_DATE].split('/')[2]
        if anio not in totales:
            totales[anio] = {'total_anual': 0, 'cuenta_ventas': 0, 'meses': {}}
        mes = sale[IDX_SALES_DATE].split('/')[1]
        if mes not in totales[anio]['meses']:
            totales[anio]['meses'][mes] = {'total_mes': 0, 'cuenta_mes': 0} 
        devolucion = sale[IDX_SALES_REFUND]
        if devolucion == 0:     
            totales[anio]['cuenta_ventas'] +=1
            totales[anio]['meses'][mes]['cuenta_mes'] += 1  
            id_product = sale[IDX_SALES_ID_PRODUCTO]
            totales[anio]['total_anual'] = totales[anio]['total_anual'] + name_and_price_product[id_product][1]
            totales[anio]['meses'][mes]['total_mes'] += name_and_price_product[id_product][1]
    return totales 
      
      
def get_product_name_and_price():
    '''
    Itearar en mi listado para retornar un diccionario que contiene el id_product junto con su nombre y precio
    '''
    name_and_price_product = {}
    for product in lifestore_products:
        name_and_price_product[product[IDX_PRODUCTS_ID]] = (product[IDX_PRODUCTS_NAME], product[IDX_PRODUCTS_PRICE])
    return name_and_price_product
      
     
def print_reports():
    '''
    Imprime el reporte con las:
    Lista de requerimientos de Emtech - Escribirla despues
    ToDo: Acomodar reportes de manera clara y visible
    '''
    nombres = get_product_name_and_price()

    mayores_ventas = get_ordenar_productos(lifestore_sales)
    print("\n\n*LOS PRODUCTOS CON MAYORES VENTAS SON:")
    for venta in mayores_ventas:
        print(f"- id: {venta[0]}: {nombres[venta[0]][0][:30]}") 
        
    mayores_busquedas = get_ordenar_productos(lifestore_searches, 10, True)
    print("\n\n*LOS PRODUCTOS CON MAYORES BÚSQUEDAS SON:")
    for busqueda in mayores_busquedas:
        print(f"- id: {busqueda[0]}: {nombres[busqueda[0]][0][:30]}") 
        
    categorias = get_productos_agrupar_por_categoria()
    
    mejores_resenas = get_ordenar_por_resenas(limit = 5, top = True)
    print("\n\n*LOS PRODUCTOS CON MEJORES RESEÑAS SON: ")
    for producto in mejores_resenas:
        print(f"- id: {producto[0]}: {nombres[producto[0]][0][:30]}")

    peores_resenas = get_ordenar_por_resenas(limit = 5, top = False)
    print("\n\n*LOS PRODUCTOS CON PEORES RESEÑAS SON: ")
    for producto in peores_resenas:
        print(f"id: {producto[0]}: {nombres[producto[0]][0][:30]}")

    menores_ventas = get_menos_ventas_por_categorias(categorias, lifestore_sales)
    print('\n\n*LOS PRODUCTOS CON MENORES VENTAS POR CATEGORÍA SON:')
    for category in menores_ventas:
        menores_ventas[category]['ordenados_ventas']
        print(f"\n*** {category} ***")
        for i in range(5):
            if i < len(menores_ventas[category]['ordenados_ventas']):
                product = menores_ventas[category]['ordenados_ventas'][i]
                nombre = nombres[product[0]]
                print(f"- El producto '{nombre[0][:15]}', se vendió: {product[1]} veces")
    
    totales = get_totales(lifestore_sales, nombres)
    meses_del_anio = {"01":'Enero', "02":'Febrero', "03":'Marzo', "04":'Abril', "05":'Mayo', "06":'Junio', "07":'Julio', 
    "08":'Agosto', "09":'Septiembre', "10":'Octubre', "11":'Noviembre', "12":'Diciembre'}
    print("\n\n*INGRESOS TOTALES")
    for anio in totales:
        print(f"\n***EN {anio} EL INGRESO TOTAL FUE: $ {totales[anio]['total_anual']}***")
        venta_anual = 0
        for mes in meses_del_anio:
            if mes in totales[anio]['meses'] and totales[anio]['meses'][mes]['total_mes'] != 0:
                venta_anual = (venta_anual + totales[anio]['meses'][mes]['cuenta_mes'])
                print(f"- El ingreso total en {meses_del_anio[mes]} del {anio} fue: ${totales[anio]['meses'][mes]['total_mes']}")
            else: 
                print(f"- En {meses_del_anio[mes]} del {anio} no hubo ingresos")
        print(f"\n -Las ventas promedio mensuales del {anio} fueron: {(venta_anual/12):.2f}")
        meses_con_mas_ventas = sorted(totales[anio]['meses'].items(), key = lambda x:x[1]['cuenta_mes'], reverse = True)
        print("\n*MESES CON MAYORES VENTAS")
        for mes in meses_con_mas_ventas[0:4]:
            if mes[1]['cuenta_mes'] != 0:
                print(f"- El mes {meses_del_anio[mes[0]]} tuvo {mes[1]['cuenta_mes']} ventas")
            else:
                print(f"- Este año no hubo ventas")    

  
     

#[1, 1, 5, '24/07/2020', 0],
if __name__ == "__main__":
    print_reports()    
    exit()
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
    
    
    
    
    
    
    
    

         
    




