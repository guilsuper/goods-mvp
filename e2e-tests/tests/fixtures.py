# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy import text


load_dotenv()


DB_URI = os.environ["DB_URI"]
engine = create_engine(DB_URI)


@pytest.fixture
def driver():
    """Selenium driver fixture."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def sctr_create():
    """Creates an SCTR using raw query to the DB."""
    def create(company_id):
        """Creates an SCTR an link it to company."""
        sctr = {
            "id": 1,
            "unique_identifier": "asd",
            # It's SKU type
            "unique_identifier_type": "1",
            "marketing_name": "asdd",
            "version": "1",
            # Published state
            "state": "2",
            "cogs": "100",
            "company_id": company_id,
            "is_latest_version": "t"
        }
        stmt = f"""
            INSERT INTO api_sctr VALUES
            {tuple(sctr.values())}
        """
        with engine.connect() as conn:
            conn.execute(text(stmt))
            conn.commit()
            return sctr

    return create


@pytest.fixture
def company_create():
    """Creates a company using raw query to the DB."""
    def create():
        """Creates a company."""
        company = {
            "id": 2,
            "website": "aaaa11.com",
            "name": "aaa11",
            "jurisdiction": "ggggg",
            "company_unique_identifier": "kjkjkj",
            "slug": "aaa11"
        }
        stmt = f"""
            INSERT INTO api_company VALUES
            {tuple(company.values())}
        """
        with engine.connect() as conn:
            conn.execute(text(stmt))
            conn.commit()
            return company

    return create


@pytest.fixture
def component_create():
    """Creates an component using raw query to the DB."""
    def create(sctr_id):
        """Creates an component an link it to sctr."""
        component = {
            "id": 1,
            "fraction_cogs": "100",
            "marketing_name": "asdqwe",
            # It's Externally Sourced type
            "component_type": "1",
            "country_of_origin": "AG",
            "external_sku": "daqwe",
            "parent_sctr_id": sctr_id,
            "company_name": "qwezc"
        }
        stmt = f"""
            INSERT INTO api_sourcecomponent VALUES
            {tuple(component.values())}
        """
        with engine.connect() as conn:
            conn.execute(text(stmt))
            conn.commit()
            return component

    return create
