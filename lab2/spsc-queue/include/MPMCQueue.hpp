#pragma once

#include "Queue.hpp"

#include <array>
#include <cstddef>
#include <mutex>
#include <optional>

template <typename T, size_t N>
class MPMCQueue final : public IQueue<T> {
    std::mutex mtx;

    std::array<T, N> buffer;
    size_t read_idx{};
    size_t write_idx{};

public:
    MPMCQueue() = default;

    bool push(T value) {
        std::scoped_lock<std::mutex> lock(mtx);
        const size_t next_idx = (write_idx + 1) % N;

        if (next_idx == read_idx) {
            return false;
        }

        buffer[write_idx] = std::move(value);
        write_idx = next_idx;

        return true;
    }

    std::optional<T> pop() {
        std::scoped_lock<std::mutex> lock(mtx);

        if (read_idx == write_idx) {
            return std::nullopt;
        }

        T out = std::move(buffer[read_idx]);
        read_idx++;
        read_idx %= N;

        return out;
    };
};
