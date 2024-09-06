import grpc
import example_pb2
import example_pb2_grpc

# Interceptor to print response metadata
class ClientInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        print(f"Request sent with metadata: {client_call_details.metadata}")
        response = continuation(client_call_details, request)
        print(f"Response metadata: {response.trailing_metadata()}")
        return response

def run():
    # Create a channel and a stub
    with grpc.insecure_channel('localhost:50051') as channel:
        # Add the interceptor to capture metadata
        intercept_channel = grpc.intercept_channel(channel, ClientInterceptor())
        stub = example_pb2_grpc.GreeterStub(intercept_channel)

        # Prepare the request
        request = example_pb2.HelloRequest(name="World")

        # Send the request and receive the response
        response = stub.SayHello(request, metadata=(('client-header', 'header-value'),))
        print(f"Client received: {response.message}")

if __name__ == '__main__':
    run()

