from pm4py.models.transition_system import transition_system


def add_arc_from_to(name, fr, to, ts, data=None):
    '''
    Adds a transition from a state to another state in some transition system.
    Assumes from and to are in the transition system!

    Parameters
    ----------
    name: name of the transition
    fr: state from
    to:  state to
    ts: transition system to use

    Returns
    -------
    None
    '''
    tran = transition_system.TransitionSystem.Transition(name, fr, to, data)
    ts.transitions.add(tran)
    fr.outgoing.add(tran)
    to.incoming.add(tran)


def remove_arc_from_to(name, fr, to, ts):
    '''
    Removes a transition with a specific name from a state to another state in some transition system.
    Assumes from and to are in the transition system!

    Parameters
    ----------
    name: name of the transition
    fr: state from
    to:  state to
    ts: transition system to use

    Returns
    -------
    None
    '''
    ts.transitions = [t for t in ts.transitions if t.name != name]
    fr.outgoing = [t for t in fr.outgoing if t.name != name]
    to.incoming = [t for t in to.incoming if t.name != name]


def remove_all_arcs_from_to(fr, to, ts):
    '''
    Removes all transitions from a state to another state in some transition system.
    Assumes from and to are in the transition system!

    Parameters
    ----------
    fr: state from
    to:  state to
    ts: transition system to use

    Returns
    -------
    None
    '''
    names_transitions_to_delete = [t.name for t in ts.transitions if t in fr.outgoing and t in to.incoming]
    ts.transitions = [t for t in ts.transitions if t.name not in names_transitions_to_delete]
    fr.outgoing = [t for t in fr.outgoing if t.name not in names_transitions_to_delete]
    to.incoming = [t for t in to.incoming if t.name not in names_transitions_to_delete]


def transitive_reduction(ts):
    '''
    Computes the transitive reduction of an acyclic transition system.
    Assumes the transition system in input to be acyclic.

    Parameters
    ----------
    ts: acyclic transition system to use

    Returns
    -------
    None
    '''

    def check(state, child, done):
        if child not in done:
            child_children = [tr.to_state for tr in ts.transitions if tr in child.outgoing]
            for child_child in child_children:
                remove_all_arcs_from_to(state, child_child, ts)
                check(state, child_child, done)
            done.add(child)

    for state in ts.states:
        done = set()
        children = [tr.to_state for tr in ts.transitions if tr in state.outgoing]
        for child in children:
            check(state, child, done)


if __name__ == '__main__':
    ts = transition_system.TransitionSystem()
    a = transition_system.TransitionSystem.State('A')
    ts.states.add(a)
    b = transition_system.TransitionSystem.State('B')
    ts.states.add(b)
    c = transition_system.TransitionSystem.State('C')
    ts.states.add(c)
    d = transition_system.TransitionSystem.State('D')
    ts.states.add(d)
    e = transition_system.TransitionSystem.State('E')
    ts.states.add(e)
    add_arc_from_to('AB', a, b, ts)
    add_arc_from_to('AC', a, c, ts)
    add_arc_from_to('AD', a, d, ts)
    add_arc_from_to('AE', a, e, ts)
    add_arc_from_to('BD', b, d, ts)
    add_arc_from_to('CD', c, d, ts)
    add_arc_from_to('CE', c, e, ts)
    add_arc_from_to('DE', d, e, ts)

    from pm4py.models.transition_system import visualize as ts_vis

    # vis = ts_vis.graphviz.visualize(ts)
    # vis.view()
    transitive_reduction(ts)
    vis2 = ts_vis.graphviz.visualize(ts)
    vis2.view()