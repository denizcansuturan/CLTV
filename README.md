# CUSTOMER LIFETIME VALUE

1. Data preparation
2. Average Order Value (average_order_value = total_price / total_transaction)
3. Purchase Frequency (total_transaction / total_number_of_customers)
4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
5. Profit Margin (profit_margin =  total_price * 0.10)
6. Customer Value (customer_value = average_order_value * purchase_frequency)
7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
8. Segmentation
9. Functionalization

**Business Problem**: 
An e-commerce company divides its customers into segments and wants to define marketing strategies according to these segments.
Dataset includes the sales of a UK based online store from 01/12/2009 to 09/12/2011.

**Variables**:
- **Invoice:** Unique number for every transaction. Invoices that start with C are cancelled transactions.
- **StockCode:** Unique number for every product.
- **Description:** Product name.
- **Quantity:** Number of specific product that has been ordered in an invoice.
- **InvoiceDate:** Invoice date including the time.
- **Price**: Unit prices(GBP)
- **Customer ID:** Unique number for each customer.
- **Country:** Country the customer lives.

[Medium Blog on this Problem]()
