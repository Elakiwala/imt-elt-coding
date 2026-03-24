import pandas as pd
import pytest
from unittest.mock import patch

from src.transform import (
    _drop_internal_columns,
    transform_products,
    transform_users,
    transform_orders,
)

class TestDropInternalColumns:
    """Tests for the _drop_internal_columns() helper."""

    def test_remove_internal_columns(self, sample_products):
        df = _drop_internal_columns(sample_products)

        # vérifier que les colonnes avec "_" sont supprimées
        assert "_internal_cost_usd" not in df.columns
        assert "_supplier_id" not in df.columns

    def test_keep_normal_columns(self, sample_products):
        df = _drop_internal_columns(sample_products)

        # vérifier que les colonnes normales restent
        assert "product_id" in df.columns
        assert "brand" in df.columns

    def test_empty_df(self):
        df = pd.DataFrame()
        result = _drop_internal_columns(df)

        # si dataframe vide → doit rester vide
        assert result.empty


class TestTransformProducts:
    """Tests pour transform_products()"""

    @patch("src.transform._load_to_silver")   # on mock l'écriture BDD
    @patch("src.transform._read_bronze")      # on mock la lecture BDD
    def test_remove_invalid_prices(self, mock_read, mock_load, sample_products):
        # on injecte un faux dataframe
        mock_read.return_value = sample_products

        result = transform_products()

        # vérifier que les prix <= 0 sont supprimés
        assert (result["price_usd"] > 0).all()

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_tags_clean(self, mock_read, mock_load, sample_products):
        mock_read.return_value = sample_products

        result = transform_products()

        # vérifier que "|" est remplacé par ", "
        assert all("|" not in tag for tag in result["tags"])

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_boolean_columns(self, mock_read, mock_load, sample_products):
        mock_read.return_value = sample_products

        result = transform_products()

        # vérifier que les colonnes sont bien en bool
        assert result["is_active"].dtype == bool
        assert result["is_hype_product"].dtype == bool

class TestTransformUsers:
    """Tests pour transform_users()"""

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_remove_pii(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users

        result = transform_users()

        # vérifier suppression des colonnes sensibles
        assert "_hashed_password" not in result.columns
        assert "_last_ip" not in result.columns
        assert "_device_fingerprint" not in result.columns

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_fill_loyalty(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users

        result = transform_users()

        # vérifier que les None deviennent "none"
        assert "none" in result["loyalty_tier"].values

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_email_clean(self, mock_read, mock_load, sample_users):
        mock_read.return_value = sample_users

        result = transform_users()

        # vérifier lower + strip
        assert all(email == email.strip().lower() for email in result["email"])

class TestTransformOrders:
    """Tests pour transform_orders()"""

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_remove_invalid_status(self, mock_read, mock_load, sample_orders):
        mock_read.return_value = sample_orders

        result = transform_orders()

        # vérifier que status invalide est supprimé
        assert "invalid_status" not in result["status"].values

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_date_format(self, mock_read, mock_load, sample_orders):
        mock_read.return_value = sample_orders

        result = transform_orders()

        # vérifier conversion en datetime
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])

    @patch("src.transform._load_to_silver")
    @patch("src.transform._read_bronze")
    def test_coupon_fill(self, mock_read, mock_load, sample_orders):
        mock_read.return_value = sample_orders

        result = transform_orders()

        # vérifier que les None sont remplacés
        assert result["coupon_code"].isna().sum() == 0