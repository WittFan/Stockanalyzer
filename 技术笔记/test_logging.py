import logging

def test1():
    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python Error')
    logging.critical('Python critical')

def test2():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Python debug')
    logging.info('Python info')
    logging.warning('Python warning')
    logging.error('Python Error')
    logging.critical('Python critical')

def test3():
    logging.basicConfig(filename='./test.log',
                        format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.DEBUG)
    logging.debug('This message should go to the logs file')
    logging.info('So should this')
    logging.warning('And this, too')

def test4():
    logger = logging.setLogger('alpha')


if __name__=='__main__':
    test3()