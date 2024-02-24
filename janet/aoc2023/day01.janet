
(import "/janet/aoc2023/utils" :as utils)

(defn string/take-first-last [str]
  (let [a (first str)
        b (last str)]
    (string/join (map string/from-bytes [a b]) "")))

(defn part1 [filename]
  (as-> (utils/slurp-lines filename) prev
    (map utils/filter-alpha prev)
    (map string/take-first-last prev)
    (map int/u64 prev)
    (reduce + 0 prev)))

(defn part2 [filename]
  (->> (utils/slurp-lines filename)
       (map |(string/replace-all "zero" "z0o" $))
       (map |(string/replace-all "one" "o1e" $))
       (map |(string/replace-all "two" "t2o" $))
       (map |(string/replace-all "three" "t3e" $))
       (map |(string/replace-all "four" "f4r" $))
       (map |(string/replace-all "five" "f5e" $))
       (map |(string/replace-all "six" "s6x" $))
       (map |(string/replace-all "seven" "s7n" $))
       (map |(string/replace-all "eight" "e8t" $))
       (map |(string/replace-all "nine" "n9e" $))
       (map utils/filter-alpha)
       (map string/take-first-last)
       (map int/s64)
       (reduce + 0)))

(assert (compare= (part1 "data/day01_part1_sample.txt") 142))
(assert (compare= (part1 "data/day01.txt") 54968))

(assert (compare= (part2 "data/day01_part2_sample.txt") 281))
(assert (compare= (part2 "data/day01.txt") 54094))
