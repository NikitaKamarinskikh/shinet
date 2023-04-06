from enum import Enum


class UsersStatuses(Enum):
    BLOCKED = 'Blocked 🔴'
    ACTIVE = 'Active 🟢'


class UsersRoles(Enum):
    CLIENT = 'client'
    MASTER = 'master'


