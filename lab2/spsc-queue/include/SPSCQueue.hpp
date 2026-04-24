#pragma once

#include "Queue.hpp"
#include <array>
#include <atomic>
#include <cstddef>
#include <optional>

template <typename T, size_t N>
class SPSCQueue final : public IQueue<T>{
    alignas(64) std::array<T, N> buffer;
    alignas(64) std::atomic<size_t> read_idx{};
    alignas(64) std::atomic<size_t> write_idx{};

public:
    SPSCQueue() = default;

    bool push(T value) {
        const size_t idx = write_idx.load(std::memory_order_relaxed);
        const size_t next_idx = (idx + 1) % N;

        if (next_idx == read_idx.load(std::memory_order_acquire)) {
            return false;
        }

        buffer[idx] = std::move(value);
        write_idx.store(next_idx, std::memory_order_release);

        return true;
    }

    std::optional<T> pop() {
        const size_t idx = read_idx.load(std::memory_order_relaxed);

        if (idx == write_idx.load(std::memory_order_acquire)) {
            return std::nullopt;
        }

        T out = std::move(buffer[idx]);
        read_idx.store((idx + 1) % N, std::memory_order_release);

        return out;
    };
};
