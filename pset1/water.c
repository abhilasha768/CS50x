#include<stdio.h>
#include<cs50.h>
int main(void)
{   
   
   
    printf("Minutes: ");
    int minutes=get_int();
    int bottles=(1.5*128)/16;
    printf("Bottles: %d\n",(minutes*bottles));
    
}