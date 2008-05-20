#include <iostream>
#include "util.h"
#include "util1.h"
#include <stdio.h>
#include <assert.h>
#include "String.h"

void stringCopy(char* strDst, const char* strSrc)
{
    while( (*strDst++=*strSrc++) ) {}
}

void func() 
{

}

int func(int x)
{
    cout << x << endl;
    return x;
}


using namespace std;
int main()
{
    //overwrite
    X* pX = NULL;
    pX = new Y();
    pX->f1();

    //overload
    float f = 10.1;
    pX->f2(10);
    pX->f2(f);

    delete pX;


    String a("haha");
    String b(a);
    String c;
    c = "yeah";
    a = a.c_str();

    cout << c.c_str() << endl;

    assert( a == b );
    assert( a != c );
    assert( a == "haha" );

    assert( a[0] == 'h' );
    a[0] = 'H';
    assert( a == "haha" );





    return 0;
}


