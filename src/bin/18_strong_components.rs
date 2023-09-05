use std::collections::{BTreeMap, HashMap, HashSet, VecDeque};

type Graph = HashMap<char, HashSet<char>>;

fn postorder_dfs(
    graph: &Graph,
    deque: &mut VecDeque<char>,
    visited: &mut HashSet<char>,
    node: &char,
) {
    visited.insert(*node);
    for neighbour in graph.get(&node).unwrap_or(&HashSet::new()).iter() {
        if !visited.contains(neighbour) {
            postorder_dfs(graph, deque, visited, neighbour);
        }
    }
    deque.push_front(*node);
}

fn label_dfs(graph: &Graph, node_label: &mut HashMap<char, usize>, node: &char, label: usize) {
    node_label.insert(*node, label);

    for neighbour in graph[node].iter() {
        if !node_label.contains_key(neighbour) {
            label_dfs(graph, node_label, neighbour, label);
        }
    }
}

fn strong_components(graph: &Graph) -> BTreeMap<usize, HashSet<char>> {
    let rev_graph = rev(graph);
    let mut visited = HashSet::<char>::new();
    let mut deque = VecDeque::<char>::new();
    let mut node_label = HashMap::<char, usize>::new();

    for node in graph.keys() {
        if !visited.contains(node) {
            postorder_dfs(&rev_graph, &mut deque, &mut visited, node);
        }
    }

    let mut label: usize = 0;
    for node in deque.iter() {
        if !node_label.contains_key(node) {
            label_dfs(graph, &mut node_label, node, label);
            label += 1;
        }
    }

    let mut components: BTreeMap<usize, HashSet<char>> = BTreeMap::new();
    for (node, label) in node_label {
        components.entry(label).or_default().insert(node);
    }
    return components;
}

fn rev(graph: &Graph) -> Graph {
    let mut rev_graph = HashMap::<char, HashSet<char>>::new();

    for (a, edges) in graph.iter() {
        for b in edges.iter() {
            rev_graph.entry(*b).or_default().insert(*a);
        }
    }

    return rev_graph;
}

fn main() {
    let graph = Graph::from([
        ('a', HashSet::from(['b'])),
        ('b', HashSet::from(['f'])),
        ('c', HashSet::from(['h'])),
        ('d', HashSet::from(['c'])),
        ('e', HashSet::from(['f', 'i'])),
        ('f', HashSet::from(['g', 'l'])),
        ('g', HashSet::from(['c', 'a'])),
        ('h', HashSet::from(['l', 'd'])),
        ('i', HashSet::from(['n'])),
        ('j', HashSet::from(['k', 'm'])),
        ('k', HashSet::from(['h', 'l'])),
        ('l', HashSet::from(['o', 'p'])),
        ('m', HashSet::from(['i'])),
        ('n', HashSet::from(['j', 'o'])),
        ('o', HashSet::from(['k'])),
        ('p', HashSet::from([])),
    ]);

    let components = strong_components(&graph);

    println!("{components:#?}");
}
