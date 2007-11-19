#ifndef __HUFFLE_LOADER_H__
#define __HUFFLE_LOADER_H__

const int MAX_SEED = 32000;

class HuffleLoader 
{
  public:
    HuffleLoader();
    ~HuffleLoader();
    static bool load(int seed, char deck[52]);
};
#endif /*__HUFFLE_LOADER_H__*/

