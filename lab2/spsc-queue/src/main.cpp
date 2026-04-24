#include <cstdint>
#include <iostream>
#include <string>
#include <thread>
#include <chrono>
#include <latch>
#include <iomanip>

#include "Queue.hpp"
#include "SPSCQueue.hpp" 
#include "MPMCQueue.hpp" 

constexpr size_t QUEUE_SIZE = 1024;

void producer(std::latch &latch,
              Producer<uint64_t> auto& producer,
              size_t items) {
    latch.arrive_and_wait();

    for (uint64_t i = 1; i <= items; ++i) {
        while(!producer.push(i)) {
            std::this_thread::yield();
        }
    }
}

void consumer(std::latch &latch,
              Consumer<uint64_t> auto& consumer,
              uint64_t num_items,
              uint64_t& out) {
    latch.arrive_and_wait();

    int64_t consumer_checksum = 0;

    for (uint64_t i = 1; i <= num_items; ++i) {
        while (true) {
            auto value = consumer.pop();

            if (!value) {
                std::this_thread::yield();
                continue;
            }

            consumer_checksum += *value;
            break;
        }
    }

    out = consumer_checksum;
}


int main(int argc, const char *argv[]) {
    if (argc != 3) {
        return 1;
    }

    int isUsingSPSCOptimization = std::stoull(argv[1]);
    size_t num_items = std::stoull(argv[2]);

    std::cout << "Items to process: " << num_items << "\n";
    std::cout << "Queue capacity:   " << QUEUE_SIZE << "\n";
    std::cout << "Queue type: " << (isUsingSPSCOptimization ? "SPSC" : "MPMC") << std::endl;

    std::unique_ptr<IQueue<uint64_t>> queue;

    if (isUsingSPSCOptimization) {
        queue = std::make_unique<SPSCQueue<uint64_t, QUEUE_SIZE>>();
    } else {
        queue = std::make_unique<MPMCQueue<uint64_t, QUEUE_SIZE>>();
    }

    // A latch to ensure both threads start at the EXACT same time
    std::latch start_latch(3);

    uint64_t expected_checksum = (num_items * (num_items + 1)) / 2; // Gauss sum formula
    uint64_t consumer_checksum = 0;

    std::jthread producer_thread([&] { 
        producer(start_latch, *queue, num_items);
    });

    std::jthread consumer_thread([&] { 
        consumer(start_latch, *queue, num_items, consumer_checksum);
    });

    start_latch.arrive_and_wait();
    auto start_time = std::chrono::high_resolution_clock::now();

    producer_thread.join();
    consumer_thread.join();

    auto end_time = std::chrono::high_resolution_clock::now();

    auto duration_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
    double duration_sec = duration_ns / 1'000'000'000.0;
    double ops_per_sec = num_items / duration_sec;

    std::cout << "\n--- Results ---\n";
    if (consumer_checksum == expected_checksum) {
        std::cout << "Status:       SUCCESS (Checksum matched)\n";
    } else {
        std::cout << "Status:       FAILED (Data corruption or loss!)\n";
        std::cout << "Expected:     " << expected_checksum << "\n";
        std::cout << "Got:          " << consumer_checksum << "\n";
    }

    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Time elapsed: " << duration_sec << " seconds\n";
    std::cout << "Throughput:   " << (ops_per_sec / 1'000'000.0) << " Million Ops/sec\n";
    std::cout << "Avg Latency:  " << (static_cast<double>(duration_ns) / num_items) << " ns/item\n";

    return 0;
}
