from queue import Queue
from typing import Callable
from numpy import random
from heapq import heappush, heappop

class TandemSystem:
    def __init__(self, lambda_t: Callable, lambda_max: float, server_attendance_functions: list[Callable], closing_time: int):
        self.lambda_t = lambda_t        # function of intensity at time t
        self.max_lambda = lambda_max    # upperbound of the intensity function
        self.server_attendance_functions = server_attendance_functions # functions to generate each server attendance times
        self.closing_time = closing_time

        self.generator = random.default_rng()

        self.time = 0
        self.served_consumers = 0
        self.events_queue: list[tuple[float, str]] = []     # (time, event_key)
        self.events = {
            'arrival': self.new_arrival,
            'server1_process_ended': self.first_server_departure,
            'server2_process_ended': self.second_server_departure
        }

        self.first_server_status = -1
        self.second_server_status = -1

        self.first_queue = Queue()
        self.second_queue = Queue()

        self.first_queue_arrivals = {}
        self.first_server_arrivals = {}
        self.second_queue_arrivals = {}
        self.second_server_departures = {}

    def arrival_time_generator(self):
        while True:
            t = self.generator.exponential(1 / self.max_lambda)
            if random.rand() < self.lambda_t(t)/ self.max_lambda:
                return t

    def gen_next_arrival(self):
        if self.time >= self.closing_time:
            return
        t = self.arrival_time_generator()
        arrival_time = self.time + t
        if arrival_time < self.closing_time:
            heappush(self.events_queue, (arrival_time, 'arrival'))


    def first_server_process_consumer(self, consumer_id):
        self.first_server_status = consumer_id
        self.first_server_arrivals[consumer_id] = self.time
        processing_time = self.server_attendance_functions[0]()
        processing_end = self.time + processing_time
        heappush(self.events_queue, (processing_end, 'server1_process_ended'))

    def second_server_process_consumer(self, consumer_id):
        self.second_server_status = consumer_id
        self.second_server_departures[consumer_id] = self.time
        processing_time = self.server_attendance_functions[1]()
        processing_end = self.time + processing_time
        heappush(self.events_queue, (processing_end, 'server2_process_ended'))

    def new_arrival(self):
        consumer_id = self.served_consumers
        self.served_consumers += 1
        self.first_queue_arrivals[consumer_id] = self.time

        if self.first_server_status == -1:
            self.first_server_process_consumer(consumer_id)
        else:
            self.first_queue.put(consumer_id)
        self.gen_next_arrival()

    def first_server_departure(self):
        consumer_id = self.first_server_status
        self.second_queue_arrivals[consumer_id] = self.time

        if not self.first_queue.empty():
            next_consumer_id = self.first_queue.get()
            self.first_server_process_consumer(next_consumer_id)
        else:
            self.first_server_status = -1

        if not self.second_queue.empty():
            self.second_queue.put(consumer_id)
        else:
            self.second_server_process_consumer(consumer_id)

    def second_server_departure(self):
        consumer_id = self.second_server_status
        self.second_server_departures[consumer_id] = self.time

        if not self.second_queue.empty():
            next_consumer_id = self.second_queue.get()
            self.second_server_process_consumer(next_consumer_id)
        else:
            self.second_server_status = -1

    def run_simulation(self):
        self.gen_next_arrival()
        while self.events_queue:
            time, event_key = heappop(self.events_queue)
            print(f"Event {event_key}: {time}")
            self.time = time
            self.events[event_key]()









