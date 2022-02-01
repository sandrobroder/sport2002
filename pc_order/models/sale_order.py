# -*- coding: utf-8 -*-
from odoo import fields, models
import json


class SaleOrder(models.Model):
	_inherit = 'sale.order'

	reference_customer = fields.Char(string="Reference Customer", compute="_compute_reference_customer", copy=False)

	def _compute_reference_customer(self):
		for sale in self:
			reference_customer = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								reference_customer = record.name

			sale.reference_customer = reference_customer

	payment_method = fields.Char(string="Pago Prestashop", compute="_compute_payment_method", copy=False)

	def _compute_payment_method(self):
		for sale in self:
			payment_method = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								payment_method = record.payment_method

			sale.payment_method = payment_method

	store_id = fields.Char(string="ID Pedido", compute="_compute_store_id", copy=False)

	def _compute_store_id(self):
		for sale in self:
			store_id = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								store_id = record.store_id

			sale.store_id = store_id

	delivery_method = fields.Char(string="Delivery Method", compute="_compute_delivery_method", copy=False)

	def _compute_delivery_method(self):
		for sale in self:
			delivery_method = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								delivery_method = record.carrier_id

			sale.delivery_method = delivery_method

	order_date = fields.Datetime(string="Fecha Prestahop", compute="_compute_order_date", copy=False, readonly=True)

	def _compute_order_date(self):
		for sale in self:
			order_date = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								order_date = record.date_order

			sale.order_date = order_date

	order_state = fields.Char(string="Order State", compute="_compute_order_state", copy=False)

	def _compute_order_state(self):
		for sale in self:
			order_state = ""
			order_id = sale.id
			mapped = self.env['channel.order.mappings'].search([('order_name', '=', order_id)])
			if mapped:
				for map_data in mapped:
					store_id = map_data.store_order_id
					if store_id:
						store_order_data = self.env['order.feed'].search([('store_id', '=', store_id)])
						if store_order_data:
							for record in store_order_data:
								order_state = record.order_state
								if (type(order_state) is str) and (len(order_state) > 2):
									value_pos = order_state.find('value')
									order_state = order_state[value_pos + 9:]
									value_pos = order_state.find("'")
									order_state = order_state[:value_pos]
								else:
									order_state=order_state

			sale.order_state = order_state

	estado = fields.Selection(
		[('10', 'Pago por transferencia bancaria pendiente'), ('18', ''), ('19', 'Generar etiqueta correos express'),
		 ('21', ''), ('2', 'Pago aceptado'), ('3', 'Preparación en proceso - sending'), ('4', 'Enviado'),
		 ('5', 'Entregado'), ('55', 'Entregado desde Dupla'), ('6', 'Cancelado'), ('7', 'Reembolso'),
		 ('8', 'Error en el pago'),('27', 'CETELEM - Crédito Aprobado')], string="Estado Prestashop", compute="_compute_estado", copy=False)

	def _compute_estado(self):
		estado = "10"
		estados_posibles = ['10', '2', '18', '19', '21', '3', '4', '5', '55', '6', '7', '8','27']
		for sale in self:
			if sale.order_state in estados_posibles:
				sale.estado = sale.order_state
			else:
				sale.estado = ""

	amount_tax = fields.Monetary(string='Taxes', store=True, readonly=False, compute='_amount_all')
