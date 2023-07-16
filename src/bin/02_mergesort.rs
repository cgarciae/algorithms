fn merge(xs: &mut [i32], m: usize) {
    let n = xs.len();
    let mut tmp = Vec::<i32>::with_capacity(xs.len());
    let mut i = 0;
    let mut j = m;

    for _ in 0..xs.len() {
        if j >= n {
            tmp.push(xs[i]);
        } else if i >= m {
            tmp.push(xs[j]);
        } else if xs[i] < xs[j] {
            tmp.push(xs[i]);
            i += 1;
        } else {
            tmp.push(xs[j]);
            j += 1;
        }
    }
    for k in 0..xs.len() {
        xs[k] = tmp[k];
    }
}

fn mergesort(xs: &mut [i32]) {
    if xs.len() <= 1 {
        return;
    }

    let m = xs.len() / 2;

    mergesort(&mut xs[..m]);
    mergesort(&mut xs[m..]);
    merge(xs, m);
}

fn main() {
    let mut xs = vec![4, 3, 5, 2, 1];

    mergesort(&mut xs);

    println!("{xs:?}")
}
