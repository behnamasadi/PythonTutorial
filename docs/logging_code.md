### logging

```
import logging 
print(dir(logging))  
```
- Entries with all caps are constant i.e.: `BASIC_FORMAT`
- Entries starting with capitalized items are classes i.e.: `BufferingFormatter`
- Entries starting with lower case are methods i.e: `addLevelName`

###Levels
Numeric Values: 
- Notset: 0
- Debug: 10
- Info: 20
- Warning: 30
- Error: 40
- Critical: 50


Create and configuring logger

```
LOG_FORMAT="%(levelname)s %(asctime)s -%(message)s"
logging.basicConfig(filename="data/logging_file.log", level=logging.DEBUG, format=LOG_FORMAT, filemode='w')
logger=logging.getLogger()
```

### print(logger.level)
```
logger.info("some info")
logger.debug("some debug")
logger.warning("some warning")
logger.error("some error")
logger.critical("some critical")
```


[code](../Tutorials/logging_code.py)  
