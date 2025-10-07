#!/usr/bin/env python3
"""
Generate random mock data for ClickHouse customer domain tables.

Usage:
    python generate_customer_data.py --customers 1000 --addresses 2000 --transactions 5000
    python generate_customer_data.py -c 100 -a 150 -t 500
"""

import argparse
import random
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize Faker
fake = Faker()

# Constants
CUSTOMER_STATUSES = ["active", "inactive", "suspended"]
LOYALTY_TIERS = ["bronze", "silver", "gold", "platinum"]
ADDRESS_TYPES = ["home", "work", "billing", "shipping"]
TRANSACTION_TYPES = ["purchase", "refund", "payment", "adjustment"]
PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer", "cash"]
TRANSACTION_STATUSES = ["completed", "pending", "failed", "cancelled"]
CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD"]


def generate_customers(num_customers):
    """Generate customer data."""
    print(f"Generating {num_customers} customers...")

    sql_lines = [
        "-- Generated Customer Data",
        "-- Total records: {}".format(num_customers),
        "USE customer_domain;",
        "",
        "INSERT INTO customer_domain.customer (",
        "  customer_id, first_name, last_name, email, phone,",
        "  date_of_birth, registration_date, customer_status,",
        "  loyalty_tier, total_lifetime_value",
        ") VALUES",
    ]

    values = []
    for i in range(1, num_customers + 1):
        customer_id = f"c{i:06d}"
        first_name = fake.first_name().replace("'", "''")
        last_name = fake.last_name().replace("'", "''")
        email = fake.email().replace("'", "''")
        phone = fake.phone_number().replace("'", "''")

        # Generate date of birth (18-80 years old)
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)

        # Registration date in the last 2 years
        days_ago = random.randint(1, 730)
        registration_date = datetime.now() - timedelta(days=days_ago)

        customer_status = random.choice(CUSTOMER_STATUSES)
        loyalty_tier = random.choice(LOYALTY_TIERS)
        total_lifetime_value = round(random.uniform(0, 50000), 2)

        value = (
            f"  ('{customer_id}', '{first_name}', '{last_name}', '{email}', '{phone}', "
            f"'{dob}', '{registration_date.strftime('%Y-%m-%d %H:%M:%S')}', '{customer_status}', "
            f"'{loyalty_tier}', {total_lifetime_value})"
        )
        values.append(value)

    # Join values with commas
    sql_lines.append(",\n".join(values) + ";")

    return "\n".join(sql_lines), num_customers


def generate_addresses(num_addresses, num_customers):
    """Generate customer address data."""
    print(f"Generating {num_addresses} addresses...")

    sql_lines = [
        "-- Generated Customer Address Data",
        "-- Total records: {}".format(num_addresses),
        "USE customer_domain;",
        "",
        "INSERT INTO customer_domain.customer_address (",
        "  address_id, customer_id, address_type, street_address,",
        "  city, state, postal_code, country, is_primary, is_verified",
        ") VALUES",
    ]

    values = []
    customer_address_count = {}  # Track addresses per customer

    for i in range(1, num_addresses + 1):
        address_id = f"a{i:06d}"

        # Assign to random customer
        customer_num = random.randint(1, num_customers)
        customer_id = f"c{customer_num:06d}"

        # Track how many addresses this customer has
        if customer_id not in customer_address_count:
            customer_address_count[customer_id] = 0
        customer_address_count[customer_id] += 1

        # First address for a customer is primary
        is_primary = customer_address_count[customer_id] == 1

        address_type = random.choice(ADDRESS_TYPES)
        street_address = fake.street_address().replace("'", "''")
        city = fake.city().replace("'", "''")
        state = fake.state_abbr()
        postal_code = fake.postcode()
        country = fake.country_code(representation="alpha-3")
        is_verified = random.choice([True, True, True, False])  # 75% verified

        value = (
            f"  ('{address_id}', '{customer_id}', '{address_type}', '{street_address}', "
            f"'{city}', '{state}', '{postal_code}', '{country}', {is_primary}, {is_verified})"
        )
        values.append(value)

    # Join values with commas
    sql_lines.append(",\n".join(values) + ";")

    return "\n".join(sql_lines), num_addresses


def generate_transactions(num_transactions, num_customers):
    """Generate customer transaction data."""
    print(f"Generating {num_transactions} transactions...")

    sql_lines = [
        "-- Generated Customer Transaction Data",
        "-- Total records: {}".format(num_transactions),
        "USE customer_domain;",
        "",
        "INSERT INTO customer_domain.customer_transaction (",
        "  transaction_id, customer_id, transaction_date, transaction_type,",
        "  amount, currency, payment_method, status, order_id, description",
        ") VALUES",
    ]

    values = []
    for i in range(1, num_transactions + 1):
        transaction_id = f"t{i:06d}"

        # Assign to random customer
        customer_num = random.randint(1, num_customers)
        customer_id = f"c{customer_num:06d}"

        # Transaction date in the last year
        days_ago = random.randint(1, 365)
        transaction_date = datetime.now() - timedelta(days=days_ago)

        transaction_type = random.choice(TRANSACTION_TYPES)

        # Refunds are negative
        if transaction_type == "refund":
            amount = round(random.uniform(-500, -10), 2)
        else:
            amount = round(random.uniform(10, 5000), 2)

        currency = random.choice(CURRENCIES)
        payment_method = random.choice(PAYMENT_METHODS)
        status = random.choice(TRANSACTION_STATUSES)
        order_id = f"ord-{random.randint(100000, 999999)}"

        # Generate description based on transaction type
        if transaction_type == "refund":
            description = fake.sentence(nb_words=3).replace("'", "''")
        else:
            description = fake.catch_phrase().replace("'", "''")

        value = (
            f"  ('{transaction_id}', '{customer_id}', '{transaction_date.strftime('%Y-%m-%d %H:%M:%S')}', "
            f"'{transaction_type}', {amount}, '{currency}', '{payment_method}', '{status}', "
            f"'{order_id}', '{description}')"
        )
        values.append(value)

    # Join values with commas
    sql_lines.append(",\n".join(values) + ";")

    return "\n".join(sql_lines), num_transactions


def write_to_file(filename, content):
    """Write content to a SQL file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Written to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate random mock data for ClickHouse customer domain tables.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --customers 1000 --addresses 2000 --transactions 5000
  %(prog)s -c 100 -a 150 -t 500
  %(prog)s -c 10000  # Generates 10k customers with default addresses/transactions
        """,
    )

    parser.add_argument(
        "-c",
        "--customers",
        type=int,
        default=1000,
        help="Number of customers to generate (default: 1000)",
    )

    parser.add_argument(
        "-a",
        "--addresses",
        type=int,
        default=None,
        help="Number of addresses to generate (default: customers * 1.5)",
    )

    parser.add_argument(
        "-t",
        "--transactions",
        type=int,
        default=None,
        help="Number of transactions to generate (default: customers * 5)",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="./sql_output",
        help="Output directory for SQL files (default: ./sql_output)",
    )

    args = parser.parse_args()

    # Calculate defaults
    num_customers = args.customers
    num_addresses = args.addresses if args.addresses else int(num_customers * 1.5)
    num_transactions = (
        args.transactions if args.transactions else int(num_customers * 5)
    )

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("Mock Data Generation")
    print("=" * 60)
    print(f"Customers:    {num_customers:,}")
    print(f"Addresses:    {num_addresses:,}")
    print(f"Transactions: {num_transactions:,}")
    print(f"Output dir:   {args.output_dir}")
    print("=" * 60 + "\n")

    # Generate data
    customer_sql, customer_count = generate_customers(num_customers)
    address_sql, address_count = generate_addresses(num_addresses, num_customers)
    transaction_sql, transaction_count = generate_transactions(
        num_transactions, num_customers
    )

    # Write to files
    write_to_file(f"{args.output_dir}/01_insert_customers.sql", customer_sql)
    write_to_file(f"{args.output_dir}/02_insert_addresses.sql", address_sql)
    write_to_file(f"{args.output_dir}/03_insert_transactions.sql", transaction_sql)

    print("\n" + "=" * 60)
    print("Generation Complete!")
    print("=" * 60)
    print(
        f"Total records generated: {customer_count + address_count + transaction_count:,}"
    )
    print(f"\nSQL files created in: {args.output_dir}/")
    print("\nTo load into ClickHouse:")
    print(
        f"  clickhouse-client --queries-file {args.output_dir}/01_insert_customers.sql"
    )
    print(
        f"  clickhouse-client --queries-file {args.output_dir}/02_insert_addresses.sql"
    )
    print(
        f"  clickhouse-client --queries-file {args.output_dir}/03_insert_transactions.sql"
    )
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
