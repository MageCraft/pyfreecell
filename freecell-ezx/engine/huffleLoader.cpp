#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "huffleLoader.h"

HuffleLoader::HuffleLoader()
{

}

HuffleLoader::~HuffleLoader()
{

}

bool HuffleLoader::load(int seed, char deck[52])
{
  assert( seed >=0 && seed <= MAX_SEED );

  FILE* fp = fopen("small-list", "r");
  if( fp == NULL ) 
  {
      //don't have data file, shuffle by myself
      int wLeft = 52;
      int i = 0, j=0;
      char d[52];
      for (i = 0; i < 52; i++)      // put unique card in each deck loc.
	  d[i] = i;

      srand(seed);
      for (i = 0; i < 52; i++)
      {
	  j = rand() % wLeft;
	  deck[i] = d[j]+1;
	  d[j] = d[--wLeft];
	  printf("deck[%d]=%d\n", i, deck[i]);
      }
      return true;
  }

  if( fseek(fp, seed * 52, SEEK_SET) != 0 )
    return false;

  fread(deck, sizeof(char), 52, fp);
  fclose(fp);
  return true;
}

