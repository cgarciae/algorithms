fn place_queen(queens: &mut Vec<usize>, r: usize) {
    if queens.len() == 8 {
        println!("{queens:?}");
    }

    for p in 0..8 {
        let mut is_valid = true;
        for (i, pi) in queens.clone().iter().rev().enumerate() {
            let i = (i + 1) as i32;
            let p = p as i32;
            let pi = *pi as i32;
            if p == pi || p == pi - i || p == pi + i {
                is_valid = false;
                break;
            }
        }

        if is_valid {
            queens.push(p);
            place_queen(queens, r + 1);
            queens.pop();
        }
    }
}

fn main() {
    let mut queens = Vec::<usize>::new();

    place_queen(&mut queens, 0);
}
