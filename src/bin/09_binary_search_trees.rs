use std::{cell::RefCell, rc::Rc};

#[derive(Debug)]
struct Node {
    value: i32,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
}

trait NodeLike {
    fn swap(&self);
    fn rotate(&self);
    fn is_leaf(&self) -> bool;
}

impl NodeLike for Rc<RefCell<Node>> {
    fn swap(&self) {
        let mut root = self.borrow_mut();
        (root.left, root.right) = (root.right.clone(), root.left.clone());
    }
    fn rotate(&self) {
        let left = self.borrow().left.clone().unwrap();
        let left_right = left.borrow().right.clone();
        left.borrow_mut().right = Some(self.clone());
        self.borrow_mut().left = left_right;
    }

    fn is_leaf(&self) -> bool {
        let root = self.borrow();
        return root.left.is_none() && root.right.is_none();
    }
}

fn node(value: i32) -> Rc<RefCell<Node>> {
    return Rc::new(RefCell::new(Node {
        value,
        left: None,
        right: None,
    }));
}

fn main() {
    let root = node(16);
    let left = node(14);
    root.borrow_mut().left = Some(left);
    root.swap();

    println!("root = {root:?}")
}
