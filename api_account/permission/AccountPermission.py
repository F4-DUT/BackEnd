from api_account.contants import RoleData
from api_base.permission import MyBasePermission


class AdminOrManagerPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN, RoleData.MANAGER]


class EmployeePermission(MyBasePermission):
    match_any_roles = [RoleData.EMPLOYEE]


class ManagerPermission(MyBasePermission):
    match_any_roles = [RoleData.MANAGER]


class AdminPermission(MyBasePermission):
    match_any_roles = [RoleData.ADMIN]