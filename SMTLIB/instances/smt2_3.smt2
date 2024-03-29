(set-logic ALL)
(declare-fun distances () (Array Int (Array Int Int)))
(declare-fun s () (Array Int Int))
(declare-fun x_0_1 () Int)
(declare-fun x_0_2 () Int)
(declare-fun x_0_3 () Int)
(declare-fun x_0_4 () Int)
(declare-fun x_1_1 () Int)
(declare-fun x_1_2 () Int)
(declare-fun x_1_3 () Int)
(declare-fun x_1_4 () Int)
(declare-fun x_2_1 () Int)
(declare-fun x_2_2 () Int)
(declare-fun x_2_3 () Int)
(declare-fun x_2_4 () Int)
(declare-fun x_0_5 () Int)
(declare-fun x_0_0 () Int)
(declare-fun x_1_5 () Int)
(declare-fun x_1_0 () Int)
(declare-fun x_2_5 () Int)
(declare-fun x_2_0 () Int)
(declare-fun load_0 () Int)
(declare-fun load_1 () Int)
(declare-fun load_2 () Int)
(declare-fun y_0 () Int)
(declare-fun y_1 () Int)
(declare-fun y_2 () Int)
(declare-fun max_distance () Int)
(assert (= (select (select distances 0) 0) 0))
(assert (= (select (select distances 0) 1) 3))
(assert (= (select (select distances 0) 2) 3))
(assert (= (select (select distances 0) 3) 6))
(assert (= (select (select distances 0) 4) 5))
(assert (= (select (select distances 0) 5) 6))
(assert (= (select (select distances 0) 6) 6))
(assert (= (select (select distances 0) 7) 2))
(assert (= (select (select distances 1) 0) 3))
(assert (= (select (select distances 1) 1) 0))
(assert (= (select (select distances 1) 2) 6))
(assert (= (select (select distances 1) 3) 3))
(assert (= (select (select distances 1) 4) 4))
(assert (= (select (select distances 1) 5) 7))
(assert (= (select (select distances 1) 6) 7))
(assert (= (select (select distances 1) 7) 3))
(assert (= (select (select distances 2) 0) 3))
(assert (= (select (select distances 2) 1) 4))
(assert (= (select (select distances 2) 2) 0))
(assert (= (select (select distances 2) 3) 7))
(assert (= (select (select distances 2) 4) 6))
(assert (= (select (select distances 2) 5) 3))
(assert (= (select (select distances 2) 6) 5))
(assert (= (select (select distances 2) 7) 3))
(assert (= (select (select distances 3) 0) 6))
(assert (= (select (select distances 3) 1) 3))
(assert (= (select (select distances 3) 2) 7))
(assert (= (select (select distances 3) 3) 0))
(assert (= (select (select distances 3) 4) 5))
(assert (= (select (select distances 3) 5) 6))
(assert (= (select (select distances 3) 6) 7))
(assert (= (select (select distances 3) 7) 4))
(assert (= (select (select distances 4) 0) 5))
(assert (= (select (select distances 4) 1) 4))
(assert (= (select (select distances 4) 2) 6))
(assert (= (select (select distances 4) 3) 3))
(assert (= (select (select distances 4) 4) 0))
(assert (= (select (select distances 4) 5) 3))
(assert (= (select (select distances 4) 6) 3))
(assert (= (select (select distances 4) 7) 3))
(assert (= (select (select distances 5) 0) 6))
(assert (= (select (select distances 5) 1) 7))
(assert (= (select (select distances 5) 2) 3))
(assert (= (select (select distances 5) 3) 6))
(assert (= (select (select distances 5) 4) 3))
(assert (= (select (select distances 5) 5) 0))
(assert (= (select (select distances 5) 6) 2))
(assert (= (select (select distances 5) 7) 4))
(assert (= (select (select distances 6) 0) 6))
(assert (= (select (select distances 6) 1) 7))
(assert (= (select (select distances 6) 2) 5))
(assert (= (select (select distances 6) 3) 6))
(assert (= (select (select distances 6) 4) 3))
(assert (= (select (select distances 6) 5) 2))
(assert (= (select (select distances 6) 6) 0))
(assert (= (select (select distances 6) 7) 4))
(assert (= (select (select distances 7) 0) 2))
(assert (= (select (select distances 7) 1) 3))
(assert (= (select (select distances 7) 2) 3))
(assert (= (select (select distances 7) 3) 4))
(assert (= (select (select distances 7) 4) 3))
(assert (= (select (select distances 7) 5) 4))
(assert (= (select (select distances 7) 6) 4))
(assert (= (select (select distances 7) 7) 0))
(assert (= (select s 0) 3))
(assert (= (select s 1) 2))
(assert (= (select s 2) 6))
(assert (= (select s 3) 8))
(assert (= (select s 4) 5))
(assert (= (select s 5) 4))
(assert (= (select s 6) 4))
(assert (= (select s 7) 0))
(assert (and (>= x_0_1 0) (<= x_0_1 7)))
(assert (and (>= x_0_2 0) (<= x_0_2 7)))
(assert (and (>= x_0_3 0) (<= x_0_3 7)))
(assert (and (>= x_0_4 0) (<= x_0_4 7)))
(assert (and (>= x_1_1 0) (<= x_1_1 7)))
(assert (and (>= x_1_2 0) (<= x_1_2 7)))
(assert (and (>= x_1_3 0) (<= x_1_3 7)))
(assert (and (>= x_1_4 0) (<= x_1_4 7)))
(assert (and (>= x_2_1 0) (<= x_2_1 7)))
(assert (and (>= x_2_2 0) (<= x_2_2 7)))
(assert (and (>= x_2_3 0) (<= x_2_3 7)))
(assert (and (>= x_2_4 0) (<= x_2_4 7)))
(assert (and (= x_0_0 7) (= x_0_5 7)))
(assert (and (= x_1_0 7) (= x_1_5 7)))
(assert (and (= x_2_0 7) (= x_2_5 7)))
(assert (= (+ (ite (= x_0_1 0) 1 0)
      (ite (= x_0_2 0) 1 0)
      (ite (= x_0_3 0) 1 0)
      (ite (= x_0_4 0) 1 0)
      (ite (= x_0_5 0) 1 0)
      (ite (= x_1_1 0) 1 0)
      (ite (= x_1_2 0) 1 0)
      (ite (= x_1_3 0) 1 0)
      (ite (= x_1_4 0) 1 0)
      (ite (= x_1_5 0) 1 0)
      (ite (= x_2_1 0) 1 0)
      (ite (= x_2_2 0) 1 0)
      (ite (= x_2_3 0) 1 0)
      (ite (= x_2_4 0) 1 0)
      (ite (= x_2_5 0) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 1) 1 0)
      (ite (= x_0_2 1) 1 0)
      (ite (= x_0_3 1) 1 0)
      (ite (= x_0_4 1) 1 0)
      (ite (= x_0_5 1) 1 0)
      (ite (= x_1_1 1) 1 0)
      (ite (= x_1_2 1) 1 0)
      (ite (= x_1_3 1) 1 0)
      (ite (= x_1_4 1) 1 0)
      (ite (= x_1_5 1) 1 0)
      (ite (= x_2_1 1) 1 0)
      (ite (= x_2_2 1) 1 0)
      (ite (= x_2_3 1) 1 0)
      (ite (= x_2_4 1) 1 0)
      (ite (= x_2_5 1) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 2) 1 0)
      (ite (= x_0_2 2) 1 0)
      (ite (= x_0_3 2) 1 0)
      (ite (= x_0_4 2) 1 0)
      (ite (= x_0_5 2) 1 0)
      (ite (= x_1_1 2) 1 0)
      (ite (= x_1_2 2) 1 0)
      (ite (= x_1_3 2) 1 0)
      (ite (= x_1_4 2) 1 0)
      (ite (= x_1_5 2) 1 0)
      (ite (= x_2_1 2) 1 0)
      (ite (= x_2_2 2) 1 0)
      (ite (= x_2_3 2) 1 0)
      (ite (= x_2_4 2) 1 0)
      (ite (= x_2_5 2) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 3) 1 0)
      (ite (= x_0_2 3) 1 0)
      (ite (= x_0_3 3) 1 0)
      (ite (= x_0_4 3) 1 0)
      (ite (= x_0_5 3) 1 0)
      (ite (= x_1_1 3) 1 0)
      (ite (= x_1_2 3) 1 0)
      (ite (= x_1_3 3) 1 0)
      (ite (= x_1_4 3) 1 0)
      (ite (= x_1_5 3) 1 0)
      (ite (= x_2_1 3) 1 0)
      (ite (= x_2_2 3) 1 0)
      (ite (= x_2_3 3) 1 0)
      (ite (= x_2_4 3) 1 0)
      (ite (= x_2_5 3) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 4) 1 0)
      (ite (= x_0_2 4) 1 0)
      (ite (= x_0_3 4) 1 0)
      (ite (= x_0_4 4) 1 0)
      (ite (= x_0_5 4) 1 0)
      (ite (= x_1_1 4) 1 0)
      (ite (= x_1_2 4) 1 0)
      (ite (= x_1_3 4) 1 0)
      (ite (= x_1_4 4) 1 0)
      (ite (= x_1_5 4) 1 0)
      (ite (= x_2_1 4) 1 0)
      (ite (= x_2_2 4) 1 0)
      (ite (= x_2_3 4) 1 0)
      (ite (= x_2_4 4) 1 0)
      (ite (= x_2_5 4) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 5) 1 0)
      (ite (= x_0_2 5) 1 0)
      (ite (= x_0_3 5) 1 0)
      (ite (= x_0_4 5) 1 0)
      (ite (= x_0_5 5) 1 0)
      (ite (= x_1_1 5) 1 0)
      (ite (= x_1_2 5) 1 0)
      (ite (= x_1_3 5) 1 0)
      (ite (= x_1_4 5) 1 0)
      (ite (= x_1_5 5) 1 0)
      (ite (= x_2_1 5) 1 0)
      (ite (= x_2_2 5) 1 0)
      (ite (= x_2_3 5) 1 0)
      (ite (= x_2_4 5) 1 0)
      (ite (= x_2_5 5) 1 0))
   1))
(assert (= (+ (ite (= x_0_1 6) 1 0)
      (ite (= x_0_2 6) 1 0)
      (ite (= x_0_3 6) 1 0)
      (ite (= x_0_4 6) 1 0)
      (ite (= x_0_5 6) 1 0)
      (ite (= x_1_1 6) 1 0)
      (ite (= x_1_2 6) 1 0)
      (ite (= x_1_3 6) 1 0)
      (ite (= x_1_4 6) 1 0)
      (ite (= x_1_5 6) 1 0)
      (ite (= x_2_1 6) 1 0)
      (ite (= x_2_2 6) 1 0)
      (ite (= x_2_3 6) 1 0)
      (ite (= x_2_4 6) 1 0)
      (ite (= x_2_5 6) 1 0))
   1))
(assert (= load_0
   (+ (select s x_0_1) (select s x_0_2) (select s x_0_3) (select s x_0_4))))
(assert (<= load_0 15))
(assert (= load_1
   (+ (select s x_1_1) (select s x_1_2) (select s x_1_3) (select s x_1_4))))
(assert (<= load_1 10))
(assert (= load_2
   (+ (select s x_2_1) (select s x_2_2) (select s x_2_3) (select s x_2_4))))
(assert (<= load_2 7))
(assert (and (<= 2 load_0) (>= 15 load_0)))
(assert (and (<= 2 load_1) (>= 15 load_1)))
(assert (and (<= 2 load_2) (>= 15 load_2)))
(assert (=> (= x_0_1 7) (= x_0_2 7)))
(assert (=> (= x_0_2 7) (= x_0_3 7)))
(assert (=> (= x_0_3 7) (= x_0_4 7)))
(assert (=> (= x_0_4 7) (= x_0_5 7)))
(assert (=> (= x_1_1 7) (= x_1_2 7)))
(assert (=> (= x_1_2 7) (= x_1_3 7)))
(assert (=> (= x_1_3 7) (= x_1_4 7)))
(assert (=> (= x_1_4 7) (= x_1_5 7)))
(assert (=> (= x_2_1 7) (= x_2_2 7)))
(assert (=> (= x_2_2 7) (= x_2_3 7)))
(assert (=> (= x_2_3 7) (= x_2_4 7)))
(assert (=> (= x_2_4 7) (= x_2_5 7)))
(assert (=> false
    (<= (ite (distinct x_0_1 7) x_0_1 (- 1))
        (ite (distinct x_0_1 7) x_0_1 (- 1)))))
(assert (=> false
    (<= (ite (distinct x_0_1 7) x_0_1 (- 1))
        (ite (distinct x_0_1 7) x_0_1 (- 1)))))
(assert (=> false
    (<= (ite (distinct x_1_1 7) x_1_1 (- 1))
        (ite (distinct x_1_1 7) x_1_1 (- 1)))))
(assert (=> false (<= load_0 load_1)))
(assert (=> false (<= load_0 load_2)))
(assert (=> false (<= load_1 load_2)))
(assert (= y_0
   (+ (select (select distances x_0_0) x_0_1)
      (select (select distances x_0_1) x_0_2)
      (select (select distances x_0_2) x_0_3)
      (select (select distances x_0_3) x_0_4)
      (select (select distances x_0_4) x_0_5))))
(assert (= y_1
   (+ (select (select distances x_1_0) x_1_1)
      (select (select distances x_1_1) x_1_2)
      (select (select distances x_1_2) x_1_3)
      (select (select distances x_1_3) x_1_4)
      (select (select distances x_1_4) x_1_5))))
(assert (= y_2
   (+ (select (select distances x_2_0) x_2_1)
      (select (select distances x_2_1) x_2_2)
      (select (select distances x_2_2) x_2_3)
      (select (select distances x_2_3) x_2_4)
      (select (select distances x_2_4) x_2_5))))
(assert (and (<= 4 y_0) (>= 42 y_0)))
(assert (and (<= 4 y_1) (>= 42 y_1)))
(assert (and (<= 4 y_2) (>= 42 y_2)))
(assert (let ((a!1 (ite (> y_2 (ite (> y_1 y_0) y_1 y_0)) y_2 (ite (> y_1 y_0) y_1 y_0))))
  (= max_distance a!1)))
(assert (<= 8 max_distance))

(assert (<= max_distance 12))
(assert (>= max_distance 12))
(check-sat)
(get-value (x_0_0))
(get-value (x_0_1))
(get-value (x_0_2))
(get-value (x_0_3))
(get-value (x_0_4))
(get-value (x_0_5))
(get-value (x_1_0))
(get-value (x_1_1))
(get-value (x_1_2))
(get-value (x_1_3))
(get-value (x_1_4))
(get-value (x_1_5))
(get-value (x_2_0))
(get-value (x_2_1))
(get-value (x_2_2))
(get-value (x_2_3))
(get-value (x_2_4))
(get-value (x_2_5))