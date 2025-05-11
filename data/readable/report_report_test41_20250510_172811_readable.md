# ===== SOFTWARE ANALYSIS REPORT =====

---
## Code Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `LOC` | Lines of Code | `296` |
| `SLOC` | Source Lines of Code | `727` |
| `Comment Density` | Proportion of comment lines to total lines | `0.388` |
| `Blank Line Density` | Proportion of blank lines to total lines | `0.205` |

---
## Halstead Metrics:

| Metric | Description | Value |
|--------|-------------|-------|
| `n1` | Number of unique operators | `11` |
| `n2` | Number of unique operands | `236` |
| `N1` | Total occurrences of operators | `353` |
| `N2` | Total occurrences of operands | `1161` |
| `N` | Total number of operators and operands (N1 + N2) | `1514` |
| `n` | Total number of distinct operators and operands (n1 + n2) | `247` |
| `V` | Volume (size of the implementation) | `12033.828` |
| `D` | Difficulty (how difficult the program is to understand) | `27.057` |
| `HN` | Halstead's number (product of difficulty and volume) | `1898.358` |
| `E` | Effort (estimated mental effort) | `325601.731` |
| `T` | Time (estimated time to understand the program) | `18088.985` |
| `B` | Bugs (estimated number of bugs in the program) | `108.534` |
| `M` | Vocabulary (unique operators and operands used) | `-76.847` |


---
### Long Parameter List Detections:

  - Function `'__init__'` at line `1064`
    * **Parameters**: `5`, Threshold: `3`

  - Function `'minimax'` at line `1131`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'maxValue'` at line `1268`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'minValue'` at line `1413`
    * **Parameters**: `6`, Threshold: `3`

  - Function `'alphaBeta'` at line `1707`
    * **Parameters**: `5`, Threshold: `3`

  - Function `'maxValue'` at line `1838`
    * **Parameters**: `5`, Threshold: `3`

  - Function `'minValue'` at line `2012`
    * **Parameters**: `5`, Threshold: `3`

---
### Long Method Detections:

  - Function `'setup_logger'` from line `33` to `67`
    * **Length**: `35 lines`, Threshold: `15`

  - Function `'getAction'` from line `68` to `89`
    * **Length**: `22 lines`, Threshold: `15`

  - Function `'evaluationFunction'` from line `90` to `190`
    * **Length**: `101 lines`, Threshold: `15`

  - Function `'scoreEvaluationFunction'` from line `191` to `216`
    * **Length**: `26 lines`, Threshold: `15`

  - Function `'minimax'` from line `234` to `261`
    * **Length**: `28 lines`, Threshold: `15`

  - Function `'maxValue'` from line `262` to `295`
    * **Length**: `34 lines`, Threshold: `15`

  - Function `'minValue'` from line `296` to `360`
    * **Length**: `65 lines`, Threshold: `15`

  - Function `'alphaBeta'` from line `380` to `402`
    * **Length**: `23 lines`, Threshold: `15`

  - Function `'maxValue'` from line `403` to `441`
    * **Length**: `39 lines`, Threshold: `15`

  - Function `'minValue'` from line `442` to `506`
    * **Length**: `65 lines`, Threshold: `15`

  - Function `'expectimax'` from line `526` to `651`
    * **Length**: `126 lines`, Threshold: `15`

  - Function `'betterEvaluationFunction'` from line `652` to `728`
    * **Length**: `77 lines`, Threshold: `15`

---
### Duplicated Code Detections:

##### Duplicate 1, **Similarity**: `0.95`
 - **Block 1** `(Line 49)`:
```
        if foodList is not None:
                    closestFoodDist = min((manhattanDistance(newPos, food) for food in foodList),
                                          default=float('inf'))
                    score += weights["FOOD"] / (closestFoodDist + 1.0)
                    ra_logger.info("closest food distance: %s", closestFoodDist)
                    ra_logger.info("updated score (food): %s", score)
```
 - **Block 2** `(Line 69)`:
```
        if capsules is not None:
                    closestCapsuleDist = min((manhattanDistance(newPos, capsule) for capsule in capsules),
                                             default=float('inf'))
                    score += weights["CAPSULE"] / (closestCapsuleDist + 1.0)
                    ra_logger.info("closest capsule distance: %s", closestCapsuleDist)
                    ra_logger.info("updated score (capsule): %s", score)
                ra_logger.info("final evaluation score: %s", score)
                return score
```

##### Duplicate 2, **Similarity**: `1.00`
 - **Block 1** `(Line 88)`:
```
        if state.isWin() or state.isLose() or depth == self.depth:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("Terminal state reached: eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 144)`:
```
        if state.isWin() or state.isLose() or depth == self.depth:
                        result = self.evaluationFunction(state)
                        aba_logger.info("terminal state or max depth reached, evaluation value=%d", result)
                        return result
```

##### Duplicate 3, **Similarity**: `0.76`
 - **Block 1** `(Line 88)`:
```
        if state.isWin() or state.isLose() or depth == self.depth:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("Terminal state reached: eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 211)`:
```
        if gameState.isWin() or gameState.isLose() or depth == self.depth * state.getNumAgents():
                        result = self.evaluationFunction(state)
                        em_logger.info("terminal state or max depth reached, evaluation value=%d", result)
                        return result
```

##### Duplicate 4, **Similarity**: `1.00`
 - **Block 1** `(Line 92)`:
```
        if agentIndex == 0:
                        return maxValue(agentIndex, depth, state)
```
 - **Block 2** `(Line 148)`:
```
        if agentIndex == 0:
                        return maxValue(agentIndex, depth, state, alpha, beta)
```

##### Duplicate 5, **Similarity**: `1.00`
 - **Block 1** `(Line 94)`:
```
        else:
                        return minValue(agentIndex, depth, state)
```
 - **Block 2** `(Line 150)`:
```
        else:
                        return minValue(agentIndex, depth, state, alpha, beta)
```

##### Duplicate 6, **Similarity**: `1.00`
 - **Block 1** `(Line 96)`:
```
        def maxValue(agentIndex: int, depth: int, state: GameState):
                    bestValue = float("-inf")
                    legalActions = state.getLegalActions(agentIndex)
                    mma_logger.info("Pacman (max): depth=%d, legalActions=%s", depth, legalActions)
```
 - **Block 2** `(Line 110)`:
```
        def minValue(agentIndex: int, depth: int, state: GameState):
                    bestValue = float("inf")
                    legalActions = state.getLegalActions(agentIndex)
                    mma_logger.info("Ghost (min): agentIndex=%d, depth=%d, legalActions=%s", agentIndex, depth, legalActions)
```

##### Duplicate 7, **Similarity**: `0.81`
 - **Block 1** `(Line 100)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 114)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
                    nextAgent = agentIndex + 1
```

##### Duplicate 8, **Similarity**: `1.00`
 - **Block 1** `(Line 100)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 157)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions, evaluation value=%d", result)
                        return result
```

##### Duplicate 9, **Similarity**: `0.81`
 - **Block 1** `(Line 100)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 175)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions for ghost, evaluation value=%d", result)
                        return result
                    nextAgent = agentIndex + 1
```

##### Duplicate 10, **Similarity**: `0.94`
 - **Block 1** `(Line 100)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
```
 - **Block 2** `(Line 228)`:
```
        if not actions:
                            result = self.evaluationFunction(state)
                            em_logger.info("ghost has no legal actions at depth=%d, returning evaluation=%d", depth, result)
                            return result
```

##### Duplicate 11, **Similarity**: `0.77`
 - **Block 1** `(Line 104)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = minimax(1, depth, successor)
                        bestValue = max(bestValue, value)
                        mma_logger.info("Pacman considering action=%s, value=%f", action, value)
                    return bestValue
```
 - **Block 2** `(Line 122)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = minimax(nextAgent, depth, successor)
                        bestValue = min(bestValue, value)
                        mma_logger.info("Ghost considering action=%s, value=%f", action, value)
                    return bestValue
                bestAction = None
                bestValue = float("-inf")
```

##### Duplicate 12, **Similarity**: `0.85`
 - **Block 1** `(Line 104)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = minimax(1, depth, successor)
                        bestValue = max(bestValue, value)
                        mma_logger.info("Pacman considering action=%s, value=%f", action, value)
                    return bestValue
```
 - **Block 2** `(Line 161)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(1, depth, successor, alpha, beta)
```

##### Duplicate 13, **Similarity**: `0.85`
 - **Block 1** `(Line 104)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = minimax(1, depth, successor)
                        bestValue = max(bestValue, value)
                        mma_logger.info("Pacman considering action=%s, value=%f", action, value)
                    return bestValue
```
 - **Block 2** `(Line 183)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(nextAgent, depth, successor, alpha, beta)
                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)
```

##### Duplicate 14, **Similarity**: `0.81`
 - **Block 1** `(Line 114)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
                    nextAgent = agentIndex + 1
```
 - **Block 2** `(Line 157)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions, evaluation value=%d", result)
                        return result
```

##### Duplicate 15, **Similarity**: `1.00`
 - **Block 1** `(Line 114)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
                    nextAgent = agentIndex + 1
```
 - **Block 2** `(Line 175)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions for ghost, evaluation value=%d", result)
                        return result
                    nextAgent = agentIndex + 1
```

##### Duplicate 16, **Similarity**: `0.77`
 - **Block 1** `(Line 114)`:
```
        if not legalActions:
                        eval_value = self.evaluationFunction(state)
                        mma_logger.info("No legal actions: returning eval=%f", eval_value)
                        return eval_value
                    nextAgent = agentIndex + 1
```
 - **Block 2** `(Line 228)`:
```
        if not actions:
                            result = self.evaluationFunction(state)
                            em_logger.info("ghost has no legal actions at depth=%d, returning evaluation=%d", depth, result)
                            return result
```

##### Duplicate 17, **Similarity**: `1.00`
 - **Block 1** `(Line 119)`:
```
        if nextAgent >= state.getNumAgents():
                        nextAgent = 0
                        depth += 1
```
 - **Block 2** `(Line 180)`:
```
        if nextAgent >= state.getNumAgents():
                        nextAgent = 0
                        depth += 1
```

##### Duplicate 18, **Similarity**: `0.95`
 - **Block 1** `(Line 130)`:
```
        for action in gameState.getLegalActions(0):
                    successor = gameState.generateSuccessor(0, action)
                    value = minimax(1, 0, successor)
                    mma_logger.info("Root: Pacman action=%s, value=%f", action, value)
```
 - **Block 2** `(Line 195)`:
```
        for action in gameState.getLegalActions(0):
                    successor = gameState.generateSuccessor(0, action)
                    value = alphaBeta(1, 0, successor, alpha, beta)
```

##### Duplicate 19, **Similarity**: `1.00`
 - **Block 1** `(Line 141)`:
```
        def getAction(self, gameState):
                aba_logger.info("getting action for gameState=%s", gameState)
```
 - **Block 2** `(Line 204)`:
```
        def getAction(self, gameState):
                em_logger.info("getting action for gameState=%s", gameState)
```

##### Duplicate 20, **Similarity**: `0.76`
 - **Block 1** `(Line 144)`:
```
        if state.isWin() or state.isLose() or depth == self.depth:
                        result = self.evaluationFunction(state)
                        aba_logger.info("terminal state or max depth reached, evaluation value=%d", result)
                        return result
```
 - **Block 2** `(Line 211)`:
```
        if gameState.isWin() or gameState.isLose() or depth == self.depth * state.getNumAgents():
                        result = self.evaluationFunction(state)
                        em_logger.info("terminal state or max depth reached, evaluation value=%d", result)
                        return result
```

##### Duplicate 21, **Similarity**: `0.85`
 - **Block 1** `(Line 152)`:
```
        def maxValue(agentIndex, depth, state, alpha, beta):
                    aba_logger.info("entering maxValue: agentIndex=%d, depth=%d", agentIndex, depth)
                    bestValue = float("-inf")
                    bestAction = None
                    legalActions = state.getLegalActions(agentIndex)
```
 - **Block 2** `(Line 171)`:
```
        def minValue(agentIndex, depth, state, alpha, beta):
                    aba_logger.info("entering minValue: agentIndex=%d, depth=%d", agentIndex, depth)
                    bestValue = float("inf")
                    legalActions = state.getLegalActions(agentIndex)
```

##### Duplicate 22, **Similarity**: `0.81`
 - **Block 1** `(Line 157)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions, evaluation value=%d", result)
                        return result
```
 - **Block 2** `(Line 175)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions for ghost, evaluation value=%d", result)
                        return result
                    nextAgent = agentIndex + 1
```

##### Duplicate 23, **Similarity**: `0.94`
 - **Block 1** `(Line 157)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions, evaluation value=%d", result)
                        return result
```
 - **Block 2** `(Line 228)`:
```
        if not actions:
                            result = self.evaluationFunction(state)
                            em_logger.info("ghost has no legal actions at depth=%d, returning evaluation=%d", depth, result)
                            return result
```

##### Duplicate 24, **Similarity**: `1.00`
 - **Block 1** `(Line 161)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(1, depth, successor, alpha, beta)
```
 - **Block 2** `(Line 183)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(nextAgent, depth, successor, alpha, beta)
                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)
```

##### Duplicate 25, **Similarity**: `0.79`
 - **Block 1** `(Line 161)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(1, depth, successor, alpha, beta)
```
 - **Block 2** `(Line 285)`:
```
        for ghost in ghostStates:
                ghostPos = ghost.getPosition()
                ghostDist = manhattanDistance(pacmanPos, ghostPos)
```

##### Duplicate 26, **Similarity**: `0.77`
 - **Block 1** `(Line 175)`:
```
        if not legalActions:
                        result = self.evaluationFunction(state)
                        aba_logger.info("no legal actions for ghost, evaluation value=%d", result)
                        return result
                    nextAgent = agentIndex + 1
```
 - **Block 2** `(Line 228)`:
```
        if not actions:
                            result = self.evaluationFunction(state)
                            em_logger.info("ghost has no legal actions at depth=%d, returning evaluation=%d", depth, result)
                            return result
```

##### Duplicate 27, **Similarity**: `0.79`
 - **Block 1** `(Line 183)`:
```
        for action in legalActions:
                        successor = state.generateSuccessor(agentIndex, action)
                        value = alphaBeta(nextAgent, depth, successor, alpha, beta)
                        bestValue = min(bestValue, value)
                        beta = min(beta, bestValue)
```
 - **Block 2** `(Line 285)`:
```
        for ghost in ghostStates:
                ghostPos = ghost.getPosition()
                ghostDist = manhattanDistance(pacmanPos, ghostPos)
```

---
# ===== END OF REPORT =====
