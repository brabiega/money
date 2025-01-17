#!/usr/bin/python
# -*- coding: utf-8 -*-

#
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ConfigParser
import argparse
import models

#
CONFIG_FILE = '/etc/money/money.cfg'

parser = argparse.ArgumentParser()
parser.add_argument('--env', help='environment to use', default='test')
parser.add_argument('--drop', help='drop existing tables',
                    action='store_true', default=False)
args = parser.parse_args()

config = ConfigParser.SafeConfigParser()
config.read(CONFIG_FILE)

DB_ENDPOINT = config.get(args.env, 'db_uri')


# database engine
engine = create_engine(DB_ENDPOINT, echo=False)

if args.drop:
    models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
s = Session()

pawel = models.User(login='pawel', password='tajne_haslo_do_bazy', email='money@example.com')
s.add(pawel)

s.add(models.AccountType(name='current', sort=1, group=1000))
s.add(models.AccountType(name='debit', sort=2, group=1000))
s.add(models.AccountType(name='credit card', sort=3, group=1000))
s.add(models.AccountType(name='loan', sort=4, group=1000))
s.add(models.AccountType(name='savings', sort=5, group=2000))
s.add(models.AccountType(name='rainy day', sort=6, group=8000))
s.add(models.AccountType(name='money to burn', sort=7, group=9000))
s.commit()
