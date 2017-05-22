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

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(iShare_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return iShare_pb2.HelloReply(message='Hello, %s!' % request.name)

    def Sign_up(self, request, context):
        log = iShare_log.Log('Sign_up')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iShare_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50061')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
