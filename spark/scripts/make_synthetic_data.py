from pydantic import BaseModel, UUID4, Field, validator, field_validator, root_validator, model_validator
from typing import List, Union
import random
from enum import Enum, auto
import numpy as np
import pandas as pd
from uuid import uuid4
from datetime import date, datetime
from faker import Faker
from hashlib import sha256
from pathlib import Path

fake = Faker()

class TransactionStatus(Enum):
    COMPLETED = 'Completed'
    PENDING = 'Pending'
    FAILED = 'Failed'
    REVERSED = 'Reversed'

class Currency(Enum):
    ISK = 'ISK'
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    JPY = 'JPY'

class Network(Enum):
    VISA = 'Visa'
    MASTERCARD = 'MasterCard'
    AMEX = 'American Express'
    DISCOVER = 'Discover'

class CardType(Enum):
    CREDIT = 'Credit'
    DEBIT = 'Debit'

class DeviceType(Enum):
    MOBILE = ("Mobile", ["NFC", "Online Payment Gateway"])
    TABLET = ("Tablet", ["NFC", "Online Payment Gateway"])
    DESKTOP = ("Desktop", ["Online Payment Gateway"])
    POS_TERMINAL = ("POS", ["NFC", "EMV Chip", "Magnetic Stripe", "Online Payment Gateway"])

    def __init__(self, label, payment_methods):
        self.label = label
        self.payment_methods = payment_methods

class PaymentMethod(Enum):
    NFC = ("NFC", ["Visa", "MasterCard", "AMEX", "Discover"], ["Credit"])
    EMV_CHIP = ("EMV Chip", ["Visa", "MasterCard", "AMEX", "Discover"], ["Credit", "Debit"])
    MAGNETIC_STRIPE = ("Magnetic Stripe", ["Visa", "MasterCard", "AMEX", "Discover"], ["Credit", "Debit"])
    ONLINE_GATEWAY = ("Online Payment Gateway", ["Visa", "MasterCard"], ["Credit"])

    def __init__(self, label, networks, card_types):
        self.label = label
        self.networks = networks
        self.card_types = card_types

class Provider(Enum):
    RAPYD = 5006830589
    TAYA = 4406861259
    STRAUMUR = 6209221020

class MCC(Enum):
    AIRLINES = '3000'
    GROCERY_STORES = '5411'
    HOTELS = '7011'
    OFFICE_SUPPLIES = '5111'
    AUTOMATED_FUEL_DISPENSERS = '5542'
    ELECTRONICS = '5732'
    GAS_STATIONS = '5541'
    PHARMACIES = '5912'


class DistributionType(Enum):
    NORMAL = 'normal'
    UNIFORM = 'uniform'
    EXPONENTIAL = 'exponential'

class Transaction(BaseModel):
    distribution: DistributionType
    value: float = Field(default=None)

    @model_validator(mode='before')
    def set_and_validate_value(cls, values):
        distribution = values['distribution']
        if distribution == DistributionType.NORMAL:
            values['value'] = float(np.random.normal(loc=1000, scale=500))
        elif distribution == DistributionType.UNIFORM:
            values['value'] = float(np.random.uniform())
        elif distribution == DistributionType.EXPONENTIAL:
            values['value'] = float(np.random.exponential())
        return values


class Bank(Enum):
    LANDSBANKINN = 4710080280
    ARION = 5810080150
    ISLANDSBANKI = 4910080160 

class Location(Enum):
    KOPAVOGUR = 200
    REYKJAVIK = 101
    AKUREYRI = 600
    HAFNARFJORDUR = 220
    KEFLAVIK = 230

class Merchant(BaseModel):
    name: str
    ssn: str
    mcc_codes: List[MCC]
    bank: Bank
    locations: List[Location]

merchants = {
    "KRONAN": Merchant(name="KRONAN", ssn="7112982239", mcc_codes=[MCC.GROCERY_STORES, MCC.PHARMACIES], bank=Bank.LANDSBANKINN, locations=[Location.REYKJAVIK, Location.KOPAVOGUR, Location.AKUREYRI]),
    "ELKO": Merchant(name="ELKO", ssn="5610003280", mcc_codes=[MCC.ELECTRONICS], bank=Bank.ARION, locations=[Location.AKUREYRI, Location.KEFLAVIK]),
    "N1": Merchant(name="N1", ssn="4110033370", mcc_codes=[MCC.GAS_STATIONS, MCC.AUTOMATED_FUEL_DISPENSERS], bank=Bank.ISLANDSBANKI, locations=[Location.HAFNARFJORDUR]),
    "BONUS": Merchant(
        name="BONUS",
        ssn="4501993389",
        mcc_codes=[MCC.GROCERY_STORES],
        bank=Bank.LANDSBANKINN,
        locations=[Location.REYKJAVIK, Location.KOPAVOGUR, Location.AKUREYRI]
    ),
    "OLIS": Merchant(
        name="OLIS",
        ssn="5002693249",
        mcc_codes=[MCC.GAS_STATIONS],
        bank=Bank.ARION,
        locations=[Location.REYKJAVIK, Location.HAFNARFJORDUR, Location.KEFLAVIK]
    ),
    "SAMKAUP": Merchant(
        name="SAMKAUP",
        ssn="5712983769",
        mcc_codes=[MCC.GROCERY_STORES, MCC.PHARMACIES],
        bank=Bank.ISLANDSBANKI,
        locations=[Location.AKUREYRI, Location.KEFLAVIK]
    )
}

batch_size = 1000
ids = [str(uuid4()) for _ in range(batch_size)]
providers = [Provider(random.choice(list(Provider)).value) for _ in range(batch_size)]
merchant_names = random.choices(list(merchants.keys()), k=batch_size)
transactions = [Transaction(distribution=DistributionType.NORMAL) for _ in range(batch_size)]
timestamps = [fake.date_time_between(start_date='-2y', end_date='now') for _ in range(batch_size)]
issuing_banks = [Bank(random.choice(list(Bank))).value for _ in range(batch_size)]
hashed_customer_ids = [sha256(str(uuid4()).encode()).hexdigest()[:10] for _ in range(batch_size)]
networks = [Network(random.choice(list(Network))).value for _ in range(batch_size)]
card_types = [CardType(random.choice(list(CardType))).value for _ in range(batch_size)]
reversals = [random.choices([True, False], weights=[1, 99])[0] for _ in range(batch_size)]
transaction_statuses = [TransactionStatus(random.choice(list(TransactionStatus))).value for _ in range(batch_size)]
currencies = random.choices([Currency.ISK.value, Currency.USD.value, Currency.EUR.value, Currency.GBP.value, Currency.JPY.value],
                            weights=[90, 3.33 ,3.33, 2.33, 1.34], k=batch_size)
merchant_locations = [f"{random.randint(100, 999)}" for _ in range(batch_size)]
device_types = [DeviceType(random.choice(list(DeviceType))).value for _ in range(batch_size)]
payment_methods = [PaymentMethod(random.choice(list(PaymentMethod))).value for _ in range(batch_size)]

payments_data = []
for id_, provider, transaction, timestamp, merchant_key, issuing_bank, hashed_customer_id, network, card_type, reversal, status, currency, location in zip(
    ids, providers, transactions, timestamps, merchant_names, issuing_banks, hashed_customer_ids,
    networks, card_types, reversals, transaction_statuses, currencies, merchant_locations):

    device_type = random.choice(list(DeviceType))
    payment_method = random.choice(device_type.payment_methods)

    # Find the PaymentMethod enum based on label
    payment_method_enum = next((pm for pm in PaymentMethod if pm.label == payment_method), None)
    network = random.choice(payment_method_enum.networks)
    card_type = random.choice(payment_method_enum.card_types)

    merchant = merchants[merchant_key]
    merchant_name = merchant.name
    merchant_ssn = merchant.ssn
    merchant_mcc = random.choice(merchant.mcc_codes).value
    acquiring_bank = merchant.bank.value
    merchant_location = random.choice(merchant.locations).value

    payments_data.append({
        'id': id_,
        'provider': provider.value,
        'transaction_value': transaction.value,
        'timestamp': timestamp,
        'merchant_name': merchant_name,
        'merchant_ssn': merchant_ssn,
        'merchant_mcc': merchant_mcc,
        'acquiring_bank': acquiring_bank,
        'issuing_bank': issuing_bank,
        'hashed_customer_id': hashed_customer_id[:10],
        'network': network,
        'card_type': card_type,
        'is_reversal': reversal,
        'transaction_status': status,
        'currency': currency,
        'merchant_location': merchant_location,
        'device_type': device_type.label,
        'payment_method': payment_method
    })

payment_df = pd.DataFrame(payments_data)

payment_df[['merchant_ssn', 'merchant_mcc', 'merchant_location']] = payment_df[['merchant_ssn', 'merchant_mcc', 'merchant_location']].astype('Int64')

payment_df['timestamp'] = pd.to_datetime(payment_df['timestamp'])  

output_directory = "/home/iceberg/data"
Path(output_directory).mkdir(parents=True, exist_ok=True)

# split by year and month and write to Parquet
for (year, month), group in payment_df.groupby([payment_df['timestamp'].dt.year, payment_df['timestamp'].dt.month]):
    filename = f"payments-{year}-{month:02d}.parquet"
    filepath = Path(output_directory) / filename
    group.to_parquet(filepath, index=False)