fn subset_sum(nums: &[u32], target: i32) -> bool {
    if target == 0 {
        return true;
    }
    if target < 0 || nums.len() == 0 {
        return false;
    }

    let elem = nums[0] as i32;
    let nums = &nums[1..];

    if subset_sum(nums, target - elem) || subset_sum(nums, target) {
        return true;
    }

    return false;
}

fn main() {
    let nums: Vec<u32> = vec![11, 6, 5, 1, 7, 13, 12];

    let answer = subset_sum(&nums, 15);

    println!("answer = {answer}")
}
