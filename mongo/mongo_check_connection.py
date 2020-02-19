import time
import logging
import pymongo
import urllib.parse
log = logging.getLogger(__name__)

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
            _name = urllib.parse.quote_plus(name)
            _password = urllib.parse.quote_plus(password)
            client = pymongo.MongoClient(f'mongodb://{name}:{password}@{host}:{port}',
                                         serverSelectionTimeoutMS=timeout)

            info = client.server_info()
            if print_dbg:
                print('client.server_info() ', info)
        except Exception as e:
            print('timeout', tentativo_num)
            log.warning("Error connecting to mongo, will retry in 1 sec: %r",
                        e)
            time.sleep(sleep)
        else:
            return True

    else:
        print(('Unable to connect'))
        return False

if __name__ == '__main__':
    if mongo_check_connection():
        print('ok')
    else:
        print('failed')
