package com.threefour.util;

import java.util.Objects;

/**
 * Class that defines a pair.
 * @param <K> Key.
 * @param <V> Value.
 */
public class Pair<K, V> {

    private final K key;
    private V value;


    /**
     * Constructor.
     * @param key Pair's key.
     * @param value Pair's value.
     */
    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    /**
     * Returns pair's key.
     * @return Pair's key.
     */
    public K getKey() {
        return key;
    }

    /**
     * Returns pair's value.
     * @return Pair's value.
     */
    public V getValue() {
        return value;
    }

    /**
     * Changes pair's value.
     * @param value New pair's value.
     * @return Old pair's value.
     */
    public V setValue(V value) {
        V old = this.value;
        this.value = value;
        return old;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        final Pair<?,?> other = (Pair<?,?>) obj;
        return this.key.equals(other.key) && this.value.equals(other.value);
    }

    @Override
    public int hashCode() {
        return Objects.hashCode(key.toString() + value.toString());
    }
    
}
