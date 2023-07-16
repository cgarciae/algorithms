fn is_median(a: i32, b: i32, c: i32) -> bool {
    return (a <= b && a >= c) || (a <= c && a >= b);
}

fn select(array: &[i32]) -> usize {
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

fn quicksort(array: &mut [i32]) {
    if array.len() <= 1 {
        return;
    }
    let pivot = select(array);
    let r = partition(array, pivot);
    quicksort(&mut array[..r]);
    quicksort(&mut array[r + 1..]);
}

fn main() {
    let mut xs = vec![4, 3, 5, 2, 1];

    quicksort(&mut xs);

    println!("{xs:?}")
}
