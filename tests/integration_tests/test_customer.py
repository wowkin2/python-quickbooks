from datetime import datetime, timedelta
import unittest
from quickbooks.objects.customer import Customer


class CustomerTest(unittest.TestCase):
    def setUp(self):
        self.DisplayName = "Name {0}".format(datetime.now().strftime('%d%H%M'))

    def test_create(self):
        customer = Customer()

        customer.DisplayName = self.DisplayName
        customer.save()

        self.id = customer.Id
        query_customer = Customer.get(customer.Id)

        self.assertEquals(customer.Id, query_customer.Id)
        self.assertEquals(query_customer.DisplayName, self.DisplayName)

    def test_update(self):
        customer = Customer.filter(DisplayName=self.DisplayName)[0]
        updated_name = self.DisplayName + "new"
        customer.DisplayName = updated_name
        customer.save()

        self.assertEquals(customer.DisplayName, updated_name)

    def test_changed(self):
        customers = Customer.all(max_results=2)

        for customer in customers:
            customer.DisplayName = "{0}{1}".format(customer.DisplayName, datetime.now().strftime('%d%H%M'))
            customer.save()

        changed_since = datetime.now() - timedelta(minutes=2)
        changed_customers = Customer.changed(changed_since.strftime("%Y-%m-%dT%H:%M:%S-06:00"))

        self.assertEquals(len(changed_customers), 2)
