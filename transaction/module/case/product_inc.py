from .base import BaseCase
from module.database import get_connection
import module.database.product as pd

class CheckSleep(BaseCase):
    def _get_routines(self):
        return [self._1, self._2]

    def _1(self):
        self._sleep(10)

    def _2(self):
        self._sleep(10)
               
class CheckUpdateAtomicity(BaseCase):
    id = 1
    name = 'coke'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _close(self, conn):
        product = pd.select_product_by_id(conn, self.id)
        self._logger.info(f'{self.__class__.__name__}: Got product {product}')
        pd.delete_product(conn, self.id)

    def _get_routines(self):
        return [self._increment_1000, self._increment_1000]

    def _increment_1000(self):
        with get_connection() as conn:
            for i in range(1000):
                pd.increment_product(conn, self.id)

class CheckRepeatableRead(BaseCase):
    id = 2
    name = 'pen'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _get_routines(self):
        return [self._select_sleep_select, self._delete_product_after_sleep]

    def _select_sleep_select(self):
        with get_connection() as conn:
            conn.begin()
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" at the first select')
            self._sleep(5)
            # get None when commited here
            conn.commit()
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after 5 second')
            # still have product due to REPEATABLE READ
            #conn.commit()

    def _delete_product_after_sleep(self):
        with get_connection() as conn:
            self._logger.info(f'Start sleep...')
            self._sleep(3)
            self._logger.info(f'Wake up and delete product')
            pd.delete_product(conn, self.id)
            self._logger.info(f'Product deleted')
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Select Product again and got "{product}"')

class CheckUpdateWithoutSelectForUpdate(BaseCase):
    id = 3
    name = 'apple'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _get_routines(self):
        return [self._select_sleep_update, self._delete_product_after_sleep]

    def _select_sleep_update(self):
        with get_connection() as conn:
            conn.begin()
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" at the first select')
            self._sleep(5)
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" before update')
            
            pd.update_product_total(conn, self.id, 50)
            self._logger.info(f'Product updated')

            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after update')
            
            conn.commit()
            self._logger.info(f'Commited')
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after commit')

    def _delete_product_after_sleep(self):
        with get_connection() as conn:
            self._logger.info(f'Start sleep...')
            self._sleep(3)
            self._logger.info(f'Wake up and delete product')
            pd.delete_product(conn, self.id)
            self._logger.info(f'Product deleted')
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Select Product again and got "{product}"')

class CheckSelectForUpdate(BaseCase):
    id = 4
    name = 'orange'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _get_routines(self):
        return [self._select_sleep_update, self._delete_product_after_sleep]

    def _select_sleep_update(self):
        with get_connection() as conn:
            conn.begin()
            product = pd.select_product_for_update_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" at select for update')
            self._sleep(5)
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" before update')
            
            pd.update_product_total(conn, self.id, 50)
            self._logger.info(f'Product updated')

            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after update')
            
            conn.commit()
            self._logger.info(f'Commited')
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after commit')

    def _delete_product_after_sleep(self):
        with get_connection() as conn:
            self._logger.info(f'Start sleep...')
            self._sleep(3)
            self._logger.info(f'Wake up and delete product')
            pd.delete_product(conn, self.id)
            self._logger.info(f'Product deleted')
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Select Product again and got "{product}"')

class CheckUpdateWithSelectForShare(BaseCase):
    id = 5
    name = 'pie'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _close(self, conn):
        pd.delete_product(conn, self.id)

    def _get_routines(self):
        return [self._select_sleep_update, self._delete_product_after_sleep]

    def _select_sleep_update(self):
        with get_connection() as conn:
            conn.begin()
            # When using for share, another thread will get deadlock exception
            # https://stackoverflow.com/questions/32827650/mysql-innodb-difference-between-for-update-and-lock-in-share-mode
            product = pd.select_product_for_share_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" at select for share')
            self._sleep(5)
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" before update')
            
            pd.update_product_total(conn, self.id, 50)
            self._logger.info(f'Product updated')

            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after update')
            
            conn.commit()
            self._logger.info(f'Commited')
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after commit')

    def _delete_product_after_sleep(self):
        with get_connection() as conn:
            self._logger.info(f'Start sleep...')
            for i in range(3):
                self._sleep(1)
                product = pd.select_product_by_id(conn, self.id)
                self._logger.info(f'Select Product and got "{product}"')
            self._logger.info(f'Wake up and delete product')
            pd.delete_product(conn, self.id)
            self._logger.info(f'Product deleted')
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Select Product again and got "{product}"')

class CheckSelectForUpdateOtherRead(BaseCase):
    id = 6
    name = 'book'
    total = 0

    def _setup(self, conn):
        pd.create_product_table(conn)
        pd.insert_product(conn, self.id, self.name, self.total)

    def _get_routines(self):
        return [self._select_sleep_update, self._read_after_sleep]

    def _select_sleep_update(self):
        with get_connection() as conn:
            conn.begin()
            product = pd.select_product_for_update_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" at select for update')
            
            self._sleep(5)

            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" before update')
            
            pd.update_product_total(conn, self.id, 50)
            self._logger.info(f'Product updated')

            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after update')
            
            conn.commit()
            self._logger.info(f'Commited')
            
            product = pd.select_product_by_id(conn, self.id)
            self._logger.info(f'Got product "{product}" after commit')

    def _read_after_sleep(self):
        self._logger.info(f'Start sleep...')
        self._sleep(2)
        with get_connection() as conn:
            self._logger.info(f'Begin after sleep')
            #conn.begin()
            for i in range(10):
                self._sleep(1)
                # Actually we can read the row even using FOR UPDATE !?
                product = pd.select_product_by_id(conn, self.id)
                self._logger.info(f'Select Product and got "{product}"')
                # we still read old value if we do not commit
                #conn.commit()
