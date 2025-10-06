from pickletools import stackslice
import time
from venv import logger
import requests
import logging
from django.conf import settings
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ProductService:
    @staticmethod
    def get_product(product_id: int) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(
                f"{settings.PRODUCT_SERVICE_URL}/api/products/{product_id}/", timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch product with ID {product_id}: {e}")
            return None

    @staticmethod
    def check_availability(product_id: int, quantity: int) -> bool:
        try:
            response = requests.get(
                f"{settings.PRODUCT_SERVICE_URL}/api/products/{product_id}/check-availability/",
                timeout=10,
                params={"quantity": quantity},
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("available", False)
            return False

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Failed to check availability of product with ID {product_id}: {e}"
            )
            return False


class UserService:
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/api/users/profile/",
                timeout=10,
                headers=headers,
            )
            if response.status_code == 200:
                return response.json()
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch user with token {token}: {e}")
            return None
