use std::{cell::RefCell, rc::Rc};

#[derive(Debug, Clone, Copy)]
struct Node {
    value: i32,
    id: usize,
    left: Option<usize>,
    right: Option<usize>,
}

type Nodes = Rc<RefCell<Vec<RefCell<Node>>>>;

// rotate_left [A, x, B, y, C] -> [A, x, B, y, C]
impl Node {
    fn new(nodes: &Nodes, value: i32, left: Option<usize>, right: Option<usize>) -> usize {
        let mut nodes = nodes.borrow_mut();
        let id = nodes.len();
        nodes.push(RefCell::new(Node {
            value,
            id,
            left,
            right,
        }));
        return id;
    }
    fn swap(&mut self) {
        (self.left, self.right) = (self.right, self.left);
    }
    fn rotate_left(&mut self, nodes: &mut Nodes) {
        let mut nodes = nodes.borrow_mut();
        let left = nodes[self.left.unwrap()].get_mut();
        let left_right = left.right;
        left.right = Some(self.id);
        self.left = left_right;
        *self = *left;
    }
    fn rotate_right(&mut self, nodes: &mut Nodes) {
        let mut nodes = nodes.borrow_mut();
        let right = nodes[self.right.unwrap()].get_mut();
        let right_left = right.left;
        right.left = Some(self.id);
        self.right = right_left;
        *self = *right;
    }

    fn is_leaf(&self) -> bool {
        return self.left.is_none() && self.right.is_none();
    }

    fn inorder(&self, nodes: &Nodes) -> Vec<i32> {
        let mut seq = Vec::<i32>::new();
        _inorder(self, &mut seq, nodes);
        return seq;
    }

    fn sort(&mut self, nodes: &mut Nodes) {
        let root = self;
        let seq = root.inorder(nodes);
        println!("{seq:?}");
        let mut left = root.left;
        let mut right = root.right;
        match (&mut left, &mut right) {
            (None, None) => (),
            (Some(left), None) => {
                let mut nodes_ = nodes.borrow_mut();
                let left = nodes_[*left].get_mut();
                left.sort(&mut nodes.clone());
                let seq = root.inorder(nodes);
                println!("{seq:?}");
                if left.value > root.value {
                    root.swap();
                }
                let seq = root.inorder(nodes);
                println!("{seq:?}");
            }
            (None, Some(right)) => {
                let mut nodes_ = nodes.borrow_mut();
                let right = nodes_[*right].get_mut();
                right.sort(&mut nodes.clone());
                let seq = root.inorder(nodes);
                println!("{seq:?}");
                if right.value < root.value {
                    root.swap();
                }
                let seq = root.inorder(nodes);
                println!("{seq:?}");
            }
            (Some(left), Some(right)) => {
                let mut nodes_ = nodes.borrow_mut();
                let left = nodes_[*left].get_mut();
                let mut nodes_ = nodes.borrow_mut();
                let right = nodes_[*right].get_mut();
                left.sort(&mut nodes.clone());
                right.sort(&mut nodes.clone());
                let seq = root.inorder(&mut nodes.clone());
                println!("{seq:?}");

                if left.value >= root.value && right.value <= root.value {
                    root.swap();
                    let seq = root.inorder(nodes);
                    println!("{seq:?}");
                } else if (left.value >= root.value && right.value >= root.value)
                    || (left.value <= root.value && right.value <= root.value)
                {
                    if left.value < right.value {
                        root.rotate_left(&mut nodes.clone());
                        let seq = root.inorder(&mut nodes.clone());
                        println!("{seq:?}");
                        root.sort(&mut nodes.clone());
                        let seq = root.inorder(&mut nodes.clone());
                        println!("{seq:?}");
                    } else {
                        root.rotate_right(&mut nodes.clone());
                        let seq = root.inorder(&mut nodes.clone());
                        println!("{seq:?}");
                        root.sort(&mut nodes.clone());
                        let seq = root.inorder(&mut nodes.clone());
                        println!("{seq:?}");
                    }
                }
            }
        }

        let left = root.left;
        let right = root.right;

        if let Some(left) = left {
            let nodes_ = nodes.borrow();
            let left = nodes_[left].as_ptr().borrow();
            let left_right = left.right;
            if let Some(left_right) = left_right {
                let left_right = nodes_[left_right].borrow();
                if left_right.value > root.value {
                    let seq = root.inorder(nodes);
                    println!("{seq:?}");
                    root.rotate_left(&mut nodes.clone());
                    root.sort(&mut nodes.clone());
                    let seq = root.inorder(nodes);
                    println!("{seq:?}");
                }
            }
        }
        if let Some(right) = &right {
            let nodes_ = nodes.borrow();
            let right = nodes_[*right].borrow();
            let right_left = right.left;
            if let Some(left_right) = right_left {
                let left_right = nodes_[left_right].borrow();
                if left_right.value < root.value {
                    let seq = root.inorder(nodes);
                    println!("{seq:?}");
                    root.rotate_right(&mut nodes.clone());
                    root.sort(&mut nodes.clone());
                    let seq = root.inorder(nodes);
                    println!("{seq:?}");
                }
            }
        }
    }
}

fn _inorder(node: &Node, seq: &mut Vec<i32>, nodes: &Nodes) {
    if let Some(left) = node.left {
        let nodes = nodes.clone();
        let nodes_ = nodes.borrow();
        let left = nodes_[left].borrow();
        _inorder(&left, seq, &mut nodes.clone());
    }
    seq.push(node.value);
    if let Some(right) = node.right {
        let nodes_ = nodes.borrow();
        let right = nodes_[right].borrow();
        _inorder(&right, seq, nodes);
    }
}

fn main() {
    let nodes = &mut Rc::new(RefCell::new(Vec::<RefCell<Node>>::new()));
    let root_id = Node::new(
        &nodes.clone(),
        10,
        Some(Node::new(
            &nodes.clone(),
            80,
            Some(Node::new(&nodes.clone(), 100, None, None)),
            Some(Node::new(&nodes.clone(), 60, None, None)),
        )),
        Some(Node::new(
            &nodes.clone(),
            0,
            Some(Node::new(&nodes.clone(), 1000, None, None)),
            Some(Node::new(&nodes.clone(), -1000, None, None)),
        )),
    );
    let root = nodes.borrow();
    let mut root = root[root_id].borrow().clone();
    root.sort(&mut nodes.clone());
    let seq = root.inorder(&nodes);
    println!("root = {seq:?}");
}
