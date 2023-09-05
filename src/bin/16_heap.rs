fn heapify<A: PartialOrd + Copy>(xs: &mut Vec<A>, i: usize) {
    if 2 * i + 1 >= xs.len() {
        return;
    }

    let mut largest_idx = 2 * i + 1;
    let mut largest = xs[2 * i + 1];

    if 2 * i + 2 < xs.len() && xs[2 * i + 2] > largest {
        largest_idx = 2 * i + 2;
        largest = xs[largest_idx];
    }

    if largest > xs[i] {
        xs.swap(i, largest_idx);
        heapify(xs, largest_idx);
    }
}

fn heapify_up<A: PartialOrd + Copy>(xs: &mut Vec<A>, i: usize) {
    if i == 0 {
        return;
    }

    let parent = if i % 2 == 0 { i / 2 } else { (i - 1) / 2 };

    if xs[i] > xs[parent] {
        xs.swap(i, parent);
        heapify_up(xs, parent);
    }
}

fn heap_push<A: PartialOrd + Copy>(xs: &mut Vec<A>, x: A) {
    xs.push(x);
    heapify_up(xs, xs.len() - 1);
}

fn max_heap<A: PartialOrd + Copy>(xs: &mut Vec<A>) {
    for i in (0..xs.len() / 2).rev() {
        heapify(xs, i);
    }
}

fn heap_sort<A: PartialOrd + Copy>(xs: &mut Vec<A>) -> Vec<A> {
    let mut sorted = Vec::<A>::with_capacity(xs.len());

    max_heap(xs);
    for _ in 0..xs.len() {
        sorted.push(xs.swap_remove(0));
        heapify(xs, 0);
    }

    return sorted;
}

fn main() {
    let mut xs = vec![1, 2, 3, 4, 5, 6, 7];
    max_heap(&mut xs);
    println!("{xs:?}");
    heap_push(&mut xs, 10);
    println!("{xs:?}");
    let xs = heap_sort(&mut xs);
    println!("{xs:?}");
}
