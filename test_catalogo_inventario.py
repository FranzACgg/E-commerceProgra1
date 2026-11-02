"""Pruebas unitarias básicas del módulo de catálogo."""

import json
import tempfile
import unittest
from pathlib import Path

import catalogoInventario as modulo


class TestCatalogoInventario(unittest.TestCase):
    def setUp(self):
        self.productos = [
            [1, "Leche", "Lácteos", 100.0, 2, "Leche entera"],
            [2, "Arroz", "Almacén", 200.0, 10, "Arroz blanco"],
        ]
        modulo.precios_originales.clear()
        modulo.precios_originales.update({1: 100.0, 2: 200.0})

    def test_stock_critico_filtra_productos(self):
        resultado = modulo.obtener_productos_stock_critico(self.productos, 2)
        self.assertEqual([producto[0] for producto in resultado], [1])

    def test_descuento_por_categoria(self):
        resultado = modulo.aplicar_descuento_por_categoria(self.productos, "lácteos", 10)
        self.assertEqual(resultado[0][3], 90.0)
        self.assertEqual(resultado[1][3], 200.0)

    def test_descuento_repetido_no_se_acumula(self):
        primero = modulo.aplicar_descuento_por_categoria(self.productos, "Lácteos", 10)
        segundo = modulo.aplicar_descuento_por_categoria(primero, "Lácteos", 10)
        self.assertEqual(segundo[0][3], 90.0)

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


if __name__ == "__main__":
    unittest.main()
