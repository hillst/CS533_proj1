#!/usr/bin/env python
import random
STATE = 0
VALUE = 1
class Policy:
    def __init__(self, MDP, name):
        self.MDP_ = MDP
        self.name_ = name

    def choose_action(self, horizon):
        raise Exception("Not an implemented policy")

    def get_name(self):
        return self.name_

    def bellman_backup(self, cur_state, k):
        backup_table = []
        action_table = []
        for t in range(k):
            backup_table.append([])
            action_table.append([])
            for state in self.MDP_.get_states():
                backup_table[t].append(None)
                action_table[t].append(None)
        for t in range(k):
            for state in self.MDP_.get_states():
                if t == 0: #i technically dont need to do this here but whatever
                    backup_table[t][state] = self.MDP_.get_state_reward(state)
                else:
                    max_action = None
                    max_id = -1
                    for action in self.MDP_.get_legal_actions():
                        sum_action = 0
                        for n_state in self.MDP_.get_states():
                            p_transition = self.MDP_.get_p_transition(state, action, n_state)
                            backup_value = backup_table[t-1][n_state]
                            v_transition = p_transition * backup_value
                            sum_action += v_transition
                        sum_action += self.MDP_.get_state_reward(state) 
                        if sum_action > max_action:
                            max_action = sum_action
                            max_id = action
                    backup_table[t][state] = max_action
                    action_table[t][state] = max_id
        return backup_table, action_table


class RandomPolicy(Policy):
    def __init__(self, MDP, name):
        Policy.__init__(self, MDP, name)

    def choose_action(self, horizon):
        to_take = random.randint(0, self.MDP_.get_num_actions() - 1)
        return to_take

"""
No idea what i'm doing with this for resusability
"""
class ValueIterationPolicy(Policy):
    def __init__(self, MDP, name, horizon):
        Policy.__init__(self, MDP, name)    
        self.horizon = horizon - 1
        self.backups, self.actions = self.bellman_backup(self.MDP_.get_state(), horizon)
    """
    Now given our start state and horizon we have to construct our policy
    """
    def choose_action(self, steps_to_go):
        return self.actions[self.MDP_.get_time()][self.MDP_.get_state()]
    """
    Thing described in homework. two n x h matricies, first is the non-stationary value function with i-steps to go
    second is the policy with i states to go

    that is
    value   value
    value   value
    value   value ..

    action  action
    action  action
    action  action ...
        
    """
    def display_value_f(self): 
        transpose = zip(*self.backups[::-1])
        print ",",
        print ",".join(str(i) for i in range(self.horizon, -1, -1))
        for action in range(len(transpose)):
            print str(action) + ",",
            for timestep in transpose[action]:
                print "%.2f," % timestep,
            print ""

    def display_policy(self):
        transpose = zip(*self.actions[::-1])
        print ",",
        print ",".join(str(i) for i in range(self.horizon, -1, -1))
        for action in range(len(transpose)):
            print str(action) + ",", 
            for timestep in transpose[action]:
                print str(timestep) + ",",
            print ""
