#ifndef __TEST_UTIL1_H__
#define __TEST_UTIL1_H__

#include <iostream>
using namespace std;

class X {

    public:
	X() {cout << "X::X()" << endl;}
	virtual ~X() {cout << "X::~X()" << endl;}


    public:
	virtual void f1() {cout << "X::f1()" << endl;} 
	void f2(int i) {cout << "X::f2(int) " << i << endl;} 
	void f2(float f) {cout << "X::f2(float) " << f << endl;} 

};


class Y : public X 
{
    public:
	Y(){cout << "Y::Y()" << endl;}
	~Y(){ cout << "Y::~Y()" << endl;}

    public:
	void f1(){cout << "Y::f1()" << endl;} 
	void f2(int i){cout << "Y::f2(int) " << i << endl;} 

};
#endif /*__TEST_UTIL1_H__*/
