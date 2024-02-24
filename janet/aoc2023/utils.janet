(defn slurp-lines [path]
  (->> path
       (slurp)
       (string/trim)
       (string/split "\n")))

(defn string/range [a b]
  (map string/from-bytes (range (a 0) (inc (b 0)))))

(defn get-alphabet []
  (let [lower (string/range "a" "z")
        upper (string/range "A" "Z")]
    (let [tab @{}]
      (each letter lower (put tab letter true))
      (each letter upper (put tab letter true))
      (table/to-struct tab))))

(def alphabet (get-alphabet))

(defn filter-alpha [str]
  (as-> str prev
    (string/bytes prev)
    (map string/from-bytes prev)
    (filter |(not (in alphabet $)) prev)
    (string/join prev "")))