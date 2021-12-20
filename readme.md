# CloudStudy - Backend

云学习后端

---

## Install

- ```bash
  pip3 install -r requirements.txt
  ```
- 编辑 `cs_config.py.example` 并删除 example 后缀
- ```bash
  python3 server.py init
  ```

## Serve

- ```bash
  python3 server.py
  ```

## APIs

> 除 1.1 , 1.2 外所有 API 都需要携带用户 cookie

### 1. 用户操作

#### 1.1 注册

/api/user/register

| params   | type | description     |
| -------- | ---- | --------------- |
| name     | str  |                 |
| email    | str  |                 |
| password | str  | password sha512 |

#### 1.2 登录

/api/user/login

| params   | type | description     |
| -------- | ---- | --------------- |
| email    | str  |                 |
| password | str  | password sha512 |

#### 1.3 获取登录信息

/api/user/checkLogin

```json
{
  "token": "str"
}
```

#### 1.4 获取用户设置

/api/user/settings/get

```json
{
    "id": int,
    "name": "str",
    "email": "str",
    "password": "str",
    "groupId": int,
    "groupName": "str",
    "createTime": int,
    "updateTime": int,
    "settings": {}
}
```

#### 1.5 更新用户设置

/api/user/settings/update

| params | type | description |
| ------ | ---- | ----------- |
| data   | json |             |

### 2. 后台设置

#### 2.1 站点设置

#### 2.2 用户组

##### 2.2.1 获取用户组列表

/api/admin/groups/get

```json
{
    "groups": [
        {
            "id": int,
            "name": "str",
            "isAdmin": bool
        }
    ]
}
```

##### 2.2.2 添加用户组

/api/admin/groups/add

| params | type | description |
| ------ | ---- | ----------- |
| name   | str  |             |

##### 2.2.3 删除用户组

/api/admin/groups/delete

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.2.4 获取某用户组详细信息

/api/admin/groups/detail/get

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.2.5 更新某用户组详细信息

/api/admin/groups/detail/update

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |
| data   | json |             |

#### 2.3 用户

##### 2.3.1 获取用户列表

/api/admin/users/get

```json
{
    "users": [
        {
            "id": int,
            "name": "str",
            "email": "str",
            "groupId": int,
            "groupName": "str",
            "recentLogin": int
        }
    ]
}
```

##### 2.3.2 添加用户

/api/admin/users/add

| params   | type | description |
| -------- | ---- | ----------- |
| name     | str  |             |
| email    | str  |             |
| password | str  | sha512      |
| group    | int  |             |

##### 2.3.3 删除用户

/api/admin/users/delete

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.3.4 获取某用户详细信息

/api/admin/users/detail/get

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.3.5 更新某用户详细信息

/api/admin/users/detail/update

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |
| data   | json |             |

#### 2.4 考试

##### 2.4.1 获取考试列表

/api/admin/exams/get

##### 2.4.2 添加考试

/api/admin/exams/add

##### 2.4.3 删除考试

/api/admin/exams/delete

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.4.4 获取某考试详细信息

/api/admin/exams/detail/get

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.4.5 更新某考试详细信息

/api/admin/exams/detail/update

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |
| data   | json |             |

##### 2.4.6 获取某考试题目信息

/api/admin/exams/questions/get

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.4.6 获取某题目详情

/api/admin/exams/questions/datail/get

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |

##### 2.4.6 更新某题目详情

/api/admin/exams/questions/datail/update

| params | type | description |
| ------ | ---- | ----------- |
| id     | int  |             |
| data   | json |             |
