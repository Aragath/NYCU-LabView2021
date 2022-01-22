#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import copy


# In[2]:


def predict(X: np.ndarray) -> str:
    X = np.array(X).astype(int)
    #print(X)
    score = np.zeros(4)
    level = 2 # depth of the monte-carlo search tree
    actions = ['up', 'down', 'left', 'right']
    i = 0
    temp_X = copy.deepcopy(X)
    # try every action & see return the action that has the max score
    for action in actions: # up, down, left, right
        temp = copy.deepcopy(temp_X)
        if(checkValid(temp, actions[i]) == False):
            score[i] = 0
        else:
            score[i] = play_action(level, actions[i], temp)
        print('the score for', actions[i], 'is', score[i])
        i = i + 1
    temp = score.tolist()
    best_action_index = temp.index(max(temp))
    #if(temp.count(temp[best_action_index]) >=2): # for score that's has same
     #   indices = [i for i, x in enumerate(temp) if x == temp[best_action_index]]
      #  best_action_index = random.choice(indices)
    return actions[best_action_index]
    
def play_action(level: int, action: str, X: np.ndarray) -> int:
    score = 0
    fscore = 0
    #temp_board = X
    fscore = play_action_recursive(level, action, X)
    score = fscore
    return score

def play_action_recursive(level: int, action: str, X: np.ndarray) -> int:
    tScore = 0
    if(level <=0):
        tScore = computeScore(X);
        return tScore
    temp_X = performAction(action, X)
    
    score = np.zeros(4)
    i = 0
    for action in ['up', 'down', 'left', 'right']:
        score[i] = play_action_recursive(level-1, action, temp_X)
        i = i+1
    
    return max(score)

def performAction(action: str, X: np.ndarray) -> np.ndarray:
    if(action == 'up'):
        return moveUp(X)
    elif(action == 'down'):
        return moveDown(X)
    elif(action == 'left'):
        return moveLeft(X)
    elif(action == 'right'):
        return moveRight(X)
    
def moveDown(X: np.ndarray) -> np.ndarray:
    mMerged = np.zeros((4,4), dtype=bool)
    for i in range(2, -1, -1): # [2, 1, 0]
        for j in range(0, 4, 1): # [0, 1, 2, 3]
            if X[i][j] == 0:
                continue
            elif(getsBlockAt(i, j, X) == 0): # doesn't get block
                X[3][j] = X[i][j]############ strange
                X[i][j] = 0
            else: # gets blocked
                blockedRow = getsBlockAt(i, j, X)
                if(X[i][j] == X[blockedRow][j] and not mMerged[blockedRow][j]): # merge
                    X[blockedRow][j] = X[i][j] * 2
                    X[i][j] = 0
                    mMerged[blockedRow][j] = True
                else: # can't merge
                    if(blockedRow - 1 == i): # no movements
                        continue
                    else: # move to the one below
                        X[blockedRow - 1][j] = X[i][j]
                        X[i][j] = 0
    mMerged = np.zeros((4,4), dtype=bool) # reset mMerged
    return X
    
def moveUp(X: np.ndarray) -> np.ndarray:
    X = turnRight(X)
    X = turnRight(X)
    X = moveDown(X)
    X = turnRight(X)
    X = turnRight(X)
    return X
    
def moveLeft(X: np.ndarray) -> np.ndarray:
    X = turnRight(X)
    X = turnRight(X)
    X = turnRight(X)
    X = moveDown(X)
    X = turnRight(X)
    return X

def moveRight(X: np.ndarray) -> np.ndarray:
    X = turnRight(X)
    X = moveDown(X)
    X = turnRight(X)
    X = turnRight(X)
    X = turnRight(X)
    return X
                
def computeScore(X: np.ndarray) -> int:
    score = 0
    for i in range(0, 4, 1):
        for j in range(0, 4, 1):
            s = X[i][j]
            #print(s)
            #score += Decimal(s * (s ** 0.35))
            #score += s * (math.log(s) * 0.35)
            score += s ** 2
    return score

def getsBlockAt(i: int, j: int, X:np.ndarray) -> int: # find who gets blocked by i, j, return the blocked row
    for p in range(i+1, 4, 1):
        if(X[p][j]!=0):
            return p
    return 0

def turnRight(X: np.ndarray) -> np.ndarray:
    #print('original x')
    #print(X)
    temp_array = np.array(list(zip(*X[::-1])))
    #print('turn right x')
    #print(temp_array)
    
    return temp_array

def checkValid(X: np.ndarray, action: str) -> bool:
    prevX = copy.deepcopy(X)
    if(action == 'up'):
        X = moveUp(X)
        if(np.array_equal(prevX, X)):
            return False
    elif(action == 'down'):
        X = moveDown(X)
        if(np.array_equal(prevX, X)):
            return False
    elif(action == 'left'):
        X = moveLeft(X)
        if(np.array_equal(prevX, X)):
            return False
    elif(action == 'right'):
        X = moveRight(X)
        if(np.array_equal(prevX, X)):
            return False
    return True


# In[3]:


array = np.array([[32,16,4,2], 
                  [16,4,2,0], 
                  [4,2,0,0],
                  [0,0,0,0]])

print(predict(array))


# In[ ]:




