fn _longest_subquence(
    nums: &[u32],
    prev: Option<u32>,
    subsequence: &mut Vec<u32>,
    longest: &mut Vec<u32>,
) {
    if nums.len() == 0 {
        return;
    }

    let elem = nums[0];
    let nums = &nums[1..];

    if let Some(prev_val) = prev {
        if elem <= prev_val {
            _longest_subquence(nums, prev, subsequence, longest);
            return;
        }
    }

    // with element
    subsequence.push(elem);
    if subsequence.len() > longest.len() {
        longest.clone_from(subsequence);
    }
    _longest_subquence(nums, Some(elem), subsequence, longest);
    subsequence.pop();

    // without elem
    _longest_subquence(nums, prev, subsequence, longest);
}

fn subset_sum(nums: &[u32]) -> Vec<u32> {
    let mut subset = Vec::<u32>::new();
    let mut longest = Vec::<u32>::new();

    _longest_subquence(nums, None, &mut subset, &mut longest);

    return longest;
}

fn main() {
    let nums: Vec<u32> = vec![8, 6, 7, 5, 3, 10, 9];

    let answer = subset_sum(&nums);

    println!("answer = {answer:?}")
}
