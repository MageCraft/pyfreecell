#ifndef __TEST_TEMP_H__
#define __TEST_TEMP_H__

#include <stdlib.h>

template <typename T>
class Array
{
    public:
	Array();
	virtual ~Array();

	Array& append(const T& e);
	T pop();
	size_t count();
	Array& insert(size_t index, const T& e);
	T remove(size_t index);
    
    private:
	Array(const Array& other);
	Array& operator=(const Array& other);

    protected:
	void increase_capacity();

    private:
	T* m_data;
	size_t m_length;
	size_t m_capacity;

	
};
#endif /*__TEST_TEMP_H__*/
