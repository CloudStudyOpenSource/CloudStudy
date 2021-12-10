import mysql.connector
from modules import cs_config


def connectMysql():
    global con
    global cur
    con = mysql.connector.connect(**cs_config.mysql)
    cur = con.cursor(buffered=True)
    print("Connected to Mysql Server")


def mysqlExecute(*args):
    #print(*args)
    try:
        cur.execute(*args)
    except:
        print("Err: Lost connection to Mysql Server. Reconnecting...")
        try:
            cur.close()
            con.close()
        except:
            pass
        connectMysql()
        cur.execute(*args)


def initMysql():
    mysqlExecute('''CREATE TABLE IF NOT EXISTS `users`(
       `userId` INT UNSIGNED AUTO_INCREMENT,
       `name` CHAR(20),
       `email` CHAR(250),
       `avatar` JSON,
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


initMysql()

#INSERT INTO `exams` (`examId`, `name`, `description`, `permissions`, `startTime`, `endTime`, `questions`) VALUES (NULL, '测试114514', '描述描述描述 \r\n# 114514', '{}', '2021-12-08 18:03:40.000000', '2021-12-08 18:03:40.000000', '{}')
