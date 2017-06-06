#include<stdio.h>
#include<ctype.h>
#include<cs50.h>
#include<string.h>
int main(int argc,string argv[])
{
        string key=argv[1];
        if(argc!=2)
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
        else
        {
            for(int i=0;i<strlen(key);i++)
            {
                if(isalpha(key[i]))
                {
                    
                }
                else
                {
                    printf("Usage: ./vigenere k\n");
                    return 1;
                }
            }
        }
        printf("plaintext: ");
        string ptext= get_string();
        printf("ciphertext: ");
        if(ptext!=NULL)
        {
           
           for(int i=0,j=0,n=strlen(ptext);i<n;i++,j++)
           {
                if(j>strlen(key)-1)
                {
                   j=0;
                }
                int c=0;
               if(islower(ptext[i]))
               {
                   c=(((ptext[i]-97)+(tolower(key[j])-97))%26)+97;
                   printf("%c",(char)c);
               }
               else if(isupper(ptext[i]))
               {
                   c=(((ptext[i]-65)+(toupper(key[j])-65))%26)+65;
                   printf("%c",(char)c);
               }
           
               else
               { 
                   printf("%c",ptext[i]);
                   j--;
               }
               
           }
        }
        printf("\n");
        
}