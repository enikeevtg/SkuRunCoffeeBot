from decouple import config
admins_list = [int(admin_id) for admin_id in config('ADMINS').split(',')]
