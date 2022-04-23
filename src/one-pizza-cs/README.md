https://docs.microsoft.com/en-us/dotnet/core/install/linux-ubuntu

# Google Hash Code 2022 practice problem solution: One Pizza

## Algorithm description:
### Hill-climbing algorithm 
- Empty initialization.
- Update state if new state equals or better in score,
- Random steps.

### Details
1. Initialize solution - no ingredients.
2. Select a random client which does not want the current pizza.
3. Add missing ingredients the random client like.
4. Remove existing ingredients the random client dislike.
5. If the new ingredients score is equal or higher than the existing - update the current pizza ingredients.
6. Goto 2. 

### Notes
- Tried greedy init. Did not improve the solution.
- When calculating the score with the new ingredients - perform a delta calculation which is faster.
- The commited code is hill-climb, constant seed random, stop condition: no improvment found in the last 1M iterations.

## Scores 
Tested the algorithm :
- 1M Iterations - Stop condition: no improvment found in the last 1M iterations. The algorithm takes about 10 minutes to run with the constant seed random in the code.
