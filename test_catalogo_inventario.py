"""Pruebas unitarias del catálogo basado en diccionarios."""

import tempfile
import unittest
from pathlib import Path

import catalogoInventario as modulo


class TestCatalogoInventario(unittest.TestCase):
    def setUp(self):
        self.productos = {
            1: {"nombre": "Leche", "categoria": "Lácteos", "precio": 100.0, "stock": 2, "descripcion": "Leche entera"},
            2: {"nombre": "Arroz", "categoria": "Almacén", "precio": 200.0, "stock": 10, "descripcion": "Arroz blanco"},
        }
        modulo.precios_originales.clear()
        modulo.precios_originales.update({1: 100.0, 2: 200.0})

    def test_stock_critico_filtra_productos(self):
        resultado = modulo.obtener_productos_stock_critico(self.productos, 2)
        self.assertEqual(list(resultado.keys()), [1])

    def test_descuento_por_categoria(self):
        resultado = modulo.aplicar_descuento_por_categoria(self.productos, "lácteos", 10)
        self.assertEqual(resultado[1]["precio"], 90.0)
        self.assertEqual(resultado[2]["precio"], 200.0)

    def test_descuento_repetido_no_se_acumula(self):
        primero = modulo.aplicar_descuento_por_categoria(self.productos, "Lácteos", 10)
        segundo = modulo.aplicar_descuento_por_categoria(primero, "Lácteos", 10)
        self.assertEqual(segundo[1]["precio"], 90.0)

    def test_rechaza_descuento_mayor_a_cien(self):
        with self.assertRaises(ValueError):
            modulo.aplicar_descuento_general(self.productos, 101)

    def test_rechaza_stock_negativo(self):
        with self.assertRaises(ValueError):
            modulo.actualizar_stock_producto(self.productos, 1, -1)

    def test_calcula_valor_total(self):
        self.assertEqual(modulo.calcular_valor_total_inventario(self.productos), 2200.0)

    def test_guardar_y_cargar_json(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "catalogo.json"
            self.assertTrue(modulo.guardar_catalogo_json(self.productos, ruta))
            cargados = modulo.cargar_catalogo_json(ruta)
            self.assertEqual(cargados, self.productos)

    def test_agrega_producto_con_id_siguiente(self):
        nuevo_id = modulo.agregar_nuevo_producto(
            self.productos, "Café", "Importados", 300, 4, "Café molido"
        )
        self.assertEqual(nuevo_id, 3)
        self.assertEqual(len(self.productos), 3)
        self.assertEqual(self.productos[3]["categoria"], "Importados")

    def test_obtener_categorias_sin_repetir(self):
        self.assertEqual(modulo.obtener_categorias(self.productos), ["Almacén", "Lácteos"])


if __name__ == "__main__":
    unittest.main()
