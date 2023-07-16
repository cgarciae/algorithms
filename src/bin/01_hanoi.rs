fn hanoi(n: u32, src: &mut Vec<u32>, dst: &mut Vec<u32>, tmp: &mut Vec<u32>) {
    if n == 0 {
        return;
    }

    println!("[start] src: {src:?}, tmp: {tmp:?}, dst: {dst:?}");

    hanoi(n - 1, src, tmp, dst);
    dst.insert(0, src.remove(0));
    println!("[move] src: {src:?}, tmp: {tmp:?}, dst: {dst:?}");
    hanoi(n - 1, tmp, dst, src);
    println!("[end] src: {src:?}, tmp: {tmp:?}, dst: {dst:?}");
}

fn main() {
    let n = 2;
    let mut src: Vec<u32> = (1..n + 1).collect();
    let mut tmp: Vec<u32> = Vec::new();
    let mut dst: Vec<u32> = Vec::new();

    hanoi(n, &mut src, &mut dst, &mut tmp);

    println!("src: {src:?}, tmp: {tmp:?}, dst: {dst:?}");
}
