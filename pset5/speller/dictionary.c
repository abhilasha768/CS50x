/**
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>

#include "dictionary.h"


typedef struct node
{
    char word[LENGTH+1];
    struct node* next;
}
node;

node* hashtable[HASH_SIZE];

unsigned int word_count=0;
bool loaded=false;
int i,n;

int hash_it(char * hash_string)
{
    unsigned int hash = 0;
    for( i=0,n=strlen(hash_string);i<n;i++)
    hash=(hash<<2)^hash_string[i];
    return hash % HASH_SIZE;
    
}


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // TODO
    int len =strlen(word);
    char word_copy[len+1];
    
    
    for( i=0;i<len;i++)
    {
        word_copy[i]=tolower(word[i]);
    }
    word_copy[len]='\0';
    
    int h=hash_it(word_copy);
    
    node *cursor=hashtable[h];
    
    while(cursor!=NULL)
    {
        if(strcmp(cursor->word,word_copy)==0)
        {
            return true;
        }
        else
        {
            cursor= cursor->next;
        }
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // TODO
    for(i=0;i<HASH_SIZE;i++)
    {
        hashtable[i]=NULL;
    }
    
    FILE* fp=fopen(dictionary,"r");
    if(fp==NULL)
    {
        printf("Couldn't open dictionary.\n");
        return false;
    }
    while(true)
    {
        node* new_node=malloc(sizeof(node));
        if(new_node==NULL)
        {
            printf("couln't malloc a new node.\n");
            return false;
        }
        fscanf(fp,"%s",new_node->word);
        new_node->next= NULL;
        if(feof(fp))
        {
            free(new_node);
            break;
        }
        word_count++;
        
        int h=hash_it(new_node->word);
        node *head=hashtable[h];
        if(head==NULL)
        {
            hashtable[h]=new_node;
        }
        else
        {
            new_node->next=hashtable[h];
            hashtable[h]=new_node;
        }
        
    }
    fclose(fp);
    loaded = true;
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    // TODO
    if(loaded)
    {
        return word_count;
    }
    else
    {
        return 0;
    }
   
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    // TODO
    for(i=0;i<HASH_SIZE;i++)
    {
        node * cursor=hashtable[i];
        while(cursor!=NULL)
        {
            node * temp= cursor;
            cursor=cursor->next;
            free(temp);
        }
    }
    loaded=false;
    return true;
}
