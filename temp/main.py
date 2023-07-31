import time

class foo:
    def __enter__(self):
        print(time.time())
        time.sleep(2)
        return

    def __exit__(self):
        print(time.time())
        return
    

foo fee() 