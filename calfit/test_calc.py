from gurobipy import *
import numpy as np

"""
This function will be called once for each user on each day.
Get the set goal for the next day for the current user

@:param
    true_past_steps: the vector containing the true number of steps of the current user
             (for example, if today is the third day of the study, and the current user's number of steps in day 1 and 2 are 5130 and 6250,
              then truePastNumSteps = [5.13, 6.25])
    past_goals: the past goals of the current user
             (for example, if the goal for the current user for day 1 and day 2 are: 5000 and 6000,
              then, g = [5, 6])
@:return
    goal_for_next_week: the set goal for the next week for the current user
"""
def calc_goal(true_past_steps, past_goals, isControl=False):

    # Initialize the first week by setting all goals to 5000
    # TODO -- Different from that in "testing.py" file
    if type(true_past_steps) != list:
        true_past_steps = [float("%0.3f" % float(s)) for s in true_past_steps.split(',')]
        past_goals = [float(s) for s in past_goals.split(',')]

    '''
    ######################################################
    #         Specify Data and Parameter Values          #
    ######################################################
    '''
    M = 100.0
    els = 0.1
    m = 0
    n = len(past_goals)

    test = {}
    for i in range(m,n):
        test[i] = 1

    # Assume the prior distribution uniform with 10 bings from 0 to 10, then
    m_x = 10
    fe = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
    ub_lb = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
    ub_ub = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

    mu_lb = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    mu_ub = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    p1_lb = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    p1_ub = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]


    '''
    ######################################################
    #               Declare Model -- MAP                 #
    ######################################################
    '''
    model = Model('MAP')


    '''
    ######################################################
    #                Create New Variables                #
    ######################################################
    '''
    # Add variables to the model
    # Notations:
    #   lb: lower bound for new variable
    #   ub: upper bound for new variable
    #   obj: objective coefficient for new variable
    #   vtype: variable type for new variable (GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER, GRB.SEMICONT, or GRB.SEMIINT)
    #   name: name for new variable
    #   column: column object that indicates the set of constraints in which the new variable participates, and the associated coefficients

    # a_0, a_1, ..., a_(n-1)
    a = {}
    for i in range(n):
        a[i] = model.addVar(lb=0, name='a_'+ str(i))

    # u_0, u_1, ..., u_(n-1)
    u = {}
    for i in range(n):
        u[i] = model.addVar(lb=0,name='u_'+ str(i))

    # lambda_1_0, lambda_1_1, ..., lambda_1_(n-1)
    lambda_1 = {}
    for i in range(n):
        lambda_1[i] = model.addVar(lb=0,name='lambda_1_'+ str(i))

    # lambda_3_0, lambda_3_1, ..., lambda_3_(n-1)
    lambda_3 = {}
    for i in range(n):
        lambda_3[i] = model.addVar(lb=0,name='lambda_3_'+ str(i))

    # z_0, z_1, ..., z_(n-1)
    # mu_vec0, mu_vec1, mu_vec(n-1)
    z_mu = {}
    mu_vec = {}
    for i in range(m_x):
        z_mu[i] = model.addVar(vtype=GRB.BINARY, name='z_'+str(i))
        mu_vec[i] = model.addVar(lb = 0, name='mu_vec'+str(i))

    # z_0, z_1, ..., z_(n-1)
    # p1_vec0, p1_vec1, p1_vec(n-1)
    z_p1 = {}
    p1_vec = {}
    for i in range(m_x):
        z_p1[i] = model.addVar(vtype=GRB.BINARY, name='z_'+str(i))
        p1_vec[i] = model.addVar(lb = 0, name='p1_vec'+str(i))

    # z_0, z_1, ..., z_(n-1)
    # ub_vec0, ub_vec1, ub_vec(n-1)
    z_ub = {}
    ub_vec = {}
    for i in range(m_x):
        z_ub[i] = model.addVar(vtype=GRB.BINARY, name='z_'+str(i))
        ub_vec[i] = model.addVar(lb = 0, name='ub_vec'+str(i))

    # ub
    ub = model.addVar(lb=0, name="ub")

    # gamma = model.addVar(name="gamma") -> this is commented by the author
    gamma = 0.85

    # mu
    mu = model.addVar(lb=0,name="mu")

    # p_0, p_1, ..., p_(n-1)
    p = {}
    for i in range(n):
        p[i] = model.addVar(lb=0,name='p_'+ str(i))

    # x_10, x_11, ..., x_1(n-1)
    x_1 = {}
    for i in range(n):
        x_1[i] = model.addVar(vtype=GRB.BINARY,name='x_1'+ str(i))

    # x_20, x_21, ..., x_2(n-1)
    x_2 = {}
    for i in range(n):
        x_2[i] = model.addVar(vtype=GRB.BINARY,name='x_2'+ str(i))

    # x_30, x_31, ..., x_3(n-1)
    x_3 = {}
    for i in range(n):
        x_3[i] = model.addVar(vtype=GRB.BINARY,name='x_3'+ str(i))

    # y_u0, y_u1, ..., y_u(n-1)
    y_u = {}
    for i in range(n):
        y_u[i] = model.addVar(vtype=GRB.BINARY,name='y_u'+ str(i))


    '''
    ######################################################
    #              Integrate New Variables               #
    ######################################################
    '''
    model.update()


    '''
    ######################################################
    #                   Set Objectives                   #
    ######################################################
    '''
    # need to add log histogram
    model.setObjective(
        (  quicksum(a[w] for w in range(n))
         - quicksum(z_ub[i]*np.log(fe[i]) for i in range(m_x))
         - quicksum(z_p1[i]*np.log(fe[i]) for i in range(m_x))
         - quicksum(z_mu[i]*np.log(fe[i]) for i in range(m_x))  )
        , GRB.MINIMIZE)


    '''
    ######################################################
    #                  Add Constraints                   #
    ######################################################
    '''
    # Fix variables associated with cells whose values are pre-specified
    for i in range(n):
        model.addConstr(a[i] >= u[i] - true_past_steps[i], 'const1_' + str(i))
        model.addConstr(a[i] >= true_past_steps[i] - u[i], 'const2_' + str(i))
        model.addConstr(u[i] <= M * y_u[i], 'const3_' + str(i))
        model.addConstr(lambda_1[i] <= M * (1-y_u[i]), 'const4_' + str(i))

    for i in range(m):
        model.addConstr(u[i] == 0.5 * lambda_1[i] + ub, 'const5'+str(i))

    for i in range(m,n):
        model.addConstr(u[i] == 0.5 * (lambda_1[i]+lambda_3[i])+ub, 'const6_' + str(i))
        model.addConstr(lambda_3[i] <= p[i], 'const7_' + str(i))
        model.addConstr((past_goals[i] - els) - M * x_1[i] <= u[i], 'const8_' + str(i))
        model.addConstr(u[i] <= past_goals[i] - els + M * (1 - x_1[i]), 'const9_' + str(i))
        model.addConstr((past_goals[i] - els) - M * (1 - x_2[i]) <= u[i], 'const10_' + str(i))
        model.addConstr(u[i] <= past_goals[i] + els + M * (1 - x_2[i]), 'const11_' + str(i))
        model.addConstr((past_goals[i] + els) - M * (1 - x_3[i]) <= u[i], 'const12_' + str(i))
        model.addConstr(u[i] <= past_goals[i] + els + M * x_3[i], 'const13_' + str(i))
        model.addConstr(p[i]-M*(1-x_1[i]) <= lambda_3[i], 'const14_' + str(i))
        model.addConstr(lambda_3[i] <= M*(1-x_3[i]), 'const15_' + str(i))
        model.addConstr(x_1[i]+x_2[i]+x_3[i] == 1, 'const23_' + str(i))

    for i in range(m,n-1):
        model.addConstr(p[i+1] >= gamma * p[i], 'const16_' + str(i))
        model.addConstr(p[i+1] <= gamma * p[i]+M*(1-x_1[i]), 'const16_' + str(i))
        model.addConstr(p[i+1] >= gamma * p[i]+mu-M*x_1[i], 'const16_' + str(i))
        model.addConstr(p[i+1] <= gamma * p[i]+mu, 'const16_' + str(i))
        bo = past_goals[i + 1] - past_goals[i] < 0
        model.addConstr(x_1[i+1] >= x_1[i] - bo, 'const20_' + str(i))
        model.addConstr(x_2[i+1] <= x_2[i] + bo, 'const21_' + str(i))
        model.addConstr(x_3[i+1] <= x_3[i] + bo, 'const22_' + str(i))

    for i in range(m_x):
        model.addConstr(z_ub[i]*ub_lb[i] <= ub_vec[i], 'const23_'+str(i))
        model.addConstr(ub_vec[i] <= z_ub[i]*ub_ub[i], 'const24_'+str(i))
        model.addConstr(z_p1[i]*p1_lb[i] <= p1_vec[i], 'const25_'+str(i))
        model.addConstr(p1_vec[i] <= z_p1[i]*p1_ub[i], 'const26_'+str(i))
        model.addConstr(z_mu[i]*mu_lb[i] <= mu_vec[i], 'const27_'+str(i))
        model.addConstr(mu_vec[i] <= z_mu[i]*mu_ub[i], 'const28_'+str(i))

    model.addConstr(quicksum(z_ub[i] for i in range(m_x))==1, 'constr29_'+str(i))
    model.addConstr(quicksum(z_mu[i] for i in range(m_x))==1, 'constr30_'+str(i))
    model.addConstr(quicksum(z_p1[i] for i in range(m_x))==1, 'constr31_'+str(i))

    model.addConstr(quicksum(ub_vec[i] for i in range(m_x))==ub, 'constr32_'+str(i))
    model.addConstr(quicksum(p1_vec[i] for i in range(m_x))==p[0], 'constr33_'+str(i))
    model.addConstr(quicksum(mu_vec[i] for i in range(m_x))==mu, 'constr34_'+str(i))


    '''
    ######################################################
    #             Compute Optimal Solution               #
    ######################################################
    '''
    model.optimize()


    '''
    ######################################################
    #           Retrieve Optimization Result             #
    ######################################################
    '''
    # print('\nSolution:\n')
    # for v in model.getVars():
    #     print("{var_name}, {var_value}".format(var_name=v.varName, var_value=v.x))


    '''
    ######################################################
    #         Specify Data and Parameter Values          #
    ######################################################
    '''
    u_map = []
    for key,val in u.items():
        u_map.append(val.X)

    mu_map = mu.X if mu.X != 0 else 0.1
    ub_map = ub.X

    p_map = []
    for key,val in p.items():
        p_map.append(val.X)


    '''
    ######################################################
    #               Declare Model -- goal                 #
    ######################################################
    '''
    model = Model('goal')


    '''
    ######################################################
    #         Specify Data and Parameter Values          #
    ######################################################
    '''
    T = 130
    gamma = 0.85
    els = 0.1
    # mu_head and ub_head comes from MAP
    mu = mu_map # people's reaction to the goal setting
    ub = ub_map # baseline step if no incentive is given
    #p = pt_mle

    '''
    ######################################################
    #                Create New Variables                #
    ######################################################
    '''
    u = {}
    for i in range(T):
        u[i] = model.addVar(lb=0,name='u_'+ str(i))

    lambda_1 = {}
    for i in range(T):
        lambda_1[i] = model.addVar(lb=0,name='lambda_1_'+ str(i))

    lambda_3 = {}
    for i in range(T):
        lambda_3[i] = model.addVar(lb=0,name='lambda_3_'+ str(i))

    g = {}
    for i in range(T):
        g[i] = model.addVar(lb=0, name='goal_'+str(i))

    g_ind = {}
    for i in range(T):
        g_ind[i] = model.addVar(vtype=GRB.BINARY,name='g_ind'+str(i))


    u_min = model.addVar(lb = 0, name="u_min")
    #gamma = model.addVar(name="gamma")
    gamma = 0.85
    #mu = model.addVar(lb=0,name="mu")

    p = {}
    for i in range(T):
        p[i] = model.addVar(lb=0,name='p_'+ str(i))

    #x = {}
    #for i in range(T):
     #   x[i] = model.addVar(lb=0,name='x_'+ str(i))

    x_1 = {}
    for i in range(T):
        x_1[i] = model.addVar(vtype=GRB.BINARY,name='x_1'+ str(i))


    x_2 = {}
    for i in range(T):
        x_2[i] = model.addVar(vtype=GRB.BINARY,name='x_2'+ str(i))

    x_3 = {}
    for i in range(T):
        x_3[i] = model.addVar(vtype=GRB.BINARY,name='x_3'+ str(i))

    y_u = {}
    for i in range(T):
        y_u[i] = model.addVar(vtype=GRB.BINARY,name='y_u'+ str(i))


    '''
    ######################################################
    #              Integrate New Variables               #
    ######################################################
    '''
    model.update()


    '''
    ######################################################
    #                   Set Objectives                   #
    ######################################################
    '''
    model.setObjective(u_min, GRB.MAXIMIZE)


    '''
    ######################################################
    #                  Add Constraints                   #
    ######################################################
    '''
    # Fix variables associated with cells whose values are pre-specified
    for i in range(T-n):
        model.addConstr(u_min <= u[n+i], 'constr1_'+str(i))
        model.addConstr(p[n+i] == gamma * p[n+i-1]+mu*(1-x_1[n+i-1]), 'constr2_'+str(i))
        model.addConstr(g[n+i] - g[n+i-1] <= M * (1-g_ind[n+i-1]), 'constr4_'+str(i))
        model.addConstr(g[n+i] - g[n+i-1] >= -M * g_ind[n+i-1], 'constr5_'+str(i))
        model.addConstr(x_1[n+i] >= x_1[n+i-1] - g_ind[n+i-1], 'const20_' + str(i))
        model.addConstr(x_2[n+i] <= x_2[n+i-1] + g_ind[n+i-1], 'const21_' + str(i))
        model.addConstr(x_3[n+i] <= x_3[n+i-1] + g_ind[n+i-1], 'const22_' + str(i))


    for i in range(n):
        model.addConstr(u[i]-u_map[i] <= els, 'const1_' + str(i))
        model.addConstr( u_map[i]-u[i] <= els, 'const2_' + str(i))
        model.addConstr(p[i]-p_map[i] <= els, 'const1_' + str(i))
        model.addConstr( p_map[i]-p[i] <= els, 'const2_' + str(i))

    for i in range(T):
        model.addConstr(u[i] <= M * y_u[i], 'const3_' + str(i))
        model.addConstr(lambda_1[i] <= M * (1-y_u[i]), 'const4_' + str(i))

    for i in range(m):
        model.addConstr(u[i] == 0.5 * lambda_1[i] + ub, 'const5'+str(i))

    for i in range(m+n,T):
        model.addConstr(u[i] == 0.5 * (lambda_1[i]+lambda_3[i])+ub, 'const6_' + str(i))
        model.addConstr(lambda_3[i] <= p[i], 'const7_' + str(i))
        model.addConstr((g[i]-els) - M * x_1[i] <= u[i], 'const8_' + str(i))
        model.addConstr(u[i] <= g[i]-els+M * (1-x_1[i]), 'const9_' + str(i))
        model.addConstr((g[i]-els) - M * (1-x_2[i]) <= u[i], 'const10_' + str(i))
        model.addConstr(u[i] <= g[i]+els+M * (1-x_2[i]), 'const11_' + str(i))
        model.addConstr((g[i]+els) - M * (1-x_3[i]) <= u[i], 'const12_' + str(i))
        model.addConstr(u[i] <= g[i]+els+M * x_3[i], 'const13_' + str(i))
        model.addConstr(p[i]-M*(1-x_1[i]) <= lambda_3[i], 'const14_' + str(i))
        model.addConstr(lambda_3[i] <= M*(1-x_3[i]), 'const15_' + str(i))
        model.addConstr(x_1[i]+x_2[i]+x_3[i] == 1, 'const23_' + str(i))

    for i in range(n):
        model.addConstr(g[i] == past_goals[i], 'constr24_' + str(i))


    '''
     ######################################################
     #             Compute Optimal Solution               #
     ######################################################
     '''
    model.optimize()


    '''
    ######################################################
    #           Retrieve Optimization Result             #
    ######################################################
    '''
    # print('\nSolution:\n')
    # for v in model.getVars():
    #     print("{var_name}, {var_value}".format(var_name=v.varName, var_value=v.x))


    '''
    ######################################################
    #                   Retrieve Goal                    #
    ######################################################
    '''
    goal = []
    for key, val in g.items():
        goal.append(val.X)

    goal_for_next_week = goal[len(true_past_steps): (len(true_past_steps) + 7)]

    # Return the value of the goal
    return goal_for_next_week

print (calc_goal([1035, 1034, 1033, 1032, 1031, 1030, 1029],[1000, 1000, 1000, 1000, 1000, 1000, 1000]))