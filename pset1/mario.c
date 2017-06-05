#include<stdio.h>
#include<cs50.h>
int main(void)
{   
    int n,m;int i=0,j=0;
    do
    {   
        printf("Height: ");
        n=get_int();
        
    } while(n<0 || n>23);
    m=n;
    
    while(n)
    {
    for( i=1;i<n;i++)
    {
       printf(" ");
    }
    for(j=i;j<=m+1;j++)
       printf("#");
     printf("\n");
     n--;
    }
    
}

