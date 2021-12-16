import datetime

from sqlalchemy import (Column, DateTime, String, Text,
                        create_engine)
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT
from sqlalchemy.dialects.mysql.json import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.sqltypes import Boolean
import mysql.connector

from modules import cs_config

engine = create_engine(
    "mysql://%s:%s@%s/%s" % (cs_config.mysql["user"], cs_config.mysql["password"], cs_config.mysql["host"], cs_config.mysql["database"]), future=True, echo=True)  # echo=True

Base = declarative_base()
metadata = Base.metadata



class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    email = Column(String(250))
    avatar = Column(LONGTEXT)
    password = Column(String(128))
    group = Column(INTEGER(11))
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    loginTime = Column(DateTime)
    loginToken = Column(String(128))
    settings = Column(Text)

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s')>" % (
            self.id, self.name, self.email)

    def to_dict(self):
        a = {c.name: getattr(self, c.name, None)
             for c in self.__table__.columns}
        a["group_name"] = self.group_name()
        # print(a)
        return a

    def group_name(self):
        return session.query(Group).get(self.group).name


class Group(Base):
    __tablename__ = 'groups'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(20))
    isAdmin = Column(Boolean)
    createTime = Column(DateTime)
    updateTime = Column(DateTime)

    def __repr__(self):
        return "<Group(id='%s', name='%s')>" % (
            self.id, self.name)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(250))
    description = Column(Text)
    permissions = Column(JSON)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    questions = Column(JSON)

    def __repr__(self):
        return "<Exam(id='%s', name='%s')>" % (
            self.id, self.name)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def commit():
    session.commit()


def add(*args):
    session.add(*args)
    commit()


'''
1. INSERT
cs_sql.add(User(id="1"))

2. SELECT
cs_sql.session.query(User).filter(user.name == 'name')

3. DELETE

4. UPDATE
cs_sql.session.query(User).filter(user.name == 'name')[0].name="newname"
'''



def initMysql():
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `users`(
       `userId` INT UNSIGNED AUTO_INCREMENT,
       `name` CHAR(20),
       `email` CHAR(250),
       `avatar` MEDIUMTEXT,
       `password` CHAR(128),
       `group` INT DEFAULT '1',
       `loginTime` DATETIME,
       `loginToken` CHAR(128),
       `createTime` DATETIME DEFAULT CURRENT_TIMESTAMP,
       `settings` JSON,
       PRIMARY KEY (`userId`)
    )DEFAULT CHARSET=utf8;''')
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `groups`(
       `groupId` INT UNSIGNED AUTO_INCREMENT,
       `name` CHAR(20),
       `isAdmin` BOOLEAN,
       `permissions` JSON,
       PRIMARY KEY (`groupId`)
    )DEFAULT CHARSET=utf8;''')
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `exams`(
        `examId` INT UNSIGNED AUTO_INCREMENT , 
        `name` CHAR(250) , 
        `description` TEXT , 
        `permissions` JSON , 
        `startTime` DATETIME , 
        `endTime` DATETIME , 
        `questions` JSON ,
       PRIMARY KEY (`examId`)
    )DEFAULT CHARSET=utf8;''')
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `questions`(
        `questionId` INT UNSIGNED AUTO_INCREMENT , 
        `examId` INT , 
        `type` TEXT , 
        `question` TEXT , 
        `answer` TEXT , 
        `score` FLOAT , 
       PRIMARY KEY (`questionId`)
    )DEFAULT CHARSET=utf8;''')
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `answers`(
        `answerId` INT UNSIGNED AUTO_INCREMENT , 
        `questionId` INT , 
        `userId` INT , 
        `answer` TEXT , 
        `score` FLOAT , 
       PRIMARY KEY (`answerId`)
    )DEFAULT CHARSET=utf8;''')
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `settings`(
       `key` CHAR(50),
       `value` TEXT,
       PRIMARY KEY (`key`)
    )DEFAULT CHARSET=utf8;''')
    # mysqlExecute(
    #    '''INSERT INTO `groups` (`groupId`, `name`, `isAdmin`, `permissions`) VALUES (NULL, '管理员', '1', '{}')''')
    con.commit()
    return()


# initMysql()

# INSERT INTO `exams` (`examId`, `name`, `description`, `permissions`, `startTime`, `endTime`, `questions`) VALUES (NULL, '测试114514', '描述描述描述 \r\n# 114514', '{}', '2021-12-08 18:03:40.000000', '2021-12-08 18:03:40.000000', '{}')
