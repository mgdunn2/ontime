import sqlite3

def transaction(sql_file):
    def transaction_decorator(func):
        def new_func(*args, **kwargs):
            connection = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES)
            cursor = connection.cursor()
            try:
                retval = func(cursor, *args, **kwargs)
                connection.commit()
            except:
                connection.rollback()
                raise
            finally:
                cursor.close()
                connection.close()
            return retval
        new_func.__name__ = func.__name__
        new_func.__doc__ = func.__doc__
        return new_func
    return transaction_decorator
