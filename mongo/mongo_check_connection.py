import time
import logging
from pymongo import MongoClient, errors
from mongoengine import OperationError
import urllib.parse
log = logging.getLogger(__name__)

class MultiMongoErrs(Exception):
    def __init__(self, _type=None):
        super(MultiMongoErrs, self).__init__(_type)
        self._type = _type
        if _type == 'auth':
            self.message = 'Autentication Failure'
        elif _type == 'offline':
            self.message = 'Server offline'
        else:
            if type(_type) is str:
                self.message = _type
            else:
                self.message = 'Unknow error'


def mongo_check_connection(database='test_db',
                           host='localhost',
                           port=27017,
                           name='admin',
                           password ='admin',
                           timeout=1000,
                           print_dbg=False,
                           tentativi=5,
                           sleep=1):
    """Creates a test connection for to check if the host is on-line
        :returns True if connection has been established, False otherwise"""
    for tentativo_num in range(tentativi):
        try:
            client = MongoClient(f'mongodb://{name}:{password}@{host}:{port}',
                                         serverSelectionTimeoutMS=timeout)
            client[database].authenticate(name=name, password=password)
            client[database].list_collection_names()
            info = client.server_info()
            if print_dbg:
                print('client.server_info() ', info)
        except errors.OperationFailure:
            # print('spento')
            raise MultiMongoErrs('auth')
        except OperationError:
            print('OperationError')
            raise MultiMongoErrs()


        except errors.ServerSelectionTimeoutError:
            e = 'error 2'
            print('timeout', tentativo_num)
            log.warning("Error connecting to mongo, will retry in 1 sec: %r",
                        e)
            time.sleep(sleep)
        else:
            return True

    else:
        print(('Unable to connect'))
        raise MultiMongoErrs('offline')

if __name__ == '__main__':
    if mongo_check_connection():
        print('ok')
    else:
        print('failed')
