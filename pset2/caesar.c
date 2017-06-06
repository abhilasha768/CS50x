#include<stdio.h>
#include<string.h>
#include<cs50.h>
#include<ctype.h>
int main(int argc, string argv[])
{   
    int i;
    if(argc!=2)
    {
      printf("Usage: ./caesar k\n");
      return 1;
    }
    int k=atoi(argv[1]);
    if(k > 26)
    {
        k%=26;
    }
    
    printf("plaintext: ");
    string ptext=get_string();
    printf("ciphertext: ");
    for(i=0;i<strlen(ptext);i++)
    {
        if(isalpha(ptext[i]))
        {
            if(islower(ptext[i]))
            {
                if(ptext[i]+k>122)
                 printf("%c",ptext[i]+k-26);
                else
                 printf("%c",ptext[i]+k);
            }
            else if(isupper(ptext[i]))
            {
                if(ptext[i]+k>90)
                 printf("%c",ptext[i]+k-26);
                else
                 printf("%c",ptext[i]+k);
                
            }
        }
        else
         printf("%c",ptext[i]);
    }
    printf("\n");
    
}