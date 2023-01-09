""" 
Documentation of studies

# Imports libraries
# Create the declarative base
# Create the classes
# Create the tables for classes and their columns
# All classes need a table name
# I need to create the relationships so the classes can communicate

"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float

Base = declarative_base()

class Client(Base):
    __tablename__ = "client_bank"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    fullname = Column(String(60))
    cpf = Column(String(11), nullable=False)
    address = Column(String, nullable=False)

    account = relationship("Account", back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Client(id={self.id}, name={self.name}, cpf={self.cpf}, address={self.address})"

class Account(Base):
    __tablename__ = "client_account"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    agencia = Column(String(4), nullable=False)
    numero = Column(Integer, nullable=False)
    saldo = Column(Float)
    client_id = Column(Integer, ForeignKey("client_bank.id"), nullable=False)

    client = relationship("Client", back_populates="account")

    def __repr__(self):
        return f"Account(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, numero={self.numero}, saldo={self.saldo})"
        
engine = create_engine("sqlite://")

# Creating the classes as tables in the database
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)

print(inspetor_engine.get_table_names())

with Session(engine) as session:
    felipe = Client(
        name='felipe',
        fullname='Felipe Lamas',
        cpf='05355206112',
        address='Rio de Janeiro, Realengo',
        account=[Account(tipo="conta-corrente", agencia="0001", numero=21334562, saldo=500.0)]
    )

    gabriela = Client(
        name='gabriela',
        fullname='Gabriela Bastos',
        cpf='01182294025',
        address='Rio de Janeiro, Bangu',
        account=[Account(tipo="conta corrente", agencia="0001", numero=25263788, saldo=432.25)]
    )

    craudia = Client(
        name='craudia',
        fullname='Craudia du Framengo',
        cpf='01178596283',
        address='Rio de Janeiro, Bangu',
        account=[Account(tipo="conta corrente", agencia="0001", numero=25263785, saldo=300.0)]
    )


    session.add_all([felipe, gabriela])

    session.commit()

stmt = select(Client).where(Client.name.in_(['felipe']))

print()

for client in session.scalars(stmt):
    print(client)

print()

stmt_account = select(Account).where(Account.client_id.in_([1]))
for account in session.scalars(stmt_account):
    print(account)

print()

stmt_order = select(Client).order_by(Client.fullname.desc())
for result in session.scalars(stmt_order):
    print(result)

print()

stmt_join = select(Client.fullname, Account.saldo).join_from(Account, Client)

connection = engine.connect()

results = connection.execute(stmt_join).fetchall()
for result in results:
    print(result)

print()

stmt_count = select(func.count('*')).select_from(Client)
for result in session.scalars(stmt_count):
    print(result)