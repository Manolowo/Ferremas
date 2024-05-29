class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            self.session['carrito'] = {}
            self.carrito = self.session['carrito']
        else:
            self.carrito = carrito
            
    def agregar(self, producto):
        id = str(producto.prod_id)
        if id not in self.carrito.keys():
            self.carrito[id] = {
                "id_prod": producto.prod_id,
                "nombre": producto.prod_nom,
                "precio": producto.prod_prec,
                "cantidad": 1,  
                "subtotal": producto.prod_prec,  
            }
        else:
            self.carrito[id]["cantidad"] += 1
            self.carrito[id]["subtotal"] = self.carrito[id]["cantidad"] * producto.prod_prec
        self.guardarCarrito()
    
    def restar(self, producto):
        id = str(producto.prod_id)
        if id in self.carrito.keys():
            if self.carrito[id]["cantidad"] > 1:
                self.carrito[id]["cantidad"] -= 1
                self.carrito[id]["subtotal"] = self.carrito[id]["cantidad"] * producto.prod_prec
            else:
                del self.carrito[id]
        self.guardarCarrito()
        
    def total_carrito(self):
        total = 0
        for item in self.carrito.values():
            total += item["subtotal"]
        return total

    def guardarCarrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True
    
    def eliminar(self, producto):
        id = str(producto.prod_id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardarCarrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

