from .utils import get_db_handle, get_hamilton_db_handle, get_tauranga_db_handle

MONGO_CLIENT = get_db_handle()
HAMILTON_MONGO_CLIENT = get_hamilton_db_handle()
TAURANGA_MONGO_CLIENT = get_tauranga_db_handle()