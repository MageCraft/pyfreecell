#include "Temp.h"
#include <assert.h>


static const init_size = 10;

Array::Array()
    m_data(NULL), m_length(0), m_capacity(init_size)
{
    m_data = new T[init_size];

}

Array::~Array()
{
    delete [] m_data;

}


void Array::increase_capacity()
{
   if(m_length == m_capacity)  
   {//full, need allocate new memory
       m_capacity = 2*m_capacity;
       T* new_data = new T[m_capacity];
       for(size_t i = 0; i < m_length ; i++)
       {
	   new_data[i] = m_data[i];
       }
       delete [] m_data;
       m_data = new_data;
   }

}

Array& Array::append(const T& e)
{
   increase_capacity(); 
   m_data[m_length] = e;
   m_length++;
}

T Array::pop()
{
    return m_data[m_length--];
}

size_t Array::count()
{
    return m_length;
}

Array& Array::insert(size_t index, const T& e)
{
    assert( index < m_length );
    increase_capacity();

    for( size_t i = m_length ; i >= index; i-- )
    {
	m_data[i] = m_data[i-1];
    }
    
    

}

T Array::remove(size_t index)
{

}
