import os
import unittest

from quickbooks.client import QuickBooks
from quickbooks.objects.customer import Customer
from quickbooks.objects.detailline import SaleItemLine, SalesItemLineDetail
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from quickbooks.objects.base import CustomerMemo


class InvoiceTest(unittest.TestCase):
    def setUp(self):
        QuickBooks(
            sandbox=True,
            consumer_key=os.environ.get('CONSUMER_KEY'),
            consumer_secret=os.environ.get('CONSUMER_SECRET'),
            access_token=os.environ.get('ACCESS_TOKEN'),
            access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET'),
            company_id=os.environ.get('COMPANY_ID')
        )

    def test_create(self):
        invoice = Invoice()

        line = SaleItemLine()
        line.LineNum = 1
        line.Description = "description"
        line.Amount = 100
        line.SalesItemLineDetail = SalesItemLineDetail()
        item = Item.all(max_results=1)[0]

        line.SalesItemLineDetail.ItemRef = item.to_ref()
        invoice.Line.append(line)

        customer = Customer.all(max_results=1)[0]
        invoice.CustomerRef = customer.to_ref()

        invoice.CustomerMemo = CustomerMemo()
        invoice.CustomerMemo.value = "Customer Memo"
        invoice.save()

        query_invoice = Invoice.get(invoice.Id)

        self.assertEquals(query_invoice.CustomerRef.name, customer.DisplayName)
        self.assertEquals(query_invoice.CustomerMemo.value, "Customer Memo")
        self.assertEquals(query_invoice.Line[0].Description, "description")
        self.assertEquals(query_invoice.Line[0].Amount, 100.0)
