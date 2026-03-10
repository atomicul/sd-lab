#ifndef VECTOR_H
#define VECTOR_H 1

#include <cstddef>
#include <algorithm>

template <typename T>
class Vec {
public:
    Vec();
    Vec(size_t size);

    const T &operator[](size_t idx) const;
    T &operator[](size_t idx);

    void push_back(T val);
    void pop_back();
    size_t size();

private:
    void grow();

    size_t _capacity{}, _size{};
    T *_data{};
};

template <typename T>
Vec<T>::Vec() {
    this->_data = new T[4];
    this->_capacity = 4;
}

template <typename T>
Vec<T>::Vec(size_t size) {
    this->_capacity = size;
    this->_data = new T[size];
    this->_size = size;
}

template <typename T>
void Vec<T>::grow() {
    if (_size < _capacity) {
        return;
    }

    const size_t new_capacity = _capacity * 2;

    const auto new_data = new T[new_capacity];

    std::ranges::move(_data, _data + _size, new_data);
    delete[] this->_data;

    this->_data = new_data;
    this->_capacity = new_capacity;
}

template <typename T>
const T &Vec<T>::operator[](size_t idx) const {
    return this->_data[idx];
}

template <typename T>
T &Vec<T>::operator[](size_t idx) {
    return this->_data[idx];
}

template <typename T>
void Vec<T>::push_back(T val) {
    grow();

    _data[_size++] = std::move(val);
}

template <typename T>
void Vec<T>::pop_back() {
    if (_size) {
        _size--;
    }
}

template <typename T>
size_t Vec<T>::size() {
    return _size;
}

#endif
