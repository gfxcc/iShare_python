#
# created by Yong Cao at May/2/2017
# this is a python version of iShare server
#
#


from concurrent import futures
import time

import grpc

import iShare_pb2
import iShare_pb2_grpc
import iShare_log

import iShare_mysql

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(iShare_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return iShare_pb2.HelloReply(message='Hello, %s!' % request.name)

    def Sign_up(self, request, context):
        log = iShare_log.Log('Sign_up')
        log.omit_syntax()

        cursor = iShare_mysql.db.cursor()
        cursor.execute('SELECT user_id FROM User WHERE username = \'' + request.username + '\'');
        iShare_mysql.db.commit()

        if int(cursor.rowcount) != 0:
            # username has been used
            return iShare_pb2.Reply_inf(status='CANCELLED',
                                        information="Sorry, your username has beed used. Please change username.")

        # INSERT
        cursor = iShare_mysql.db.cursor()
        cursor.execute('INSERT INTO User (username, password, email) VALUES (\'' +
                       request.username + '\', \'' + request.password + '\', \'' +
                       request.email + '\')')
        iShare_mysql.db.commit()

    def Send_DeviceToken(self, request, context):
        log = iShare_log.Log('Send_DeviceToken')
        log.omit_syntax()

        cursor = iShare_mysql.db.cursor()
        cursor.execute('UPDATE User SET deviceToken = \'' + request.content(1) +
                       '\' WHERE user_id = ' + request.content(0))
        iShare_mysql.db.commit()
        return iShare_pb2.Inf(information='OK')

    def Obtain_bills(self, request, context):
        log = iShare_log.Log('Obtain_bills')
        log.omit_syntax()

        cursor = iShare_mysql.db.cursor()
        if request.amount == 'all':
            cursor.execute('SELECT * FROM Bills WHERE member_0 = ' + request.username + ' OR member_1 = '
            + request.username + ' OR member_2 = ' + request.username + ' OR member_3 = ' + request.username +
            ' OR member_4 = ' + request.username + ' OR member_5 = ' + request.username + " OR member_6 = " +
            request.username + " OR member_7 = " + request.username + " OR member_8 = " + request.username +
            " OR member_9 = " + request.username + " OR paidBy = " + request.username + " order by bill_id desc")
        else:
            cursor.execute("SELECT * FROM Bills WHERE member_0 = " + request.username +
            " OR member_1 = " + request.username + " OR member_2 = " +
            request.username + " OR member_3 = " + request.username +
            " OR member_4 = " + request.username + " OR member_5 = " +
            request.username + " OR member_6 = " + request.username +
            " OR member_7 = " + request.username + " OR member_8 = " +
            request.username + " OR member_9 = " + request.username +
            " OR paidBy = " + request.username + " order by bill_id desc LIMIT " + request.amount)

        iShare_mysql.db.commit()
        for



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iShare_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50061')
    print 'listen on [::]:50061'
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
