fn _subset_sum(nums: &[u32], target: i32, subset: &mut Vec<u32>) -> bool {
    if target == 0 {
        return true;
    }
    if target < 0 || nums.len() == 0 {
        return false;
    }

    let elem = nums[0];
    let nums = &nums[1..];

    // with element
    subset.push(elem);
    if _subset_sum(nums, target - elem as i32, subset) {
        return true;
    }
    subset.pop();

    // without elem
    if _subset_sum(nums, target, subset) {
        return true;
    }

    return false;
}
fn subset_sum(nums: &[u32], target: i32) -> Option<Vec<u32>> {
    let mut subset = Vec::<u32>::new();

    if _subset_sum(nums, target, &mut subset) {
        return Some(subset);
    } else {
        return None;
    }
}

fn main() {
    let nums: Vec<u32> = vec![8, 6, 7, 5, 3, 10, 9];

    let answer = subset_sum(&nums, 15);

    println!("answer = {answer:?}")
}
