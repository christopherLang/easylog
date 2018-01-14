import logging


class Easylog:
    def __init__(self, loggername=None, globallevel='info',
                 create_console=True, dateformat=None):
        self._handlers = list()
        self._loggername = __name__ if loggername is None else loggername
        self._globallevel = _string2loglevel(globallevel)
        self._filecounter = 0
        self._namecounters = {'file': 0, 'console': 0}
        self._dateformats = {'file': "%Y-%m-%dT%H:%M:%S",
                             'console': "%I:%M:%S %p"}
        self._lognames = list()

        # logging.basicConfig(level=logging.DEBUG)
        self._logger = logging.getLogger(self._loggername)
        self._logger.setLevel(logging.DEBUG)

        if create_console is True:
            self.add_consolelogger()

    @property
    def handlers(self):
        return self._handlers

    @property
    def globallevel(self):
        return self._globallevel

    @property
    def logger(self):
        return self._logger

    @property
    def dateformats(self):
        return self._dateformats

    def _log_controls(self, logtype, logname=None, loglevel=None,
                      logformat=None, dateformat=None):
        if logname is None:
            logname = logtype + str(self._namecounters[logtype])
            self._namecounters[logtype] += 1
        else:
            if logname in self.handler_names():
                raise ValueError("Log name {0} already in use".format(logname))

        if loglevel is None:
            loglevel = self._globallevel

        if logformat is None:
            logformat = _default_log_format(logtype)

        if dateformat is None:
            dateformat = self._dateformats[logtype]

        logformat = logging.Formatter(logformat, dateformat)

        log_controls = {'logtype': logtype, 'logname': logname,
                        'loglevel': loglevel, 'logformat': logformat,
                        'dateformat': dateformat}

        return log_controls

    def _add_logger(self, log_handler, log_controls):
        log_handler.setLevel(log_controls['loglevel'])
        log_handler.setFormatter(log_controls['logformat'])

        self._logger.addHandler(log_handler)

        log_rec = _logger_record(log_handler, log_controls['logname'],
                                 log_controls['logtype'],
                                 log_controls['loglevel'],
                                 log_controls['dateformat'])

        self._handlers.append(log_rec)

    def add_consolelogger(self, logname=None, loglevel=None, logformat=None,
                          stream=None, dateformat=None):
        log_controls = self._log_controls('console', logname, loglevel,
                                          logformat, dateformat)
        log_handler = logging.StreamHandler(stream=stream)

        self._add_logger(log_handler, log_controls)

    def add_filelogger(self, logpath, logname=None, loglevel=None,
                       logformat=None, dateformat=None, encoding='utf-8',
                       mode='a', delay=False):
        log_controls = self._log_controls('console', logname, loglevel,
                                          logformat, dateformat)
        log_handler = logging.FileHandler(logpath, mode, encoding, delay)

        self._add_logger(log_handler, log_controls)

    def set_logformat(self, handlername, fmt, dateformat=None):
        if self._handlers:
            errmsg = "No Logging Handlers have been defined"
            raise NoDefinedHandlersError(errmsg)
        else:
            handler_records = [a_handler for a_handler in self._handlers
                               if a_handler['name'] == handlername]

            if handler_records:
                errmsg = "No handler of the name '{0}' was found"
                errmsg = errmsg.format(handlername)

                raise NoHandlersFoundError(errmsg)
            else:
                handler_rec = handler_records[0]

                if dateformat is None:
                    dateformat = handler_rec['dateformat']

                fmt = logging.Formatter(fmt, dateformat)
                handler_records['handler'].setFormatter(fmt)

    def handler_names(self):
        result = [a_logger['name'] for a_logger in self._handlers]

        return result

    def log_critical(self, msg):
        self._logger.critical(msg)

    def log_error(self, msg):
        self._logger.error(msg)

    def log_warning(self, msg):
        self._logger.warning(msg)

    def log_info(self, msg):
        self._logger.info(msg)

    def log_debug(self, msg):
        self._logger.debug(msg)


def _default_log_format(handlertype):
    handler_format = None

    if handlertype == 'console':
        handler_format = '%(levelname)s - %(message)s'
    elif handlertype == 'file':
        handler_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    elif handlertype == 'module':
        handler_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    return handler_format


def _string2loglevel(loglevel):
    logging_object_level = None

    loglevel = loglevel.lower()

    if loglevel == "critical":
        logging_object_level = logging.CRITICAL
    elif loglevel == "error":
        logging_object_level = logging.ERROR
    elif loglevel == "warning":
        logging_object_level = logging.WARNING
    elif loglevel == "info":
        logging_object_level = logging.INFO
    elif loglevel == "debug":
        logging_object_level = logging.DEBUG
    else:
        levels = "'critical', 'error', 'warning', 'info', 'debug'"
        msg = "'loglevel' must be one of: " + levels
        raise ValueError(msg)

    return logging_object_level


def _logger_record(handler, name, loggertype, loglevel, dateformat):
        record = {'handler': handler, 'name': name, 'loggertype': loggertype,
                  'loglevel': loglevel, 'dateformat': dateformat}

        return record


class Error(Exception):
    """Base class for exceptions in Easylog"""
    pass


class NoDefinedHandlersError(Error):
    """Exception raised there are no Logging Handlers defined in Easylog

    Raised only when there is attempt to modify a handler

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = "No Logging Handlers have been defined"


class NoHandlersFoundError(Error):
    """Exception raised there are no Logging Handlers found

    Raised only when there is attempt to modify a handler

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
