(ns day01
  (:require [clojure.string :as str]
            [clojure.set :as set]
            [clojure.core :as core]))

(defn char-range [start end]
  (map char (range (int start) (inc (int end)))))

(defn get-alphabet []
  (set/union (set (char-range \a \z)) (set (char-range \A \Z))))

(def alphabet (get-alphabet))

(defn alpha? [c]
  (contains? alphabet c))

(defn filter-not-alpha [s]
  (->> s
       (char-array)
       (filter #(not (alpha? %)))
       (str/join "")))

(defn take-first-last [s]
  (str/join "" (list (first s) (last s))))

(defn part1 [filename]
  (->> filename
    (core/slurp)
    (str/split-lines)
    (map filter-not-alpha)
    (map take-first-last)
    (map #(Integer/parseInt %))
    (reduce +)))

(defn part2 [filename]
  (->> filename
    (core/slurp)
    (str/split-lines)
    (filter #(not= "" %))
    (map #(str/replace % "zero" "zer0ero"))
    (map #(str/replace % "one" "on1ne"))
    (map #(str/replace % "two" "tw2wo"))
    (map #(str/replace % "three" "thre3hree"))
    (map #(str/replace % "four" "fou4our"))
    (map #(str/replace % "five" "fiv5ive"))
    (map #(str/replace % "six" "si6ix"))
    (map #(str/replace % "seven" "seve7even"))
    (map #(str/replace % "eight" "eigh8ightt"))
    (map #(str/replace % "nine" "nin9ine"))
    (map filter-not-alpha)
    (map take-first-last)
    (map #(Integer/parseInt %))
    (reduce +)))

(assert (= (part1 "../data/day01_part1_sample.txt") 142))
(assert (= (part1 "../data/day01.txt") 54968))

(assert (= (part2 "../data/day01_part2_sample.txt") 281))
(assert (= (part2 "../data/day01.txt") 54094))
