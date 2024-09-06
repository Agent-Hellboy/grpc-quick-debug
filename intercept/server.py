import grpc
from concurrent import futures
import example_pb2
import example_pb2_grpc

# Interceptor to print request and response metadata
class MetadataInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        print(f"Request metadata: {handler_call_details.invocation_metadata}")
        response = continuation(handler_call_details)
        return response

# Implementation of the gRPC service defined in example.proto
class GreeterServicer(example_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        # Send response metadata
        context.send_initial_metadata((('initial-header', 'header-value'),))
        return example_pb2.HelloResponse(message=f"Hello, {request.name}")

def serve():
    # Create the server with the interceptor to capture metadata
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[MetadataInterceptor()])
    example_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

