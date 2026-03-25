import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.transform import (
    _drop_internal_columns,
    transform_products,
    transform_users,
    transform_orders,
)


class TestDropInternalColumns:
    """Tests for the _drop_internal_columns() helper."""
    # Test that columns starting with '_' are removed
    def test_supprimer_underscore_colonnes(self):
        exemple = {"col1": [1, 2, 3], "col2": ["a", "b", "c"], "_internal_col": [1, 2, 3]}
        df = pd.DataFrame(exemple)
        sans_underscore = _drop_internal_columns(df)
        assert "_internal_col" not in sans_underscore.columns
        assert "col1" in sans_underscore.columns
        assert "col2" in sans_underscore.columns

    # Test that regular columns are kept
    def test_conserver_colonnes_normales(self):
        exemple = {"film": ["Fast and Furious", "The Matrix", "Dune 3"], "serie": ["Outlander", "The Walking Dead", "The Witcher"]}
        df = pd.DataFrame(exemple)
        resultat = _drop_internal_columns(df)
        assert list(resultat.columns) == ["film", "serie"]

    # Test edge case: empty DataFrame
    def test_dataframe_vide(self):
        df = pd.DataFrame()
        resultat = _drop_internal_columns(df)
        assert list(resultat.columns) == []


class TestTransformProducts:
    """Tests for transform_products()."""
    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")

    # Test that invalid prices (<=0) are removed
    def test_supprimer_prix_invalides(self, mock_load, mock_read, sample_products):
        mock_read.return_value = sample_products
        transform_products()
        df_charge = mock_load.call_args[0][0]  
        assert all(df_charge["price_usd"] > 0)


    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that tags are normalized ('|' replaced with ', ')
    def test_normaliser_tags(self, mock_load, mock_read, sample_products):
        mock_read.return_value = sample_products
        transform_products()
        df_charge = mock_load.call_args[0][0]  
        assert "|" not in df_charge["tags"].values[0]
        assert ", " in df_charge["tags"].values[0]
    
    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that boolean columns are converted
    def test_convertir_booleans(self, mock_load, mock_read, sample_products):
        mock_read.return_value = sample_products
        transform_products()
        df_charge = mock_load.call_args[0][0]  
        assert "is_active" in df_charge.columns
        assert "is_hype_product" in df_charge.columns
        assert df_charge["is_active"].dtype == bool
        assert df_charge["is_hype_product"].dtype == bool


class TestTransformUsers:
    """Tests for transform_users()."""
    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that PII columns (_hashed_password, _last_ip, etc.) are removed
    # PII = ["_hashed_password", "_last_ip", "email", "first_name", "last_name", "phone"]
    def test_supprimer_colonnes_pii(self, mock_load, mock_read, sample_users):
        mock_read.return_value = sample_users
        transform_users()
        df_charge = mock_load.call_args[0][0]  
        for col in ["_hashed_password", "_last_ip"]:
            assert col not in df_charge.columns
        assert "_hashed_password" not in df_charge.columns
        assert "_last_ip" not in df_charge.columns

    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that NULL loyalty_tier is filled with 'none'
    def test_remplir_loyalty_tier(self, mock_load, mock_read, sample_users):
        mock_read.return_value = sample_users
        transform_users()
        df_charge = mock_load.call_args[0][0]  
        assert df_charge["loyalty_tier"].values[0] == "gold"
        assert df_charge["loyalty_tier"].values[1] == "none"

    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that emails are lowercased and stripped
    def test_normaliser_emails(self, mock_load, mock_read, sample_users):
        df = pd.DataFrame({
            "email": ["  eva.lansalot@imt-atlantique.net "],
            "loyalty_tier": ["gold"],
        })
        mock_read.return_value = df
        transform_users()
        df_charge = mock_load.call_args[0][0]
        assert df_charge["email"].values[0] == "eva.lansalot@imt-atlantique.net"


class TestTransformOrders:
    """Tests for transform_orders()."""
    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that invalid statuses are flagged/removed
    def test_gérer_statuts_invalides(self, mock_load, mock_read, sample_orders):
        mock_read.return_value = sample_orders
        transform_orders()
        df_charge = mock_load.call_args[0][0]  
        #assert "invalid_status" in df_charge.columns
        assert "invalid_status" not in df_charge["status"].values


    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that order_date is converted to datetime
    def test_convertir_order_date(self, mock_load, mock_read, sample_orders):
        mock_read.return_value = sample_orders
        transform_orders()
        df_charge = mock_load.call_args[0][0]  
        assert not isinstance(df_charge["order_date"].values[0], str)

    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that NULL coupon_code is replaced with ''
    def test_remplir_coupon_code(self, mock_load, mock_read, sample_orders):
        mock_read.return_value = sample_orders
        transform_orders()
        df_charge = mock_load.call_args[0][0]  
        assert None not in df_charge["coupon_code"].values
        assert "" in df_charge["coupon_code"].values
