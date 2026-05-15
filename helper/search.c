#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//euclidean distance with an early exit threshold
double arrDist(double* arA, double* arB, int lenD, int brC) {
    double distSq = 0;
    for (int i = 0; i < lenD; i++) {
        double diff = arA[i] - arB[i];
        distSq += diff * diff;
        
        if (brC != -1 && distSq > (double)brC * brC) {
            return -1;
        }
    }
    return sqrt(distSq);
}

//return an array of indices that fall within the threshold
int* getClosestNeighbors(double* search, double** dataset, int threshold, int lenD, int datS, int* outCount) {
    int curS = 0;
    int* closest = NULL;

    for (int i = 0; i < datS; i++) {
        double dist = arrDist(search, dataset[i], lenD, threshold);
        
        if (dist != -1) {
            curS++;
            int* temp = realloc(closest, sizeof(int) * curS);
            if (temp == NULL) {
                free(closest);
                return NULL;
            }
            closest = temp;
            closest[curS - 1] = i;
        }
    }
    
    *outCount = curS;
    return closest;
}