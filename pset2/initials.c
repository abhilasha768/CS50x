#include<stdio.h>
#include<cs50.h>
#include<string.h>
#include <ctype.h>
int main(void)
{
    string name=get_string();
    int i;
    int len=strlen(name);
    if(name[0]!=' ')
      printf("%c",toupper(name[0]));
    for(i=1;i<len;i++)
    {
        if(name[i]==' ' && name[i+1]!=' ')
        printf("%c",toupper(name[i+1]));
        
    }
    printf("\n");
}
