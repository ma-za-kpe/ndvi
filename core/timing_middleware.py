# timing_middleware.py
import time

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()  # Record start time
        response = self.get_response(request)
        end_date = time.time()    # Record end time
        execution_time = end_date - start_time
        print(f"Endpoint: {request.path}, Execution Time: {execution_time} seconds")
        return response
