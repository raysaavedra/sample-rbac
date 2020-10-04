from rolepermissions.roles import AbstractUserRole


class BoardAdmin(AbstractUserRole):
    available_permissions = {
        'add_board': True,
        'change_board': True,
        'delete_board': True,
        'view_board': True,
        'add_thread': True,
        'change_thread': True,
        'delete_thread': True,
        'view_thread': True,
        'add_post': True,
        'change_post': True,
        'delete_post': True,
        'view_post': True,
        'add_moderator': True,
        'remove_moderator': True,
    }


class BoardModerator(AbstractUserRole):
    available_permissions = {
        'view_board': True,
        'add_thread': True,
        'change_thread': True,
        'view_thread': True,
        'add_post': True,
        'change_post': True,
        'view_post': True,
    }


class ThreadAdmin(AbstractUserRole):
    available_permissions = {
        'view_board': True,
        'add_thread': True,
        'change_thread': True,
        'view_thread': True,
        'delete_thread': True,
        'add_post': True,
        'change_post': True,
        'view_post': True,
        'delete_post': True,
    }

