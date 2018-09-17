import logging
from test_run.runnerBase import TestInterfaceCase as te


class StartEnd(te):
    def setUp(self):
        logging.info('=====setUp====')
        super(StartEnd, self).setUp()

    def tearDown(self):
        logging.info('====tearDown====')
        self.driver.close_app()
        self.driver.quit()
        pass

    # @classmethod
    # def setUpClass(cls):
    #     logging.info('=====setUp====')
    #     super(StartEnd, cls).setUpClass()

    @staticmethod
    def tearDownClass():
        pass
