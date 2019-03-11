

import os



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MY_CMDB.settings")
    import django
    django.setup()

    from eye.backend import main


    obj = main.HostManager()
    obj.interactive()
