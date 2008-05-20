#include "String.h"
#include <stdio.h>
#include <string.h>
#include <assert.h>

String::String()
    : m_data(NULL)
{

}

String::String(const char* str)
    : m_data(NULL)
{
    if( NULL == str) {
	m_data = new char[1];
	m_data[0] = '\0';
    }
    else {
	size_t length = strlen(str)+1;
	m_data = new char[length];
	strcpy(m_data, str);
    }
    
}

String::String(const String& other)
    : m_data(NULL)
{
    size_t length = strlen(other.m_data)+1;
    m_data = new char[length];
    strcpy(m_data, other.m_data);

}

String & String::operator=(const String& other)
{
    if( this == &other ) {
	return *this;
    }
    delete [] m_data;
    size_t length = strlen(other.m_data)+1;
    m_data = new char[length];
    strcpy(m_data, other.m_data);

    return *this;
}

String & String::operator=(const char* str)
{
    if( str == NULL )
    {
	return *this;
    }

    if( m_data == str ) {
	return *this;
    }
    

    delete [] m_data;
    size_t length = strlen(str)+1;
    m_data = new char[length];
    strcpy(m_data, str);

    return *this;
}

String::~String()
{
    delete [] m_data;
}

const char* String::c_str() const
{
    return m_data;
} 

bool String::operator==(const String& other)
{
    return (strcmp(m_data, other.m_data) == 0);
}

bool String::operator!=(const String& other)
{
    return !(*this==other);
}

const char& String::operator[](unsigned int index) const
{
    assert( index < strlen(m_data) );
    return m_data[index];

}

char& String::operator[](unsigned int index)
{
    assert(  index < strlen(m_data) );
    return m_data[index];

}

