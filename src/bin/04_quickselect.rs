fn is_median(a: i32, b: i32, c: i32) -> bool {
    return (a <= b && a >= c) || (a <= c && a >= b);
}

fn select_pivot(array: &[i32]) -> usize {
    let first = *array.first().unwrap();
    let last = *array.last().unwrap();
    let middle = array[array.len() / 2];

    if is_median(first, middle, last) {
        return 0;
    } else if is_median(middle, first, last) {
        return array.len() / 2;
    } else {
        return array.len() - 1;
    }
}

fn partition(array: &mut [i32], pivot: usize) -> usize {
    if array.len() == 1 {
        return 0;
    }
    let n = array.len();
    let pivot_value = array[pivot];
    array.swap(pivot, n - 1);
    let mut l: usize = 0;
    for i in 0..n - 1 {
        if array[i] < pivot_value {
            array.swap(i, l);
            l += 1;
        }
    }

    array.swap(l, n - 1);

    return l;
}

fn quickselect(array: &mut [i32], k: usize) -> i32 {
    if array.len() == 1 {
        return array[0];
    }
    let pivot = select_pivot(array);
    let r = partition(array, pivot);

    if r < k {
        return quickselect(&mut array[r + 1..], k - r - 1);
    } else if r > k {
        return quickselect(&mut array[..r], k);
    } else {
        return array[r];
    }
}

fn main() {
    let mut array = vec![5, 1, 3, 2, 0, 6, 4];
    let k = 0;

    let kth = quickselect(&mut array, k);

    println!("k = {k}, kth = {kth}");
}
