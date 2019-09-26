import math

def minmax(curDepth, nodeIdx, maxTurn, scores, targetDepth):
    if curDepth == targetDepth:
        return scores[nodeIdx]

    if maxTurn:
        return max(minmax(curDepth + 1,
                          nodeIdx * 2,
                          False, scores,
                          targetDepth),
                   minmax(curDepth + 1,
                          nodeIdx * 2 + 1,
                          True, scores,
                          targetDepth))
    else:
        return min(minmax(curDepth + 1,
                          nodeIdx * 2,
                          True, scores,
                          targetDepth),
                   minmax(curDepth + 1,
                          nodeIdx * 2 + 1,
                          True, scores,
                          targetDepth))


def main():
    scores = [3,5,2,9,12,5,23,23]

    treeDepth = math.log(len(scores), 2)

    print("The optimal value is : ", end = "")
    print(minmax(0,0,True, scores, treeDepth))

main()