/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
 
 bool binary_search(int value,int values[],int n)
{
    int end=n-1;
    int start=0;
    while(start<=end)
    {
        int mid=(start+end)/2;
        if(values[mid]==value)
            return true;
        else if(values[mid]>value)
            end=mid-1;
        else
         start=mid+1;
    }
    return false;
}

bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    if(value<0)
        return false;
    else 
        return binary_search(value,values,n);
}



void selection_sort(int values[],int n)
{
    int temp;
    for(int i=0;i<n;i++)
    {
        int min_idx=i;
        for(int j=i+1;j<n;j++)
        {
            if(values[min_idx]>values[j])
             min_idx=j;
        }
        temp=values[min_idx];
        values[min_idx]=values[i];
        values[i]=temp;
        
    }
}


/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    selection_sort(values,n);
    return;
}



