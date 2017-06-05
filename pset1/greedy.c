#include<stdio.h>
#include<math.h>
#include<cs50.h>
int main(void)
{
    float f;int coins=0;
    printf("O hai! How much change is owed?\n");
    f=get_float();
    while(f<0)
    {
        printf("How much change is owed?\n");
        f=get_float();
    }
    int amount=round(f*100);
    while(amount>0)
    {
       if(amount>=25)
       {
           amount-=25;coins++;
       }
       else if(amount>=10)
       {
           amount-=10;coins++;
       }
       else if(amount>=5)
       {
           amount-=5;coins++;
       }
       else if(amount>=1)
       {
           amount-=1;coins++;
       }
    }
    printf("%d\n",coins);
}