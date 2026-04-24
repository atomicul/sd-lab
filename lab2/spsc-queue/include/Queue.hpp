#pragma once

#include <concepts>

#include <optional>
#include <utility>

template<typename T>
class IQueue {
public:
    virtual bool push(T val);
    virtual std::optional<T> pop();
    virtual ~IQueue() {}
};

template<typename P, typename T>
concept Producer = requires(P p, T&& val) {
    { p.push(std::move(val)) } -> std::same_as<bool>;
};

template<typename C, typename T>
concept Consumer = requires(C c) {
    { c.pop() } -> std::convertible_to<std::optional<T>>;
};

template<typename Q, typename T>
concept Queue = Producer<Q, T> && Consumer<Q, T>;
